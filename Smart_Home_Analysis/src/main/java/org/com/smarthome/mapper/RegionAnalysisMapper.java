package org.com.smarthome.mapper;

import org.com.smarthome.entity.RegionAnalysis;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface RegionAnalysisMapper extends BaseMapper<RegionAnalysis> {
    
    @Select("SELECT * FROM region_analysis ORDER BY total_sales DESC")
    List<RegionAnalysis> getAllRegions();
}

