package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

@Data
@TableName("promotion_analysis")
public class PromotionAnalysis {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String promotionType;
    private BigDecimal avgDiscountRate;
    private BigDecimal totalSales;
    private Integer orderCount;
    private BigDecimal avgOrderAmount;
    private Date createTime;
    private Date updateTime;
}



