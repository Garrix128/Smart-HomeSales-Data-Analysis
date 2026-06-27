package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.entity.*;
import org.com.smarthome.service.DataManageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

/**
 * 数据管理Controller
 */
@RestController
@RequestMapping("/api/data/manage")
@CrossOrigin
public class DataManageController {
    
    @Autowired
    private DataManageService dataManageService;
    
    // SalesSummary CRUD
    @GetMapping("/sales")
    public Result<List<SalesSummary>> getAllSalesSummary() {
        try {
            List<SalesSummary> data = dataManageService.getAllSalesSummary();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @GetMapping("/sales/{id}")
    public Result<SalesSummary> getSalesSummaryById(@PathVariable Long id) {
        try {
            SalesSummary data = dataManageService.getSalesSummaryById(id);
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/sales")
    public Result<Boolean> saveSalesSummary(@RequestBody SalesSummary salesSummary) {
        try {
            boolean success = dataManageService.saveSalesSummary(salesSummary);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/sales")
    public Result<Boolean> updateSalesSummary(@RequestBody SalesSummary salesSummary) {
        try {
            boolean success = dataManageService.updateSalesSummary(salesSummary);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/sales/{id}")
    public Result<Boolean> deleteSalesSummary(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deleteSalesSummary(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    // RegionAnalysis CRUD
    @GetMapping("/region")
    public Result<List<RegionAnalysis>> getAllRegionAnalysis() {
        try {
            List<RegionAnalysis> data = dataManageService.getAllRegionAnalysis();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/region")
    public Result<Boolean> saveRegionAnalysis(@RequestBody RegionAnalysis regionAnalysis) {
        try {
            boolean success = dataManageService.saveRegionAnalysis(regionAnalysis);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/region")
    public Result<Boolean> updateRegionAnalysis(@RequestBody RegionAnalysis regionAnalysis) {
        try {
            boolean success = dataManageService.updateRegionAnalysis(regionAnalysis);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/region/{id}")
    public Result<Boolean> deleteRegionAnalysis(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deleteRegionAnalysis(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    // ProductAnalysis CRUD
    @GetMapping("/product")
    public Result<List<ProductAnalysis>> getAllProductAnalysis() {
        try {
            List<ProductAnalysis> data = dataManageService.getAllProductAnalysis();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/product")
    public Result<Boolean> saveProductAnalysis(@RequestBody ProductAnalysis productAnalysis) {
        try {
            boolean success = dataManageService.saveProductAnalysis(productAnalysis);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/product")
    public Result<Boolean> updateProductAnalysis(@RequestBody ProductAnalysis productAnalysis) {
        try {
            boolean success = dataManageService.updateProductAnalysis(productAnalysis);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/product/{id}")
    public Result<Boolean> deleteProductAnalysis(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deleteProductAnalysis(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    // UserBehavior CRUD
    @GetMapping("/user-behavior")
    public Result<List<UserBehavior>> getAllUserBehavior() {
        try {
            List<UserBehavior> data = dataManageService.getAllUserBehavior();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/user-behavior")
    public Result<Boolean> saveUserBehavior(@RequestBody UserBehavior userBehavior) {
        try {
            boolean success = dataManageService.saveUserBehavior(userBehavior);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/user-behavior")
    public Result<Boolean> updateUserBehavior(@RequestBody UserBehavior userBehavior) {
        try {
            boolean success = dataManageService.updateUserBehavior(userBehavior);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/user-behavior/{id}")
    public Result<Boolean> deleteUserBehavior(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deleteUserBehavior(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    // PredictionResult CRUD
    @GetMapping("/prediction")
    public Result<List<PredictionResult>> getAllPredictionResult() {
        try {
            List<PredictionResult> data = dataManageService.getAllPredictionResult();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/prediction")
    public Result<Boolean> savePredictionResult(@RequestBody PredictionResult predictionResult) {
        try {
            boolean success = dataManageService.savePredictionResult(predictionResult);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/prediction")
    public Result<Boolean> updatePredictionResult(@RequestBody PredictionResult predictionResult) {
        try {
            boolean success = dataManageService.updatePredictionResult(predictionResult);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/prediction/{id}")
    public Result<Boolean> deletePredictionResult(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deletePredictionResult(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    // FeatureImportance CRUD
    @GetMapping("/feature-importance")
    public Result<List<FeatureImportance>> getAllFeatureImportance() {
        try {
            List<FeatureImportance> data = dataManageService.getAllFeatureImportance();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/feature-importance")
    public Result<Boolean> saveFeatureImportance(@RequestBody FeatureImportance featureImportance) {
        try {
            boolean success = dataManageService.saveFeatureImportance(featureImportance);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/feature-importance")
    public Result<Boolean> updateFeatureImportance(@RequestBody FeatureImportance featureImportance) {
        try {
            boolean success = dataManageService.updateFeatureImportance(featureImportance);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/feature-importance/{id}")
    public Result<Boolean> deleteFeatureImportance(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deleteFeatureImportance(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    // MergedData CRUD - 清洗合并后的数据
    @GetMapping("/merged-data")
    public Result<List<MergedData>> getAllMergedData() {
        try {
            List<MergedData> data = dataManageService.getAllMergedData();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @GetMapping("/merged-data/page")
    public Result<com.baomidou.mybatisplus.extension.plugins.pagination.Page<MergedData>> getMergedDataPage(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer size,
            @RequestParam(required = false) String search) {
        try {
            com.baomidou.mybatisplus.extension.plugins.pagination.Page<MergedData> result = 
                dataManageService.getMergedDataPage(page, size, search);
            return Result.success(result);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @GetMapping("/merged-data/{id}")
    public Result<MergedData> getMergedDataById(@PathVariable Long id) {
        try {
            MergedData data = dataManageService.getMergedDataById(id);
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    @PostMapping("/merged-data")
    public Result<Boolean> saveMergedData(@RequestBody MergedData mergedData) {
        try {
            boolean success = dataManageService.saveMergedData(mergedData);
            return success ? Result.success("保存成功", true) : Result.error("保存失败");
        } catch (Exception e) {
            return Result.error("保存失败: " + e.getMessage());
        }
    }
    
    @PutMapping("/merged-data")
    public Result<Boolean> updateMergedData(@RequestBody MergedData mergedData) {
        try {
            boolean success = dataManageService.updateMergedData(mergedData);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    @DeleteMapping("/merged-data/{id}")
    public Result<Boolean> deleteMergedData(@PathVariable Long id) {
        try {
            boolean success = dataManageService.deleteMergedData(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
}

