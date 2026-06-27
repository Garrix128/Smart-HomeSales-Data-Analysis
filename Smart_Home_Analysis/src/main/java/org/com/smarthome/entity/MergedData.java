package org.com.smarthome.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.util.Date;

@Data
@TableName(value = "merged_data", keepGlobalPrefix = false)
public class MergedData {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("订单编号")
    private String 订单编号;
    
    @TableField("产品型号")
    private String 产品型号;
    
    @TableField("销售渠道")
    private String 销售渠道;
    
    @TableField("用户所在省份")
    private String 用户所在省份;
    
    @TableField("用户性别")
    private String 用户性别;
    
    @TableField("是否会员")
    private String 是否会员;
    
    @TableField("会员等级")
    private String 会员等级;
    
    @TableField("促销类型")
    private String 促销类型;
    
    @TableField("促销折扣率")
    private String 促销折扣率;
    
    @TableField("订单日期")
    private String 订单日期;
    
    @TableField("是否节假日")
    private String 是否节假日;
    
    @TableField("产品品类")
    private String 产品品类;
    
    @TableField("品牌名称")
    private String 品牌名称;
    
    @TableField("销售单价（元）")
    private String 销售单价;
    
    @TableField("销售数量（件）")
    private String 销售数量;
    
    @TableField("订单总金额（元）")
    private String 订单总金额;
    
    @TableField("处理时间")
    private String 处理时间;
    
    @TableField("create_time")
    private Date createTime;
}
