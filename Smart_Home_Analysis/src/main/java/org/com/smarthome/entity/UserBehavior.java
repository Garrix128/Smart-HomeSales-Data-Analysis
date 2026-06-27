package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 用户行为分析表
 */
@Data
@TableName("user_behavior")
public class UserBehavior {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String userId;
    private BigDecimal totalConsumption;
    private Integer orderCount;
    private BigDecimal avgOrderAmount;
    private Date lastPurchaseDate;
    private String memberType;
    private Date createTime;
    private Date updateTime;
}



