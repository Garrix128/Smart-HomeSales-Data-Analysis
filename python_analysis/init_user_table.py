"""
初始化用户表和管理员账户
在数据分析之前执行，确保用户表存在并创建管理员账户
"""
import mysql.connector
from mysql.connector import Error
import sys


class InitUserTable:
    def __init__(self):
        self.mysql_config = {
            'host': '192.168.15.135',
            'port': 3306,
            'user': 'root',
            'password': 'YourNewPassword123!'
        }
        self.database = 'smart_home'
    
    def init_user_table(self):
        """创建用户表"""
        print("=" * 60)
        print("初始化用户表...")
        print("=" * 60)
        
        conn = None
        cursor = None
        
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
            
            conn.commit()
            print("✓ 用户表创建成功")
            
        except Error as e:
            print(f"创建用户表失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    def create_admin_user(self):
        """创建管理员账户"""
        print("\n创建管理员账户...")
        
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**self.mysql_config, database=self.database)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM sys_user WHERE username = 'admin'")
            admin_exists = cursor.fetchone()[0] > 0
            
            if admin_exists:
                print("✓ 管理员账户已存在")
            else:
                import hashlib
                admin_password = hashlib.md5('admin'.encode('utf-8')).hexdigest()
                
                insert_sql = """
                    INSERT INTO sys_user (username, password, email, role, status, real_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(insert_sql, (
                    'admin',
                    admin_password,
                    'admin@smarthome.com',
                    'admin',
                    1,
                    '系统管理员'
                ))
                
                conn.commit()
                print("✓ 管理员账户创建成功")
                print("  用户名: admin")
                print("  密码: admin")
            
        except Error as e:
            print(f"创建管理员账户失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    def run(self):
        """执行完整的初始化流程"""
        try:
            self.init_user_table()
            self.create_admin_user()
            
            print("\n" + "=" * 60)
            print("用户表和管理员账户初始化完成")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n初始化失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    print("=" * 60)
    print("初始化用户表和管理员账户")
    print("=" * 60)
    
    init = InitUserTable()
    success = init.run()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()



