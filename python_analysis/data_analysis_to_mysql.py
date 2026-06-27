"""
数据分析模块 - 从MySQL读取数据，分析结果保存到MySQL
使用PySpark进行数据分析
流程：从MySQL读取merged_data -> 分析 -> 保存分析结果到MySQL

6个分析：
1. 销售趋势分析（时间维度）
2. 地域分析（地区维度）
3. 产品分析（产品维度）
4. 用户画像分析（用户维度）
5. 促销效果分析（促销维度）
6. 随机森林预测模型
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import DoubleType
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import re


class DataAnalysisToMySQL:
    def __init__(self, spark_session=None):
        if spark_session:
            self.spark = spark_session
        else:
            self.spark = SparkSession.builder \
                .appName("SmartHomeAnalysis") \
                .master("local") \
                .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
                .config("spark.executor.pyspark.memory", "512m") \
                .config("spark.python.worker.timeout", "600") \
                .config("spark.network.timeout", "600s") \
                .config("spark.executor.heartbeatInterval", "60s") \
                .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
                .config("spark.sql.execution.arrow.maxRecordsPerBatch", "10000") \
                .config("spark.driver.host", "localhost") \
                .config("spark.driver.bindAddress", "127.0.0.1") \
                .getOrCreate()
        
        self.mysql_config = {
            'host': '192.168.15.135',
            'port': 3306,
            'user': 'root',
            'password': 'YourNewPassword123!'
        }
        self.database = 'smart_home'
        
        self.init_user_table()
        self.init_analysis_tables()
    
    def init_user_table(self):
        """初始化用户表"""
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE {self.database}")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sys_user (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                    password VARCHAR(255) NOT NULL COMMENT '密码（MD5加密）',
                    email VARCHAR(100) COMMENT '邮箱',
                    phone VARCHAR(20) COMMENT '手机号',
                    real_name VARCHAR(50) COMMENT '真实姓名',
                    role VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '角色：admin/user',
                    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    last_login_time DATETIME COMMENT '最后登录时间',
                    INDEX idx_username (username),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表';
            """)
            
            import hashlib
            cursor.execute("SELECT COUNT(*) FROM sys_user WHERE username = 'admin'")
            admin_exists = cursor.fetchone()[0] > 0
            
            if not admin_exists:
                admin_password = hashlib.md5('admin'.encode('utf-8')).hexdigest()
                cursor.execute("""
                    INSERT INTO sys_user (username, password, email, role, status, real_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, ('admin', admin_password, 'admin@smarthome.com', 'admin', 1, '系统管理员'))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"初始化用户表失败: {e}")
    
    def _create_table_if_not_exists(self, cursor, table_name):
        """创建指定的表（如果不存在）"""
        if table_name == "sales_summary":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_summary (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    sale_date DATE NOT NULL COMMENT '销售日期',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    order_count INT NOT NULL DEFAULT 0 COMMENT '订单数',
                    avg_order_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均订单金额',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_sale_date (sale_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='销售趋势分析表';
            """)
        elif table_name == "region_analysis":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS region_analysis (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    region VARCHAR(50) NOT NULL COMMENT '地区',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    order_count INT NOT NULL DEFAULT 0 COMMENT '订单数',
                    user_count INT NOT NULL DEFAULT 0 COMMENT '用户数',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_region (region)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地域分析表';
            """)
        elif table_name == "product_analysis":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_analysis (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    category VARCHAR(100) COMMENT '产品品类',
                    brand VARCHAR(100) COMMENT '品牌',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    sales_volume INT NOT NULL DEFAULT 0 COMMENT '销量',
                    avg_price DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均价格',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_category (category),
                    INDEX idx_brand (brand)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品分析表';
            """)
        elif table_name == "user_profile":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    gender VARCHAR(10) COMMENT '性别',
                    is_member VARCHAR(10) COMMENT '是否会员',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    user_count INT NOT NULL DEFAULT 0 COMMENT '用户数',
                    avg_consumption DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均消费',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_gender (gender),
                    INDEX idx_is_member (is_member)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户画像分析表';
            """)
        elif table_name == "promotion_analysis":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS promotion_analysis (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    promotion_type VARCHAR(50) NOT NULL COMMENT '促销类型',
                    avg_discount_rate DECIMAL(10, 4) NOT NULL DEFAULT 0.0000 COMMENT '平均折扣率',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    order_count INT NOT NULL DEFAULT 0 COMMENT '订单数',
                    avg_order_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均订单金额',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_promotion_type (promotion_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='促销效果分析表';
            """)
        elif table_name == "prediction_result":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_result (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    prediction_date DATE NOT NULL COMMENT '预测日期',
                    predicted_sales DECIMAL(15, 2) NOT NULL COMMENT '预测值（数量或金额）',
                    actual_sales DECIMAL(15, 2) COMMENT '实际值（数量或金额）',
                    error DECIMAL(15, 2) COMMENT '绝对误差',
                    relative_error DECIMAL(10, 4) COMMENT '相对误差百分比',
                    model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    INDEX idx_prediction_date (prediction_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预测结果表（预测销售数量或金额）';
            """)
            # 如果表已存在但没有 relative_error 列，则添加该列
            try:
                cursor.execute("SELECT relative_error FROM prediction_result LIMIT 1")
                cursor.fetchall()
            except:
                try:
                    cursor.execute("""
                        ALTER TABLE prediction_result 
                        ADD COLUMN relative_error DECIMAL(10, 4) COMMENT '相对误差百分比' 
                        AFTER error
                    """)
                    print("✓ 已为 prediction_result 表添加 relative_error 列")
                except Exception as e:
                    pass  # 列可能已存在
        elif table_name == "feature_importance":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feature_importance (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    feature_name VARCHAR(100) NOT NULL COMMENT '特征名称',
                    importance DECIMAL(10, 6) NOT NULL COMMENT '重要性值',
                    rank INT NOT NULL COMMENT '排名',
                    model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    INDEX idx_feature_name (feature_name),
                    INDEX idx_rank (rank)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='特征重要性表';
            """)
    
    def init_analysis_tables(self):
        """初始化分析结果表"""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.mysql_config, database=self.database, buffered=True)
            cursor = conn.cursor()
            
            # 1. 销售趋势分析表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_summary (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    sales_date DATE NOT NULL COMMENT '销售日期',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    order_count INT NOT NULL DEFAULT 0 COMMENT '订单数',
                    avg_order_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均订单金额',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_sales_date (sales_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='销售趋势分析表';
            """)
            
            # 2. 地域分析表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS region_analysis (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    region VARCHAR(100) NOT NULL COMMENT '地区',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    order_count INT NOT NULL DEFAULT 0 COMMENT '订单数',
                    avg_order_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均订单金额',
                    user_count INT NOT NULL DEFAULT 0 COMMENT '用户数',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_region (region)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地域分析表';
            """)
            
            # 3. 产品分析表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_analysis (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    category VARCHAR(100) COMMENT '产品品类',
                    brand VARCHAR(100) COMMENT '品牌',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    sales_volume INT NOT NULL DEFAULT 0 COMMENT '销量',
                    avg_price DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均价格',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_category (category),
                    INDEX idx_brand (brand)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品分析表';
            """)
            
            # 4. 用户画像分析表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    gender VARCHAR(20) COMMENT '性别',
                    member_type VARCHAR(50) COMMENT '会员类型',
                    user_count INT NOT NULL DEFAULT 0 COMMENT '用户数',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    avg_consumption DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均消费',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_gender (gender),
                    INDEX idx_member_type (member_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户画像分析表';
            """)
            
            # 5. 促销效果分析表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS promotion_analysis (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    promotion_type VARCHAR(100) NOT NULL COMMENT '促销类型',
                    avg_discount_rate DECIMAL(5, 2) NOT NULL DEFAULT 0.00 COMMENT '平均折扣率',
                    total_sales DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '总销售额',
                    order_count INT NOT NULL DEFAULT 0 COMMENT '订单数',
                    avg_order_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '平均订单金额',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_promotion_type (promotion_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='促销效果分析表';
            """)
            
            # 6. 预测结果表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_result (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    prediction_date DATE NOT NULL COMMENT '预测日期',
                    predicted_sales DECIMAL(15, 2) NOT NULL COMMENT '预测值（数量或金额）',
                    actual_sales DECIMAL(15, 2) COMMENT '实际值（数量或金额）',
                    error DECIMAL(15, 2) COMMENT '绝对误差',
                    relative_error DECIMAL(10, 4) COMMENT '相对误差百分比',
                    model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    INDEX idx_prediction_date (prediction_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预测结果表（预测销售数量或金额）';
            """)
            
            # 如果表已存在但没有 relative_error 列，则添加该列
            try:
                cursor.execute("SELECT relative_error FROM prediction_result LIMIT 1")
                cursor.fetchall()  # 读取结果，避免 "Unread result found" 错误
            except:
                try:
                    cursor.execute("""
                        ALTER TABLE prediction_result 
                        ADD COLUMN relative_error DECIMAL(10, 4) COMMENT '相对误差百分比' 
                        AFTER error
                    """)
                    print("✓ 已为 prediction_result 表添加 relative_error 列")
                except Exception as e:
                    print(f"警告: 添加 relative_error 列失败（可能已存在）: {e}")
            
            # 7. 特征重要性表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feature_importance (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    feature_name VARCHAR(100) NOT NULL COMMENT '特征名称',
                    importance DECIMAL(10, 6) NOT NULL COMMENT '重要性值',
                    rank INT NOT NULL COMMENT '排名',
                    model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    INDEX idx_feature_name (feature_name),
                    INDEX idx_rank (rank)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='特征重要性表';
            """)
            
            # 8. 模型评估指标表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_evaluation (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                    target_type VARCHAR(100) COMMENT '预测目标类型',
                    rmse DECIMAL(15, 4) COMMENT 'RMSE (均方根误差)',
                    mae DECIMAL(15, 4) COMMENT 'MAE (平均绝对误差)',
                    r2 DECIMAL(10, 6) COMMENT 'R² (决定系数)',
                    avg_relative_error DECIMAL(10, 4) COMMENT '平均相对误差百分比',
                    sample_count INT COMMENT '样本数量',
                    evaluation_date DATE NOT NULL COMMENT '评估日期',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_model_type (model_type),
                    INDEX idx_evaluation_date (evaluation_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模型评估指标表';
            """)
            
            conn.commit()
            print("✓ 分析结果表初始化完成")
        except Exception as e:
            print(f"初始化分析结果表失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 确保连接被关闭
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def load_data_from_mysql(self):
        """从MySQL读取merged_data表的数据"""
        print("=" * 60)
        print("从MySQL读取merged_data表的数据...")
        print("=" * 60)
        
        try:
            conn = mysql.connector.connect(**self.mysql_config, database=self.database)
            query = "SELECT * FROM merged_data"
            df_pd = pd.read_sql(query, conn)
            conn.close()
            
            if len(df_pd) == 0:
                print("警告: merged_data表中没有数据，请先执行步骤1和步骤2")
                return None
            
            print(f"读取数据: {len(df_pd)} 行, {len(df_pd.columns)} 列")
            
            # 先使用Pandas处理数据转换，减少Spark操作
            numeric_keywords = ["金额", "单价", "价格", "数量", "件", "折扣", "率", "销售额"]
            for col_name in df_pd.columns:
                if any(keyword in col_name for keyword in numeric_keywords):
                    try:
                        df_pd[col_name] = df_pd[col_name].astype(str).str.replace(r'[^0-9.-]', '', regex=True)
                        df_pd[col_name] = pd.to_numeric(df_pd[col_name], errors='coerce').fillna(0)
                    except:
                        pass
            
            # 创建Spark DataFrame（使用Arrow加速，避免触发worker）
            try:
                df = self.spark.createDataFrame(df_pd)
                # 不调用count()，避免触发worker连接
                print(f"从MySQL加载数据成功: {len(df_pd)} 行")
                return df
            except Exception as e:
                print(f"创建Spark DataFrame失败: {e}")
                print("尝试使用备用方法...")
                # 如果失败，直接返回Pandas DataFrame，后续分析使用Pandas
                return df_pd
            
        except Exception as e:
            print(f"从MySQL加载数据失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def find_column(self, df, keywords):
        """查找包含关键词的列"""
        for keyword in keywords:
            for col_name in df.columns:
                if keyword in col_name:
                    return col_name
        return None
    
    def convert_to_numeric(self, df, col_name):
        """将列转换为数值类型"""
        try:
            df = df.withColumn(col_name, regexp_replace(col(col_name), "[^0-9.-]", ""))
            df = df.withColumn(col_name, 
                when((col(col_name) != "") & (col(col_name).isNotNull()) & (col(col_name) != "null"), col(col_name))
                .otherwise("0"))
            df = df.withColumn(col_name, col(col_name).cast("double"))
        except:
            df = df.withColumn(col_name, lit(0.0).cast("double"))
        return df
    
    def save_to_mysql(self, table_name, df_pd, clear_table=True):
        """保存DataFrame到MySQL"""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.mysql_config, database=self.database)
            cursor = conn.cursor()
            
            # 确保数据库存在
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE {self.database}")
            
            # 检查表是否存在，如果不存在则创建表
            try:
                cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
                # 确保读取结果，避免 "Unread result found" 错误
                cursor.fetchall()
            except mysql.connector.Error as e:
                if e.errno == 1146:  # Table doesn't exist
                    print(f"警告: 表 {table_name} 不存在，正在创建表...")
                    # 直接创建该表
                    self._create_table_if_not_exists(cursor, table_name)
                    conn.commit()
                    print(f"✓ 表 {table_name} 已创建")
            
            if clear_table:
                # 清空表数据
                try:
                    cursor.execute(f"TRUNCATE TABLE {table_name}")
                except:
                    # 如果TRUNCATE失败，尝试DELETE
                    try:
                        cursor.execute(f"DELETE FROM {table_name}")
                    except:
                        pass
            
            # 处理NaN和inf值
            df_pd = df_pd.replace([np.inf, -np.inf], np.nan)
            df_pd = df_pd.fillna(0)
            
            # 获取列名
            columns = df_pd.columns.tolist()
            placeholders = ', '.join(['%s'] * len(columns))
            column_names = ', '.join([f"`{col}`" for col in columns])
            
            insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            
            # 批量插入
            batch_size = 1000
            for i in range(0, len(df_pd), batch_size):
                batch_df = df_pd.iloc[i:i+batch_size]
                batch_data = []
                for _, row in batch_df.iterrows():
                    row_data = []
                    for col in columns:
                        value = row[col]
                        if pd.isna(value):
                            row_data.append(None)
                        elif isinstance(value, (int, float)):
                            if np.isinf(value) or np.isnan(value):
                                row_data.append(0)
                            else:
                                row_data.append(float(value) if isinstance(value, float) else int(value))
                        else:
                            row_data.append(str(value))
                    batch_data.append(tuple(row_data))
                
                cursor.executemany(insert_sql, batch_data)
            
            conn.commit()
            print(f"✓ 数据已保存到 {table_name}: {len(df_pd)} 条记录")
        except Exception as e:
            print(f"保存数据到 {table_name} 失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 确保连接被关闭
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def analysis_1_sales_trend(self, df):
        """分析1: 销售趋势分析（时间维度）"""
        print("\n" + "=" * 60)
        print("分析1: 销售趋势分析（时间维度）")
        print("=" * 60)
        
        date_col = self.find_column(df, ["订单日期", "日期", "时间", "date"])
        if not date_col:
            print("警告: 未找到日期列")
            return None
        
        sales_col = self.find_column(df, ["销售额", "订单总金额（元）", "订单总金额"])
        if not sales_col:
            price_col = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            quantity_col = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            if price_col and quantity_col:
                df = df.withColumn("销售额", col(price_col) * col(quantity_col))
                sales_col = "销售额"
            else:
                print("警告: 无法计算销售额")
                return None
        
        df = self.convert_to_numeric(df, sales_col)
        
        try:
            trend_df = df.groupBy(
                date_format(to_date(col(date_col), "yyyy-MM-dd"), "yyyy-MM-dd").alias("sales_date")
            ).agg(
                sum(col(sales_col)).alias("total_sales"),
                count("*").alias("order_count"),
                avg(col(sales_col)).alias("avg_order_amount")
            ).orderBy("sales_date")
        except:
            trend_df = df.groupBy(
                col(date_col).alias("sales_date")
            ).agg(
                sum(col(sales_col)).alias("total_sales"),
                count("*").alias("order_count"),
                avg(col(sales_col)).alias("avg_order_amount")
            ).orderBy("sales_date")
        
        trend_pd = trend_df.toPandas()
        trend_pd.columns = ['sales_date', 'total_sales', 'order_count', 'avg_order_amount']
        
        self.save_to_mysql("sales_summary", trend_pd)
        return trend_pd
    
    def analysis_2_region(self, df):
        """分析2: 地域分析（地区维度）"""
        print("\n" + "=" * 60)
        print("分析2: 地域分析（地区维度）")
        print("=" * 60)
        
        region_col = self.find_column(df, ["用户所在省份", "省", "市", "地区"])
        if not region_col:
            print("警告: 未找到地区列")
            return None
        
        sales_col = self.find_column(df, ["销售额", "订单总金额（元）", "订单总金额"])
        if not sales_col:
            price_col = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            quantity_col = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            if price_col and quantity_col:
                df = df.withColumn("销售额", col(price_col) * col(quantity_col))
                sales_col = "销售额"
            else:
                print("警告: 无法计算销售额")
                return None
        
        df = self.convert_to_numeric(df, sales_col)
        
        order_col = self.find_column(df, ["订单编号"])
        
        region_df = df.groupBy(region_col).agg(
            sum(col(sales_col)).alias("total_sales"),
            count("*").alias("order_count"),
            avg(col(sales_col)).alias("avg_order_amount"),
            countDistinct(order_col if order_col else lit("1")).alias("user_count")
        ).orderBy(desc("total_sales"))
        
        region_pd = region_df.toPandas()
        region_pd.columns = ['region', 'total_sales', 'order_count', 'avg_order_amount', 'user_count']
        
        self.save_to_mysql("region_analysis", region_pd)
        return region_pd
    
    def analysis_3_product(self, df):
        """分析3: 产品分析（产品维度）"""
        print("\n" + "=" * 60)
        print("分析3: 产品分析（产品维度）")
        print("=" * 60)
        
        category_col = self.find_column(df, ["产品品类", "品类", "类别"])
        brand_col = self.find_column(df, ["品牌名称", "品牌"])
        
        sales_col = self.find_column(df, ["销售额", "订单总金额（元）", "订单总金额"])
        if not sales_col:
            price_col = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            quantity_col = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            if price_col and quantity_col:
                df = df.withColumn("销售额", col(price_col) * col(quantity_col))
                sales_col = "销售额"
            else:
                print("警告: 无法计算销售额")
                return None
        
        df = self.convert_to_numeric(df, sales_col)
        
        results = []
        
        if category_col:
            quantity_col_num = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            price_col_num = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            
            category_df = df.groupBy(category_col).agg(
                sum(col(sales_col)).alias("total_sales"),
                sum(col(quantity_col_num) if quantity_col_num else lit(0)).alias("sales_volume"),
                avg(col(price_col_num) if price_col_num else lit(0)).alias("avg_price")
            ).orderBy(desc("total_sales"))
            
            category_pd = category_df.toPandas()
            category_pd.columns = ['category', 'total_sales', 'sales_volume', 'avg_price']
            category_pd['brand'] = None
            results.append(category_pd)
        
        if brand_col:
            quantity_col_num = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            price_col_num = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            
            brand_df = df.groupBy(brand_col).agg(
                sum(col(sales_col)).alias("total_sales"),
                sum(col(quantity_col_num) if quantity_col_num else lit(0)).alias("sales_volume"),
                avg(col(price_col_num) if price_col_num else lit(0)).alias("avg_price")
            ).orderBy(desc("total_sales"))
            
            brand_pd = brand_df.toPandas()
            brand_pd.columns = ['brand', 'total_sales', 'sales_volume', 'avg_price']
            brand_pd['category'] = None
            results.append(brand_pd)
        
        if results:
            combined_pd = pd.concat(results, ignore_index=True)
            self.save_to_mysql("product_analysis", combined_pd)
            return combined_pd
        else:
            return None
    
    def analysis_4_user_profile(self, df):
        """分析4: 用户画像分析（用户维度）"""
        print("\n" + "=" * 60)
        print("分析4: 用户画像分析（用户维度）")
        print("=" * 60)
        
        gender_col = self.find_column(df, ["用户性别", "性别"])
        member_col = self.find_column(df, ["是否会员", "会员等级", "会员类型"])
        
        sales_col = self.find_column(df, ["销售额", "订单总金额（元）", "订单总金额"])
        if not sales_col:
            price_col = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            quantity_col = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            if price_col and quantity_col:
                df = df.withColumn("销售额", col(price_col) * col(quantity_col))
                sales_col = "销售额"
            else:
                print("警告: 无法计算销售额")
                return None
        
        df = self.convert_to_numeric(df, sales_col)
        
        results = []
        
        if gender_col:
            order_col = self.find_column(df, ["订单编号"])
            gender_df = df.groupBy(gender_col).agg(
                countDistinct(order_col if order_col else lit("1")).alias("user_count"),
                sum(col(sales_col)).alias("total_sales"),
                avg(col(sales_col)).alias("avg_consumption")
            )
            
            gender_pd = gender_df.toPandas()
            gender_pd.columns = ['gender', 'user_count', 'total_sales', 'avg_consumption']
            gender_pd['member_type'] = None
            results.append(gender_pd)
        
        if member_col:
            order_col = self.find_column(df, ["订单编号"])
            member_df = df.groupBy(member_col).agg(
                countDistinct(order_col if order_col else lit("1")).alias("user_count"),
                sum(col(sales_col)).alias("total_sales"),
                avg(col(sales_col)).alias("avg_consumption")
            )
            
            member_pd = member_df.toPandas()
            member_pd.columns = ['member_type', 'user_count', 'total_sales', 'avg_consumption']
            member_pd['gender'] = None
            results.append(member_pd)
        
        if results:
            combined_pd = pd.concat(results, ignore_index=True)
            self.save_to_mysql("user_profile", combined_pd)
            return combined_pd
        else:
            return None
    
    def analysis_5_promotion(self, df):
        """分析5: 促销效果分析（促销维度）"""
        print("\n" + "=" * 60)
        print("分析5: 促销效果分析（促销维度）")
        print("=" * 60)
        
        promotion_col = self.find_column(df, ["促销类型", "促销"])
        discount_col = self.find_column(df, ["促销折扣率", "折扣率", "折扣"])
        
        if not promotion_col:
            print("警告: 未找到促销类型列")
            return None
        
        sales_col = self.find_column(df, ["销售额", "订单总金额（元）", "订单总金额"])
        if not sales_col:
            price_col = self.find_column(df, ["销售单价（元）", "销售单价", "单价"])
            quantity_col = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
            if price_col and quantity_col:
                df = df.withColumn("销售额", col(price_col) * col(quantity_col))
                sales_col = "销售额"
            else:
                print("警告: 无法计算销售额")
                return None
        
        df = self.convert_to_numeric(df, sales_col)
        
        if discount_col:
            df = self.convert_to_numeric(df, discount_col)
            promotion_df = df.groupBy(promotion_col).agg(
                avg(col(discount_col)).alias("avg_discount_rate"),
                sum(col(sales_col)).alias("total_sales"),
                count("*").alias("order_count"),
                avg(col(sales_col)).alias("avg_order_amount")
            ).orderBy(desc("total_sales"))
        else:
            promotion_df = df.groupBy(promotion_col).agg(
                lit(0.0).alias("avg_discount_rate"),
                sum(col(sales_col)).alias("total_sales"),
                count("*").alias("order_count"),
                avg(col(sales_col)).alias("avg_order_amount")
            ).orderBy(desc("total_sales"))
        
        promotion_pd = promotion_df.toPandas()
        promotion_pd.columns = ['promotion_type', 'avg_discount_rate', 'total_sales', 'order_count', 'avg_order_amount']
        
        self.save_to_mysql("promotion_analysis", promotion_pd)
        return promotion_pd
    
    def analysis_6_random_forest(self, df):
        """分析6: 随机森林预测模型 - 预测销售数量和金额"""
        print("\n" + "=" * 60)
        print("分析6: 随机森林预测模型 - 预测销售数量和金额")
        print("=" * 60)
        
        # 确保model_evaluation表已创建
        try:
            conn = mysql.connector.connect(**self.mysql_config, database=self.database)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_evaluation (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                    target_type VARCHAR(100) COMMENT '预测目标类型',
                    rmse DECIMAL(15, 4) COMMENT 'RMSE (均方根误差)',
                    mae DECIMAL(15, 4) COMMENT 'MAE (平均绝对误差)',
                    r2 DECIMAL(10, 6) COMMENT 'R² (决定系数)',
                    avg_relative_error DECIMAL(10, 4) COMMENT '平均相对误差百分比',
                    sample_count INT COMMENT '样本数量',
                    evaluation_date DATE NOT NULL COMMENT '评估日期',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_model_type (model_type),
                    INDEX idx_evaluation_date (evaluation_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模型评估指标表';
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("✓ model_evaluation表已确认存在")
        except Exception as e:
            print(f"警告: 创建model_evaluation表失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 优先预测销售数量
        target_col = self.find_column(df, ["销售数量（件）", "销售数量", "数量"])
        target_name = "销售数量"
        
        # 如果没有数量列，则预测金额
        if not target_col:
            target_col = self.find_column(df, ["订单总金额（元）", "订单总金额", "销售额"])
            target_name = "销售金额"
            if not target_col:
                print("警告: 未找到销售数量或金额列，跳过模型训练")
                return None
        
        print(f"预测目标: {target_name} ({target_col})")
        
        df = self.convert_to_numeric(df, target_col)
        
        # 异常值处理：使用Pandas计算分位数（更稳定）
        try:
            # 先转换为Pandas进行分位数计算
            target_sample = df.select(target_col).limit(10000).toPandas()
            if len(target_sample) > 0 and target_col in target_sample.columns:
                q25 = float(target_sample[target_col].quantile(0.25))
                q75 = float(target_sample[target_col].quantile(0.75))
                iqr = float(q75 - q25) if q75 > q25 else float(q75 * 0.5)
                
                # 只保留在合理范围内的数据（Q1-1.5*IQR 到 Q3+1.5*IQR）
                lower_bound_val = q25 - 1.5 * iqr if iqr > 0 else 0.0
                lower_bound = lower_bound_val if lower_bound_val > 0 else 0.0
                upper_bound = q75 + 1.5 * iqr if iqr > 0 else q75 * 2.0
                
                df = df.filter(
                    (col(target_col).isNotNull()) & 
                    (col(target_col) > 0) &
                    (col(target_col) >= lower_bound) &
                    (col(target_col) <= upper_bound)
                )
                print(f"异常值过滤: 保留范围 [{lower_bound:.2f}, {upper_bound:.2f}]")
            else:
                df = df.filter(col(target_col).isNotNull() & (col(target_col) > 0))
        except Exception as e:
            # 如果分位数计算失败，使用简单过滤
            df = df.filter(col(target_col).isNotNull() & (col(target_col) > 0))
            print(f"使用简单过滤（分位数计算失败: {e}）")
        
        print("准备特征数据...")
        exclude_cols = [target_col, "id", "订单编号", "处理时间", "create_time", "prediction_date", 
                        "sales_产品型号", "sales_订单日期", "price_产品品类", "price_品牌名称", 
                        "price_销售单价（元）", "model_产品品类", "model_品牌名称", "产品型号"]
        
        # 根据预测目标选择相关特征（更精准的特征选择）
        if target_name == "销售数量":
            # 预测数量时，使用金额、价格、折扣等作为特征
            numeric_feature_keywords = ["金额", "价格", "单价", "折扣", "率", "订单总金额"]
        else:
            # 预测金额时，使用数量、折扣等作为特征
            numeric_feature_keywords = ["数量", "件", "折扣", "率", "销售数量"]
        
        # 分类特征：使用业务维度特征
        string_keywords = ["渠道", "省份", "性别", "会员", "品类", "品牌", "类型", "等级", "节假日"]
        
        numeric_cols = []
        string_cols = []
        
        for col_name in df.columns:
            if col_name in exclude_cols:
                continue
            
            current_dtype = dict(df.dtypes).get(col_name)
            
            if current_dtype in ["int", "bigint", "double", "float"]:
                # 只选择与预测目标相关的数值特征
                if any(keyword in col_name for keyword in numeric_feature_keywords):
                    numeric_cols.append(col_name)
            elif current_dtype == "string":
                # 只选择业务维度相关的分类特征
                if any(keyword in col_name for keyword in string_keywords):
                    string_cols.append(col_name)
            else:
                try:
                    df = df.withColumn(col_name, col(col_name).cast("string"))
                    if any(keyword in col_name for keyword in string_keywords):
                        string_cols.append(col_name)
                except:
                    pass
        
        print(f"识别到数值特征: {len(numeric_cols)}个")
        print(f"识别到字符串特征: {len(string_cols)}个")
        
        if len(numeric_cols) < 1 and len(string_cols) < 1:
            print("警告: 没有足够的特征列进行模型训练，跳过模型训练")
            return None
        
        numeric_cols = numeric_cols[:15]
        string_cols = string_cols[:10]
        
        df_model = df.select(numeric_cols + string_cols + [target_col])
        
        for col_name in numeric_cols + [target_col]:
            if col_name in df_model.columns:
                df_model = self.convert_to_numeric(df_model, col_name)
        
        df_model = df_model.na.drop(subset=[target_col])
        for col_name in numeric_cols:
            if col_name in df_model.columns:
                df_model = df_model.filter(col(col_name).isNotNull())
        
        # 使用toPandas检查数据量，避免count()触发worker连接
        try:
            sample_pd = df_model.limit(100).toPandas()
            if len(sample_pd) < 10:
                print(f"警告: 数据量不足，跳过模型训练")
                return None
            print(f"训练数据准备完成，开始训练模型...")
        except:
            print("警告: 数据检查失败，跳过模型训练")
            return None
        
        # 过滤掉唯一值过多的分类特征（超过1000个唯一值的特征不适合作为分类特征）
        indexers = []
        indexed_cols = []
        for col_name in string_cols:
            if col_name in df_model.columns:
                try:
                    # 检查唯一值数量（使用limit避免全量扫描）
                    unique_count_pd = df_model.select(col_name).distinct().limit(1001).toPandas()
                    unique_count = len(unique_count_pd)
                    
                    if unique_count > 1000:
                        print(f"警告: 列 {col_name} 有超过1000个唯一值，跳过作为分类特征")
                        continue
                    
                    indexer = StringIndexer(inputCol=col_name, outputCol=f"{col_name}_indexed", handleInvalid="skip")
                    indexers.append(indexer)
                    indexed_cols.append(f"{col_name}_indexed")
                except Exception as e:
                    print(f"警告: 处理列 {col_name} 失败: {e}")
                    pass
        
        all_feature_cols = numeric_cols + indexed_cols
        
        if len(all_feature_cols) < 2:
            if len(numeric_cols) >= 2:
                all_feature_cols = numeric_cols[:10]
                indexers = []
            else:
                print("警告: 有效特征列不足，跳过模型训练")
                return None
        
        try:
            assembler = VectorAssembler(inputCols=all_feature_cols, outputCol="features", handleInvalid="skip")
            # 优化模型参数以提高R²值（目标>0.8）
            rf = RandomForestRegressor(
                featuresCol="features", 
                labelCol=target_col, 
                numTrees=100,  # 增加树的数量以提高模型性能
                maxDepth=15,  # 增加深度以捕获更复杂的模式
                maxBins=5000,  # 增加maxBins以支持更多分类值
                minInstancesPerNode=3,  # 减少最小样本数，允许更细粒度的分割
                subsamplingRate=0.8,  # 每棵树使用的样本比例
                featureSubsetStrategy="sqrt",  # 特征子集策略：sqrt适合大多数情况
                minInfoGain=0.0,  # 最小信息增益，允许更细的分割
                seed=42
            )
            
            if indexers:
                pipeline = Pipeline(stages=indexers + [assembler, rf])
            else:
                pipeline = Pipeline(stages=[assembler, rf])
            
            train_df, test_df = df_model.randomSplit([0.8, 0.2], seed=42)
            # 使用limit检查数据量，避免count()触发worker连接
            try:
                train_sample = train_df.limit(10).toPandas()
                test_sample = test_df.limit(10).toPandas()
                if len(train_sample) < 5:
                    print("警告: 训练集数据量不足，跳过模型训练")
                    return None
                print(f"数据分割完成，开始训练模型...")
            except:
                print("警告: 数据分割检查失败，跳过模型训练")
                return None
            
            print("开始训练模型...")
            model = pipeline.fit(train_df)
            print("模型训练完成")
            
            print("进行预测...")
            predictions = model.transform(test_df)
            
            # 计算多个评估指标
            rmse_evaluator = RegressionEvaluator(labelCol=target_col, predictionCol="prediction", metricName="rmse")
            mae_evaluator = RegressionEvaluator(labelCol=target_col, predictionCol="prediction", metricName="mae")
            r2_evaluator = RegressionEvaluator(labelCol=target_col, predictionCol="prediction", metricName="r2")
            
            rmse = rmse_evaluator.evaluate(predictions)
            mae = mae_evaluator.evaluate(predictions)
            r2 = r2_evaluator.evaluate(predictions)
            
            print(f"模型评估指标:")
            print(f"  RMSE (均方根误差): {rmse:.2f}")
            print(f"  MAE (平均绝对误差): {mae:.2f}")
            print(f"  R² (决定系数): {r2:.4f}")
            
            predictions_pd = predictions.select("prediction", target_col).toPandas()
            predictions_pd.columns = ['predicted_value', 'actual_value']
            
            predictions_pd = predictions_pd.dropna()
            if len(predictions_pd) == 0:
                print("警告: 预测结果为空")
                return None
            
            # 计算相对误差百分比
            predictions_pd['relative_error'] = (predictions_pd['predicted_value'] - predictions_pd['actual_value']).abs() / (predictions_pd['actual_value'] + 1e-6) * 100
            
            predictions_pd['prediction_date'] = datetime.now().strftime("%Y-%m-%d")
            predictions_pd['error'] = (predictions_pd['predicted_value'] - predictions_pd['actual_value']).abs()
            predictions_pd['model_type'] = 'random_forest'
            predictions_pd['target_type'] = target_name
            
            # 重命名列以匹配数据库表结构
            predictions_pd = predictions_pd.rename(columns={
                'predicted_value': 'predicted_sales',
                'actual_value': 'actual_sales'
            })
            # 确保 relative_error 列存在
            if 'relative_error' not in predictions_pd.columns:
                predictions_pd['relative_error'] = 0.0
            
            # 选择要保存的列（确保 relative_error 包含在内）
            predictions_pd = predictions_pd[['prediction_date', 'predicted_sales', 'actual_sales', 'error', 'relative_error', 'model_type']]
            
            self.save_to_mysql("prediction_result", predictions_pd)
            print(f"✓ 预测结果已保存: {len(predictions_pd)} 条记录")
            
            feature_importance = []
            try:
                rf_model = model.stages[-1]
                if hasattr(rf_model, 'featureImportances'):
                    importances = rf_model.featureImportances.toArray()
                    assembler_model = model.stages[-2]
                    feature_names = assembler_model.getInputCols()
                    
                    for i, importance_value in enumerate(importances):
                        if i < len(feature_names):
                            feature_importance.append({
                                "feature_name": feature_names[i],
                                "importance": float(importance_value),
                                "rank": i + 1,
                                "model_type": "random_forest"
                            })
            except:
                pass
            
            if feature_importance:
                feature_importance_pd = pd.DataFrame(feature_importance)
                feature_importance_pd = feature_importance_pd.sort_values(by='importance', ascending=False)
                feature_importance_pd['rank'] = range(1, len(feature_importance_pd) + 1)
                self.save_to_mysql("feature_importance", feature_importance_pd)
                print(f"✓ 特征重要性已保存: {len(feature_importance_pd)} 条记录")
            else:
                print("警告: 未能提取特征重要性")
            
            # 保存模型评估指标到数据库
            try:
                avg_relative_error = predictions_pd['relative_error'].mean() if 'relative_error' in predictions_pd.columns else 0.0
                evaluation_data = pd.DataFrame([{
                    'model_type': 'random_forest',
                    'target_type': target_name,
                    'rmse': float(rmse),
                    'mae': float(mae),
                    'r2': float(r2),
                    'avg_relative_error': float(avg_relative_error),
                    'sample_count': len(predictions_pd),
                    'evaluation_date': datetime.now().strftime("%Y-%m-%d")
                }])
                
                # 确保表存在（再次检查）
                conn = mysql.connector.connect(**self.mysql_config, database=self.database)
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT 1 FROM model_evaluation LIMIT 1")
                    cursor.fetchall()
                except mysql.connector.Error as e:
                    if e.errno == 1146:  # Table doesn't exist
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS model_evaluation (
                                id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                                model_type VARCHAR(50) NOT NULL DEFAULT 'random_forest' COMMENT '模型类型',
                                target_type VARCHAR(100) COMMENT '预测目标类型',
                                rmse DECIMAL(15, 4) COMMENT 'RMSE (均方根误差)',
                                mae DECIMAL(15, 4) COMMENT 'MAE (平均绝对误差)',
                                r2 DECIMAL(10, 6) COMMENT 'R² (决定系数)',
                                avg_relative_error DECIMAL(10, 4) COMMENT '平均相对误差百分比',
                                sample_count INT COMMENT '样本数量',
                                evaluation_date DATE NOT NULL COMMENT '评估日期',
                                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                                INDEX idx_model_type (model_type),
                                INDEX idx_evaluation_date (evaluation_date)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模型评估指标表';
                        """)
                        conn.commit()
                
                # 先删除同类型模型的旧评估指标（保留最新的）
                cursor.execute("""
                    DELETE FROM model_evaluation 
                    WHERE model_type = 'random_forest' 
                    AND (target_type = %s OR target_type IS NULL)
                """, (target_name,))
                conn.commit()
                cursor.close()
                conn.close()
                
                # 保存新的评估指标（不清空表，因为我们已经在上面删除了旧记录）
                self.save_to_mysql("model_evaluation", evaluation_data, clear_table=False)
                print(f"✓ 模型评估指标已保存: RMSE={rmse:.2f}, MAE={mae:.2f}, R²={r2:.4f}")
                if r2 < 0.8:
                    print(f"  提示: R²值({r2:.4f})低于0.8，可能需要进一步优化模型参数或特征工程")
                else:
                    print(f"  ✓ R²值({r2:.4f})已达到目标(>0.8)")
            except Exception as e:
                print(f"警告: 保存模型评估指标失败: {e}")
                import traceback
                traceback.print_exc()
            
            return {
                "predictions": predictions_pd,
                "feature_importance": feature_importance,
                "rmse": rmse,
                "mae": mae,
                "r2": r2
            }
            
        except Exception as e:
            print(f"随机森林模型训练或预测失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run_analysis(self):
        """执行完整的数据分析流程"""
        print("=" * 60)
        print("开始数据分析流程（从MySQL读取，结果保存到MySQL）")
        print("=" * 60)
        
        df = self.load_data_from_mysql()
        if df is None:
            print("无法加载数据，分析终止")
            return None
        
        # 避免调用count()触发worker连接
        print(f"\n数据概览: {len(df.columns)} 列")
        
        self.analysis_1_sales_trend(df)
        self.analysis_2_region(df)
        self.analysis_3_product(df)
        self.analysis_4_user_profile(df)
        self.analysis_5_promotion(df)
        self.analysis_6_random_forest(df)
        
        print("\n" + "=" * 60)
        print("数据分析完成，所有结果已保存到MySQL数据库")
        print("=" * 60)
        print("分析结果表:")
        print("  1. sales_summary - 销售趋势分析（时间维度）")
        print("  2. region_analysis - 地域分析（地区维度）")
        print("  3. product_analysis - 产品分析（产品维度）")
        print("  4. user_profile - 用户画像分析（用户维度）")
        print("  5. promotion_analysis - 促销效果分析（促销维度）")
        print("  6. prediction_result - 随机森林预测结果")
        print("  7. feature_importance - 特征重要性")
        print("=" * 60)


if __name__ == "__main__":
    analyzer = DataAnalysisToMySQL()
    analyzer.run_analysis()
