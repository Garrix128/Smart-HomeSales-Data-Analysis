package org.com.smarthome.mapper;

import org.com.smarthome.entity.ModelEvaluation;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface ModelEvaluationMapper extends BaseMapper<ModelEvaluation> {
    
    @Select("SELECT * FROM model_evaluation WHERE model_type = 'random_forest' " +
            "ORDER BY evaluation_date DESC, create_time DESC LIMIT 1")
    ModelEvaluation getLatestEvaluation();
}


