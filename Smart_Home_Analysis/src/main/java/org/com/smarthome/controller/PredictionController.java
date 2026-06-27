package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.entity.FeatureImportance;
import org.com.smarthome.entity.PredictionResult;
import org.com.smarthome.entity.ModelEvaluation;
import org.com.smarthome.service.PredictionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 预测结果Controller
 */
@RestController
@RequestMapping("/api/prediction")
@CrossOrigin
public class PredictionController {
    
    @Autowired
    private PredictionService predictionService;
    
    /**
     * 获取随机森林预测结果
     */
    @GetMapping("/random-forest")
    public Result<Map<String, Object>> getRandomForestResult() {
        try {
            List<PredictionResult> predictions = predictionService.getRecentPredictions();
            List<FeatureImportance> features = predictionService.getFeatureImportance();
            
            // 从数据库读取评估指标（优先使用Python分析计算的值）
            Map<String, Object> metrics = new HashMap<>();
            ModelEvaluation evaluation = predictionService.getLatestEvaluation();
            
            if (evaluation != null) {
                // 使用数据库中的评估指标
                if (evaluation.getRmse() != null) {
                    metrics.put("rmse", evaluation.getRmse().doubleValue());
                }
                if (evaluation.getMae() != null) {
                    metrics.put("mae", evaluation.getMae().doubleValue());
                }
                if (evaluation.getR2() != null) {
                    metrics.put("r2", evaluation.getR2().doubleValue());
                }
                if (evaluation.getAvgRelativeError() != null) {
                    metrics.put("avgRelativeError", evaluation.getAvgRelativeError().doubleValue());
                }
                if (evaluation.getSampleCount() != null) {
                    metrics.put("sampleCount", evaluation.getSampleCount());
                }
                if (evaluation.getTargetType() != null) {
                    metrics.put("targetType", evaluation.getTargetType());
                }
            }
            
            // 如果数据库中没有评估指标，则从预测结果计算（作为后备方案）
            if (metrics.isEmpty() && predictions != null && !predictions.isEmpty()) {
                double sumSquaredError = 0;
                double sumAbsoluteError = 0;
                double sumRelativeError = 0;
                double sumActual = 0;
                int count = 0;
                
                for (PredictionResult pred : predictions) {
                    if (pred.getActualSales() != null && pred.getPredictedSales() != null) {
                        double actual = pred.getActualSales().doubleValue();
                        double predicted = pred.getPredictedSales().doubleValue();
                        double error = Math.abs(predicted - actual);
                        
                        sumSquaredError += error * error;
                        sumAbsoluteError += error;
                        sumActual += actual;
                        if (pred.getRelativeError() != null) {
                            sumRelativeError += pred.getRelativeError().doubleValue();
                        }
                        count++;
                    }
                }
                
                if (count > 0) {
                    metrics.put("rmse", Math.sqrt(sumSquaredError / count));
                    metrics.put("mae", sumAbsoluteError / count);
                    metrics.put("avgRelativeError", sumRelativeError / count);
                    metrics.put("sampleCount", count);
                    
                    // 计算R²
                    double actualMean = sumActual / count;
                    double ssRes = sumSquaredError;
                    double ssTot = 0;
                    for (PredictionResult pred : predictions) {
                        if (pred.getActualSales() != null) {
                            double diff = pred.getActualSales().doubleValue() - actualMean;
                            ssTot += diff * diff;
                        }
                    }
                    metrics.put("r2", ssTot > 0 ? 1 - (ssRes / ssTot) : 0);
                }
            }
            
            Map<String, Object> result = new HashMap<>();
            result.put("predictions", predictions);
            result.put("featureImportance", features);
            result.put("metrics", metrics);
            
            return Result.success(result);
        } catch (Exception e) {
            return Result.error("获取预测结果失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取特征重要性
     */
    @GetMapping("/features")
    public Result<List<FeatureImportance>> getFeatureImportance() {
        try {
            List<FeatureImportance> data = predictionService.getFeatureImportance();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取特征重要性失败: " + e.getMessage());
        }
    }
}

