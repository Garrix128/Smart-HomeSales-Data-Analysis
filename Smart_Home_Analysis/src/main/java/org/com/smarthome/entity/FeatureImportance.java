package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.util.Date;

/**
 * 特征重要性表
 */
@Data
@TableName("feature_importance")
public class FeatureImportance {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String featureName;
    private Double importance;
    private Integer rank;
    private String modelType;
    private Date createTime;
}



