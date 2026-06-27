"""
步骤1: 数据清洗
读取Excel文件 -> 清洗数据 -> 合并数据 -> 保存为CSV文件
"""
from data_cleaning import DataCleaning
import sys


def main():
    print("=" * 60)
    print("步骤1: 数据清洗")
    print("=" * 60)
    print("功能: 读取Excel -> 清洗 -> 合并 -> 保存CSV")
    print("输出: output/cleaned_data/merged_data.csv")
    print("=" * 60)
    
    try:
        cleaner = DataCleaning()
        cleaner.run_cleaning(
            data_dir="data",
            output_dir="output/cleaned_data"
        )
        
        print("\n" + "=" * 60)
        print("步骤1完成: 数据清洗成功")
        print("=" * 60)
        print("下一步: 运行 02_清洗合并后的数据上传.py 将数据上传到MySQL")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n步骤1执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()



