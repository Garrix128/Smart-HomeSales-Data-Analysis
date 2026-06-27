package org.com.smarthome.mapper;

import org.com.smarthome.entity.ProductAnalysis;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface ProductAnalysisMapper extends BaseMapper<ProductAnalysis> {
    
    @Select("SELECT category, SUM(total_sales) as total_sales, SUM(sales_volume) as sales_volume " +
            "FROM product_analysis GROUP BY category ORDER BY total_sales DESC")
    List<Map<String, Object>> getCategoryStatistics();
    
    @Select("SELECT brand, SUM(total_sales) as total_sales " +
            "FROM product_analysis GROUP BY brand ORDER BY total_sales DESC LIMIT 10")
    List<Map<String, Object>> getTopBrands();
}



