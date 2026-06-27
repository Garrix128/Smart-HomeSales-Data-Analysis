package org.com.smarthome.service;

import org.com.smarthome.entity.RegionAnalysis;
import org.com.smarthome.entity.ProductAnalysis;
import org.com.smarthome.entity.PromotionAnalysis;
import org.com.smarthome.mapper.RegionAnalysisMapper;
import org.com.smarthome.mapper.ProductAnalysisMapper;
import org.com.smarthome.mapper.PromotionAnalysisMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;

@Service
public class AnalysisResultService {
    
    @Autowired
    private RegionAnalysisMapper regionAnalysisMapper;
    
    @Autowired
    private ProductAnalysisMapper productAnalysisMapper;
    
    @Autowired
    private PromotionAnalysisMapper promotionAnalysisMapper;
    
    public List<RegionAnalysis> getRegionAnalysis() {
        return regionAnalysisMapper.getAllRegions();
    }
    
    public List<Map<String, Object>> getCategoryStatistics() {
        return productAnalysisMapper.getCategoryStatistics();
    }
    
    public List<Map<String, Object>> getTopBrands() {
        return productAnalysisMapper.getTopBrands();
    }
    
    public List<PromotionAnalysis> getPromotionAnalysis() {
        return promotionAnalysisMapper.getAllPromotions();
    }
}

