package org.com.smarthome.service;

import org.com.smarthome.entity.PredictionResult;
import org.com.smarthome.entity.FeatureImportance;
import org.com.smarthome.entity.ModelEvaluation;
import org.com.smarthome.mapper.PredictionResultMapper;
import org.com.smarthome.mapper.FeatureImportanceMapper;
import org.com.smarthome.mapper.ModelEvaluationMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class PredictionService {
    
    @Autowired
    private PredictionResultMapper predictionResultMapper;
    
    @Autowired
    private FeatureImportanceMapper featureImportanceMapper;
    
    @Autowired
    private ModelEvaluationMapper modelEvaluationMapper;
    
    public List<PredictionResult> getRecentPredictions() {
        return predictionResultMapper.getRecentPredictions();
    }
    
    public List<FeatureImportance> getFeatureImportance() {
        return featureImportanceMapper.getTopFeatures();
    }
    
    public ModelEvaluation getLatestEvaluation() {
        return modelEvaluationMapper.getLatestEvaluation();
    }
}

