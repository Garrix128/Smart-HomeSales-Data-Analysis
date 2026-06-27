package org.com.smarthome.mapper;

import org.com.smarthome.entity.FeatureImportance;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface FeatureImportanceMapper extends BaseMapper<FeatureImportance> {
    
    @Select("SELECT * FROM feature_importance WHERE model_type = 'random_forest' " +
            "ORDER BY importance DESC LIMIT 20")
    List<FeatureImportance> getTopFeatures();
}



