package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 模型预测结果表
 */
@Data
@TableName("prediction_result")
public class PredictionResult {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String predictionDate;
    private BigDecimal predictedSales;
    private BigDecimal actualSales;
    private BigDecimal error;
    private BigDecimal relativeError;
    private String modelType;
    private Date createTime;
}

