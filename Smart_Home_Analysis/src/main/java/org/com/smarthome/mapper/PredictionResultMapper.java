package org.com.smarthome.mapper;

import org.com.smarthome.entity.PredictionResult;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface PredictionResultMapper extends BaseMapper<PredictionResult> {
    
    @Select("SELECT * FROM prediction_result WHERE model_type = 'random_forest' " +
            "ORDER BY prediction_date DESC LIMIT 30")
    List<PredictionResult> getRecentPredictions();
}



