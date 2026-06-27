package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.service.AnalysisResultService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * 产品分析Controller
 */
@RestController
@RequestMapping("/api/product")
@CrossOrigin
public class ProductAnalysisController {
    
    @Autowired
    private AnalysisResultService analysisResultService;
    
    /**
     * 获取产品品类统计
     */
    @GetMapping("/category")
    public Result<List<Map<String, Object>>> getCategoryStatistics() {
        try {
            List<Map<String, Object>> data = analysisResultService.getCategoryStatistics();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取品类统计失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取热门品牌
     */
    @GetMapping("/brands")
    public Result<List<Map<String, Object>>> getTopBrands() {
        try {
            List<Map<String, Object>> data = analysisResultService.getTopBrands();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取品牌数据失败: " + e.getMessage());
        }
    }
}



