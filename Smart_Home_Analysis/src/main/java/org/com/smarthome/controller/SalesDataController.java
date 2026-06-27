package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.service.SalesDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * 销量数据查询Controller
 */
@RestController
@RequestMapping("/api/sales")
@CrossOrigin
public class SalesDataController {
    
    @Autowired
    private SalesDataService salesDataService;
    
    /**
     * 获取销售趋势数据
     */
    @GetMapping("/trend")
    public Result<List<Map<String, Object>>> getSalesTrend(
            @RequestParam(required = false, defaultValue = "30") Integer limit) {
        try {
            List<Map<String, Object>> data = salesDataService.getMonthlyTrend();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取销售趋势数据失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取月度销售趋势
     */
    @GetMapping("/monthly")
    public Result<List<Map<String, Object>>> getMonthlyTrend() {
        try {
            List<Map<String, Object>> data = salesDataService.getMonthlyTrend();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取月度趋势数据失败: " + e.getMessage());
        }
    }
}



