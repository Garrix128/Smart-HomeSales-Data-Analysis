package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 地域分析表
 */
@Data
@TableName("region_analysis")
public class RegionAnalysis {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String region;
    private BigDecimal totalSales;
    private Integer orderCount;
    private BigDecimal avgOrderAmount;
    private Integer userCount;
    private Date createTime;
    private Date updateTime;
}



