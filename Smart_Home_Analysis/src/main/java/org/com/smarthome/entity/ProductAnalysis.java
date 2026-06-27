package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 产品分析表
 */
@Data
@TableName("product_analysis")
public class ProductAnalysis {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String category;
    private String brand;
    private BigDecimal totalSales;
    private Integer salesVolume;
    private BigDecimal avgPrice;
    private Date createTime;
    private Date updateTime;
}

