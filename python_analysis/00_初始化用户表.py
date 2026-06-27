"""
步骤0: 初始化用户表和管理员账户
在运行其他步骤之前，先执行此脚本创建用户表和管理员账户
"""
from init_user_table import InitUserTable
import sys


def main():
    print("=" * 60)
    print("步骤0: 初始化用户表和管理员账户")
    print("=" * 60)
    print("功能: 创建sys_user表并插入管理员账户")
    print("管理员账户: admin/admin")
    print("=" * 60)
    
    try:
        init = InitUserTable()
        success = init.run()
        
        if success:
            print("\n" + "=" * 60)
            print("步骤0完成: 用户表和管理员账户初始化成功")
            print("=" * 60)
            print("下一步: 运行 01_数据清洗.py 开始数据清洗")
            print("=" * 60)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n步骤0执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()



