package org.com.smarthome.mapper;

import org.com.smarthome.entity.PromotionAnalysis;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface PromotionAnalysisMapper extends BaseMapper<PromotionAnalysis> {
    
    @Select("SELECT * FROM promotion_analysis ORDER BY total_sales DESC")
    List<PromotionAnalysis> getAllPromotions();
}



