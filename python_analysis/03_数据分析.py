"""
步骤3: 数据分析
从MySQL读取merged_data表的数据 -> 分析 -> 保存分析结果到MySQL
"""
from data_analysis_to_mysql import DataAnalysisToMySQL
import sys


def main():
    print("=" * 60)
    print("步骤3: 数据分析")
    print("=" * 60)
    print("功能: 从MySQL读取merged_data -> 分析 -> 保存结果到MySQL")
    print("输入: MySQL数据库 smart_home.merged_data")
    print("输出: MySQL数据库中的分析结果表")
    print("=" * 60)
    
    try:
        analyzer = DataAnalysisToMySQL()
        analyzer.run_analysis()
        
        print("\n" + "=" * 60)
        print("步骤3完成: 数据分析成功")
        print("=" * 60)
        print("所有分析结果已保存到MySQL数据库:")
        print("  1. sales_summary - 销售趋势分析（时间维度）")
        print("  2. region_analysis - 地域分析（地区维度）")
        print("  3. product_analysis - 产品分析（产品维度）")
        print("  4. user_profile - 用户画像分析（用户维度）")
        print("  5. promotion_analysis - 促销效果分析（促销维度）")
        print("  6. prediction_result - 随机森林预测结果")
        print("  7. feature_importance - 特征重要性")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n步骤3执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

