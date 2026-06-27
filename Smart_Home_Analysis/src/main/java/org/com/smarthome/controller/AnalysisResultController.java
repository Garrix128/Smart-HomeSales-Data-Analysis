package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.entity.RegionAnalysis;
import org.com.smarthome.entity.PromotionAnalysis;
import org.com.smarthome.service.AnalysisResultService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 分析结果获取Controller
 */
@RestController
@RequestMapping("/api/analysis")
@CrossOrigin
public class AnalysisResultController {
    
    @Autowired
    private AnalysisResultService analysisResultService;
    
    /**
     * 获取地域分析数据
     */
    @GetMapping("/region")
    public Result<List<RegionAnalysis>> getRegionAnalysis() {
        try {
            List<RegionAnalysis> data = analysisResultService.getRegionAnalysis();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取地域分析数据失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取产品分析数据
     */
    @GetMapping("/product")
    public Result<Map<String, Object>> getProductAnalysis() {
        try {
            Map<String, Object> result = new HashMap<>();
            result.put("category", analysisResultService.getCategoryStatistics());
            result.put("topBrands", analysisResultService.getTopBrands());
            return Result.success(result);
        } catch (Exception e) {
            return Result.error("获取产品分析数据失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取促销效果分析数据
     */
    @GetMapping("/promotion")
    public Result<List<PromotionAnalysis>> getPromotionAnalysis() {
        try {
            List<PromotionAnalysis> data = analysisResultService.getPromotionAnalysis();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取促销效果分析数据失败: " + e.getMessage());
        }
    }
}

