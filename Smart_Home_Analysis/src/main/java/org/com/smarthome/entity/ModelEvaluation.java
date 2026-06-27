package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 模型评估指标表
 */
@Data
@TableName("model_evaluation")
public class ModelEvaluation {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String modelType;
    private String targetType;
    private BigDecimal rmse;
    private BigDecimal mae;
    private BigDecimal r2;
    private BigDecimal avgRelativeError;
    private Integer sampleCount;
    private String evaluationDate;
    private Date createTime;
    private Date updateTime;
}


