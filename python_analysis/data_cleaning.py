"""
数据清洗模块
使用PySpark进行数据清洗和预处理
流程：读取Excel -> 清洗 -> 合并 -> 保存到本地CSV
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
import os
from datetime import datetime


class DataCleaning:
    def __init__(self, spark_session=None):
        import os
        import sys
        
        python_path = sys.executable
        os.environ['PYSPARK_PYTHON'] = python_path
        os.environ['PYSPARK_DRIVER_PYTHON'] = python_path
        
        if spark_session is None:
            self.spark = SparkSession.builder \
                .appName("SmartHomeDataCleaning") \
                .master("local") \
                .getOrCreate()
        else:
            self.spark = spark_session
        
        self.spark.sparkContext.setLogLevel("WARN")
    
    def read_excel_files(self, data_dir="data"):
        """读取所有Excel文件"""
        print("=" * 60)
        print("开始读取Excel文件...")
        print("=" * 60)
        
        user_data_path = os.path.join(data_dir, "家居销量用户数据.xlsx")
        brand_path = os.path.join(data_dir, "智能家居品牌.xlsx")
        price_path = os.path.join(data_dir, "智能家居品牌价格.xlsx")
        model_path = os.path.join(data_dir, "智能家居品牌型号.xlsx")
        sales_info_path = os.path.join(data_dir, "智能家居品牌销售信息.xlsx")
        
        user_df_pd = pd.read_excel(user_data_path)
        brand_df_pd = pd.read_excel(brand_path)
        price_df_pd = pd.read_excel(price_path)
        model_df_pd = pd.read_excel(model_path)
        sales_info_df_pd = pd.read_excel(sales_info_path)
        
        print(f"用户数据: {len(user_df_pd)} 行")
        print(f"品牌数据: {len(brand_df_pd)} 行")
        print(f"价格数据: {len(price_df_pd)} 行")
        print(f"型号数据: {len(model_df_pd)} 行")
        print(f"销售信息: {len(sales_info_df_pd)} 行")
        
        user_df = self.spark.createDataFrame(user_df_pd)
        brand_df = self.spark.createDataFrame(brand_df_pd)
        price_df = self.spark.createDataFrame(price_df_pd)
        model_df = self.spark.createDataFrame(model_df_pd)
        sales_info_df = self.spark.createDataFrame(sales_info_df_pd)
        
        return user_df, brand_df, price_df, model_df, sales_info_df
    
    def clean_user_data(self, user_df):
        """清洗用户数据"""
        print("\n清洗用户数据...")
        
        user_df = user_df.dropna(subset=["销售订单编号"])
        
        user_df = user_df.withColumnRenamed("销售订单编号", "订单编号")
        
        date_cols = [c for c in user_df.columns if "日期" in c]
        for col_name in date_cols:
            user_df = user_df.withColumn(
                col_name,
                to_date(col(col_name), "yyyy/MM/dd")
            )
        
        numeric_cols = [c for c in user_df.columns if "折扣" in c or "率" in c]
        for col_name in numeric_cols:
            user_df = user_df.withColumn(
                col_name,
                when(col(col_name).isNull() | (col(col_name) < 0), 0)
                .otherwise(col(col_name))
            )
        
        user_df = user_df.dropDuplicates(["订单编号"])
        
        print(f"清洗后用户数据: {user_df.count()} 行")
        return user_df
    
    def clean_sales_data(self, sales_info_df, price_df, model_df, brand_df):
        """清洗销售数据并关联其他信息"""
        print("\n清洗销售数据...")
        
        sales_info_df = sales_info_df.dropna(subset=["销售订单编号"])
        sales_info_df = sales_info_df.withColumnRenamed("销售订单编号", "订单编号")
        
        date_cols = [c for c in sales_info_df.columns if "日期" in c]
        for col_name in date_cols:
            sales_info_df = sales_info_df.withColumn(
                col_name,
                to_date(col(col_name), "yyyy/MM/dd")
            )
        
        numeric_cols = [c for c in sales_info_df.columns if "单价" in c or "数量" in c or "金额" in c]
        for col_name in numeric_cols:
            sales_info_df = sales_info_df.withColumn(
                col_name,
                when(col(col_name).isNull() | (col(col_name) < 0), 0)
                .otherwise(col(col_name))
            )
        
        if "产品型号" in sales_info_df.columns and "产品型号" in price_df.columns:
            price_df_renamed = price_df.select(
                [col("产品型号").alias("price_产品型号")] +
                [col(c).alias(f"price_{c}") for c in price_df.columns if c != "产品型号"]
            )
            sales_info_df = sales_info_df.join(
                price_df_renamed,
                sales_info_df["产品型号"] == price_df_renamed["price_产品型号"],
                "left"
            ).drop("price_产品型号")
        
        if "产品型号" in sales_info_df.columns and "产品型号" in model_df.columns:
            model_df_renamed = model_df.select(
                [col("产品型号").alias("model_产品型号")] +
                [col(c).alias(f"model_{c}") for c in model_df.columns if c != "产品型号"]
            )
            sales_info_df = sales_info_df.join(
                model_df_renamed,
                sales_info_df["产品型号"] == model_df_renamed["model_产品型号"],
                "left"
            ).drop("model_产品型号")
        
        sales_info_df = sales_info_df.dropDuplicates(["订单编号"])
        
        print(f"清洗后销售数据: {sales_info_df.count()} 行")
        return sales_info_df
    
    def merge_datasets(self, user_df, sales_info_df):
        """合并用户数据和销售数据，自动去除重复列"""
        print("\n合并数据集...")
        print(f"用户数据列数: {len(user_df.columns)}")
        print(f"销售数据列数: {len(sales_info_df.columns)}")
        
        # 找出两个DataFrame中所有重复的列
        user_cols = set(user_df.columns)
        sales_cols = set(sales_info_df.columns)
        common_cols = user_cols & sales_cols
        
        print(f"发现重复列: {common_cols}")
        
        # 为销售数据中的所有重复列添加前缀，避免join后重复
        sales_info_df_renamed = sales_info_df
        for col_name in common_cols:
            if col_name in sales_info_df.columns:
                sales_info_df_renamed = sales_info_df_renamed.withColumnRenamed(
                    col_name, 
                    f"sales_{col_name}"
                )
        
        if common_cols:
            print(f"已重命名销售数据中的重复列: {common_cols}")
        
        # 执行join（使用重命名后的销售数据）
        merged_df = user_df.join(
            sales_info_df_renamed,
            user_df["订单编号"] == sales_info_df_renamed["sales_订单编号"],
            "inner"
        )
        
        # 删除join key的重复列（保留用户数据中的订单编号）
        merged_df = merged_df.drop("sales_订单编号")
        
        # 检查并去除所有重复列（确保每个列名只出现一次）
        final_cols = []
        seen_cols = set()
        
        for col_name in merged_df.columns:
            if col_name not in seen_cols:
                final_cols.append(col_name)
                seen_cols.add(col_name)
            else:
                print(f"警告: 发现重复列名 {col_name}，已跳过")
        
        # 使用select明确指定要保留的列（使用字符串列名，避免歧义）
        merged_df = merged_df.select(*final_cols)
        
        print(f"合并后列数: {len(merged_df.columns)}")
        print(f"合并后列名: {merged_df.columns}")
        
        # 计算销售额
        price_col = None
        quantity_col = None
        for col_name in merged_df.columns:
            if "单价" in col_name and not col_name.startswith("sales_") and not col_name.startswith("price_") and not col_name.startswith("model_"):
                price_col = col_name
            if ("数量" in col_name or "件" in col_name) and not col_name.startswith("sales_") and not col_name.startswith("price_") and not col_name.startswith("model_"):
                quantity_col = col_name
        
        if price_col and quantity_col:
            merged_df = merged_df.withColumn(
                "销售额",
                when(col(price_col).isNotNull() & col(quantity_col).isNotNull(),
                     col(price_col) * col(quantity_col)).otherwise(0)
            )
        else:
            amount_col = None
            for col_name in merged_df.columns:
                if "总金额" in col_name:
                    amount_col = col_name
                    break
            if amount_col:
                merged_df = merged_df.withColumn("销售额", col(amount_col))
            else:
                merged_df = merged_df.withColumn("销售额", lit(0))
        
        merged_df = merged_df.withColumn("处理时间", lit(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        # 删除不需要的重复列
        columns_to_drop = [
            "sales_产品型号",
            "sales_订单日期",
            "price_产品品类",
            "price_品牌名称",
            "price_销售单价（元）",
            "model_产品品类",
            "model_品牌名称",
            "销售额"
        ]
        
        for col_name in columns_to_drop:
            if col_name in merged_df.columns:
                merged_df = merged_df.drop(col_name)
                print(f"已删除列: {col_name}")
        
        print(f"合并后数据: {merged_df.count()} 行")
        print(f"合并后列数: {len(merged_df.columns)}")
        print(f"合并后列名: {merged_df.columns}")
        
        return merged_df
    
    def save_to_local_csv(self, df, local_path):
        """保存数据到本地CSV文件（使用Pandas避免Windows Hadoop问题）"""
        print(f"\n保存数据到本地CSV: {local_path}")
        
        # 确保路径是单个CSV文件
        if not local_path.endswith('.csv'):
            local_path = local_path + '.csv'
        
        dir_path = os.path.dirname(local_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        try:
            # 直接使用Pandas保存，避免Windows上的Hadoop本地库问题
            df_pd = df.toPandas()
            df_pd.to_csv(local_path, index=False, encoding="utf-8-sig")
            print(f"数据已保存到: {os.path.abspath(local_path)}")
        except Exception as e:
            print(f"保存失败: {e}")
            import traceback
            traceback.print_exc()
    
    def run_cleaning(self, data_dir="data", output_dir="output/cleaned_data"):
        """执行完整的数据清洗流程"""
        print("=" * 60)
        print("开始数据清洗流程")
        print("=" * 60)
        
        user_df, brand_df, price_df, model_df, sales_info_df = self.read_excel_files(data_dir)
        
        cleaned_user_df = self.clean_user_data(user_df)
        cleaned_sales_df = self.clean_sales_data(sales_info_df, price_df, model_df, brand_df)
        
        merged_df = self.merge_datasets(cleaned_user_df, cleaned_sales_df)
        
        # 只保存合并后的数据为一个CSV文件
        merged_csv_path = os.path.join(output_dir, "merged_data.csv")
        self.save_to_local_csv(merged_df, merged_csv_path)
        
        print("\n" + "=" * 60)
        print("数据清洗完成，合并数据已保存到单个CSV文件")
        print(f"保存路径: {os.path.abspath(merged_csv_path)}")
        print("=" * 60)
        
        return merged_df
