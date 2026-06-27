package org.com.smarthome.mapper;

import org.com.smarthome.entity.SalesSummary;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface SalesDataMapper extends BaseMapper<SalesSummary> {
    
    @Select("SELECT * FROM sales_summary ORDER BY sales_date DESC LIMIT #{limit}")
    List<SalesSummary> getRecentSalesTrend(Integer limit);
    
    @Select("SELECT DATE_FORMAT(sales_date, '%Y-%m') as month, " +
            "SUM(total_sales) as total_sales, " +
            "SUM(order_count) as order_count " +
            "FROM sales_summary " +
            "GROUP BY DATE_FORMAT(sales_date, '%Y-%m') " +
            "ORDER BY month")
    List<Map<String, Object>> getMonthlyTrend();
}



