"""
步骤2: 清洗合并后的数据上传
从CSV文件读取合并后的数据 -> 上传到MySQL的merged_data表
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import sys


class DataUpload:
    def __init__(self):
        self.mysql_config = {
            'host': '192.168.15.135',
            'port': 3306,
            'user': 'root',
            'password': 'YourNewPassword123!'
        }
        self.database = 'smart_home'
        self.init_database()
    
    def init_database(self):
        """初始化数据库（只创建数据库，不创建表）"""
        print("=" * 60)
        print("初始化MySQL数据库...")
        print("=" * 60)
        
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE {self.database}")
            
            print("✓ 数据库初始化完成")
            print("注意: merged_data表将根据CSV文件的列动态创建")
            
            conn.commit()
            
        except Error as e:
            print(f"数据库初始化失败: {e}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def create_table_from_csv(self, df, cursor):
        """根据DataFrame的列动态创建表"""
        print("\n根据CSV列动态创建merged_data表...")
        
        cursor.execute("DROP TABLE IF EXISTS merged_data")
        print("已删除旧的merged_data表（如果存在）")
        
        columns = df.columns.tolist()
        
        create_table_sql = """
            CREATE TABLE merged_data (
                id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
        """
        
        for col in columns:
            if col.lower() == 'id' or col.lower() == 'create_time':
                continue
            
            col_escaped = col.replace('`', '``').replace("'", "''")
            create_table_sql += f",\n                `{col_escaped}` TEXT COMMENT '{col_escaped}'"
        
        create_table_sql += "\n            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='合并后的清洗数据表'"
        
        cursor.execute(create_table_sql)
        print(f"✓ 已创建merged_data表，包含 {len(columns)} 个数据列")
        
        create_index_sql = []
        if '订单编号' in columns:
            create_index_sql.append("CREATE INDEX idx_订单编号 ON merged_data (`订单编号`(50))")
        if '订单日期' in columns:
            create_index_sql.append("CREATE INDEX idx_订单日期 ON merged_data (`订单日期`)")
        
        for index_sql in create_index_sql:
            try:
                cursor.execute(index_sql)
                print(f"✓ 已创建索引: {index_sql.split('ON')[0].replace('CREATE INDEX', '').strip()}")
            except Exception as e:
                print(f"警告: 创建索引失败（可能列不存在）: {e}")
    
    def upload_merged_data(self, csv_path="output/cleaned_data/merged_data.csv"):
        """上传合并后的数据到MySQL"""
        print("\n" + "=" * 60)
        print("上传合并后的数据到MySQL...")
        print("=" * 60)
        
        if not os.path.exists(csv_path):
            print(f"错误: CSV文件不存在: {csv_path}")
            print("请先运行 01_数据清洗.py")
            return False
        
        conn = None
        cursor = None
        
        try:
            print(f"读取CSV文件: {csv_path}")
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
            print(f"读取成功: {len(df)} 行数据, {len(df.columns)} 列")
            
            conn = mysql.connector.connect(**self.mysql_config, database=self.database)
            cursor = conn.cursor()
            
            self.create_table_from_csv(df, cursor)
            conn.commit()
            
            columns = df.columns.tolist()
            placeholders = ', '.join(['%s'] * len(columns))
            column_names = ', '.join([f"`{col.replace('`', '``')}`" for col in columns])
            
            insert_sql = f"""
                INSERT INTO merged_data ({column_names})
                VALUES ({placeholders})
            """
            
            batch_size = 1000
            total_rows = len(df)
            inserted_rows = 0
            
            print(f"\n开始插入数据（批量大小: {batch_size}）...")
            
            for i in range(0, total_rows, batch_size):
                batch_df = df.iloc[i:i+batch_size]
                batch_data = []
                
                for _, row in batch_df.iterrows():
                    row_data = []
                    for col in columns:
                        value = row[col]
                        if pd.isna(value):
                            row_data.append(None)
                        elif isinstance(value, (int, float)):
                            if isinstance(value, float):
                                row_data.append(float(value))
                            else:
                                row_data.append(int(value))
                        else:
                            row_data.append(str(value))
                    batch_data.append(tuple(row_data))
                
                cursor.executemany(insert_sql, batch_data)
                inserted_rows += len(batch_data)
                
                if (i + batch_size) % 5000 == 0 or inserted_rows == total_rows:
                    print(f"已插入 {inserted_rows}/{total_rows} 行数据 ({inserted_rows*100//total_rows}%)...")
            
            conn.commit()
            print(f"\n✓ 数据上传成功: {inserted_rows} 条记录已保存到merged_data表")
            
            cursor.execute("SELECT COUNT(*) FROM merged_data")
            count = cursor.fetchone()[0]
            print(f"✓ 验证: merged_data表中现有 {count} 条记录")
            
            return True
            
        except Exception as e:
            print(f"上传数据失败: {e}")
            import traceback
            traceback.print_exc()
            if conn and conn.is_connected():
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    def run_upload(self, csv_path="output/cleaned_data/merged_data.csv"):
        """执行完整的上传流程"""
        success = self.upload_merged_data(csv_path)
        
        if success:
            print("\n" + "=" * 60)
            print("步骤2完成: 数据上传成功")
            print("=" * 60)
            print("下一步: 运行 03_数据分析.py 对MySQL中的数据进行分析")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("步骤2失败: 数据上传失败")
            print("=" * 60)
        
        return success


def main():
    print("=" * 60)
    print("步骤2: 清洗合并后的数据上传")
    print("=" * 60)
    print("功能: 从CSV读取 -> 上传到MySQL的merged_data表")
    print("输入: output/cleaned_data/merged_data.csv")
    print("输出: MySQL数据库 smart_home.merged_data")
    print("=" * 60)
    
    try:
        uploader = DataUpload()
        success = uploader.run_upload()
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n步骤2执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
