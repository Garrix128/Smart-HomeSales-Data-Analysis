package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 销售汇总表
 */
@Data
@TableName("sales_summary")
public class SalesSummary {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private Date salesDate;
    private BigDecimal totalSales;
    private Integer orderCount;
    private BigDecimal avgOrderAmount;
    private Date createTime;
    private Date updateTime;
}



