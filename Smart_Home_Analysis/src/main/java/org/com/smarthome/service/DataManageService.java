package org.com.smarthome.service;

import org.com.smarthome.entity.*;
import org.com.smarthome.mapper.SalesDataMapper;
import org.com.smarthome.mapper.RegionAnalysisMapper;
import org.com.smarthome.mapper.ProductAnalysisMapper;
import org.com.smarthome.mapper.UserBehaviorMapper;
import org.com.smarthome.mapper.PredictionResultMapper;
import org.com.smarthome.mapper.FeatureImportanceMapper;
import org.com.smarthome.mapper.MergedDataMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import java.util.List;

@Service
public class DataManageService {
    
    @Autowired
    private SalesDataMapper salesDataMapper;
    
    @Autowired
    private RegionAnalysisMapper regionAnalysisMapper;
    
    @Autowired
    private ProductAnalysisMapper productAnalysisMapper;
    
    @Autowired
    private UserBehaviorMapper userBehaviorMapper;
    
    @Autowired
    private PredictionResultMapper predictionResultMapper;
    
    @Autowired
    private FeatureImportanceMapper featureImportanceMapper;
    
    @Autowired
    private MergedDataMapper mergedDataMapper;
    
    // SalesSummary CRUD
    public List<SalesSummary> getAllSalesSummary() {
        return salesDataMapper.selectList(null);
    }
    
    public SalesSummary getSalesSummaryById(Long id) {
        return salesDataMapper.selectById(id);
    }
    
    public boolean saveSalesSummary(SalesSummary salesSummary) {
        return salesDataMapper.insert(salesSummary) > 0;
    }
    
    public boolean updateSalesSummary(SalesSummary salesSummary) {
        return salesDataMapper.updateById(salesSummary) > 0;
    }
    
    public boolean deleteSalesSummary(Long id) {
        return salesDataMapper.deleteById(id) > 0;
    }
    
    // RegionAnalysis CRUD
    public List<RegionAnalysis> getAllRegionAnalysis() {
        return regionAnalysisMapper.selectList(null);
    }
    
    public boolean saveRegionAnalysis(RegionAnalysis regionAnalysis) {
        return regionAnalysisMapper.insert(regionAnalysis) > 0;
    }
    
    public boolean updateRegionAnalysis(RegionAnalysis regionAnalysis) {
        return regionAnalysisMapper.updateById(regionAnalysis) > 0;
    }
    
    public boolean deleteRegionAnalysis(Long id) {
        return regionAnalysisMapper.deleteById(id) > 0;
    }
    
    // ProductAnalysis CRUD
    public List<ProductAnalysis> getAllProductAnalysis() {
        return productAnalysisMapper.selectList(null);
    }
    
    public ProductAnalysis getProductAnalysisById(Long id) {
        return productAnalysisMapper.selectById(id);
    }
    
    public boolean saveProductAnalysis(ProductAnalysis productAnalysis) {
        return productAnalysisMapper.insert(productAnalysis) > 0;
    }
    
    public boolean updateProductAnalysis(ProductAnalysis productAnalysis) {
        return productAnalysisMapper.updateById(productAnalysis) > 0;
    }
    
    public boolean deleteProductAnalysis(Long id) {
        return productAnalysisMapper.deleteById(id) > 0;
    }
    
    // UserBehavior CRUD
    public List<UserBehavior> getAllUserBehavior() {
        return userBehaviorMapper.selectList(null);
    }
    
    public UserBehavior getUserBehaviorById(Long id) {
        return userBehaviorMapper.selectById(id);
    }
    
    public boolean saveUserBehavior(UserBehavior userBehavior) {
        return userBehaviorMapper.insert(userBehavior) > 0;
    }
    
    public boolean updateUserBehavior(UserBehavior userBehavior) {
        return userBehaviorMapper.updateById(userBehavior) > 0;
    }
    
    public boolean deleteUserBehavior(Long id) {
        return userBehaviorMapper.deleteById(id) > 0;
    }
    
    // PredictionResult CRUD
    public List<PredictionResult> getAllPredictionResult() {
        return predictionResultMapper.selectList(null);
    }
    
    public PredictionResult getPredictionResultById(Long id) {
        return predictionResultMapper.selectById(id);
    }
    
    public boolean savePredictionResult(PredictionResult predictionResult) {
        return predictionResultMapper.insert(predictionResult) > 0;
    }
    
    public boolean updatePredictionResult(PredictionResult predictionResult) {
        return predictionResultMapper.updateById(predictionResult) > 0;
    }
    
    public boolean deletePredictionResult(Long id) {
        return predictionResultMapper.deleteById(id) > 0;
    }
    
    // FeatureImportance CRUD
    public List<FeatureImportance> getAllFeatureImportance() {
        return featureImportanceMapper.selectList(null);
    }
    
    public FeatureImportance getFeatureImportanceById(Long id) {
        return featureImportanceMapper.selectById(id);
    }
    
    public boolean saveFeatureImportance(FeatureImportance featureImportance) {
        return featureImportanceMapper.insert(featureImportance) > 0;
    }
    
    public boolean updateFeatureImportance(FeatureImportance featureImportance) {
        return featureImportanceMapper.updateById(featureImportance) > 0;
    }
    
    public boolean deleteFeatureImportance(Long id) {
        return featureImportanceMapper.deleteById(id) > 0;
    }
    
    // MergedData CRUD
    public List<MergedData> getAllMergedData() {
        return mergedDataMapper.selectList(null);
    }
    
    public MergedData getMergedDataById(Long id) {
        return mergedDataMapper.selectById(id);
    }
    
    public Page<MergedData> getMergedDataPage(Integer page, Integer size, String search) {
        // 限制最大页面大小，防止查询过大数据
        if (size == null || size <= 0) {
            size = 10;
        }
        if (size > 200) {
            size = 200;
        }
        
        // 确保页码有效
        if (page == null || page <= 0) {
            page = 1;
        }
        
        // 创建分页对象
        Page<MergedData> pageObj = new Page<>(page, size);
        // 启用查询总数（默认已启用）
        pageObj.setSearchCount(true);
        
        QueryWrapper<MergedData> wrapper = new QueryWrapper<>();
        
        if (search != null && !search.trim().isEmpty()) {
            String searchTerm = search.trim();
            wrapper.and(w -> w
                .like("订单编号", searchTerm)
                .or().like("产品型号", searchTerm)
                .or().like("品牌名称", searchTerm)
                .or().like("用户所在省份", searchTerm)
            );
        }
        
        // 使用主键索引排序，按id升序
        wrapper.orderByAsc("id");
        
        // 执行分页查询 - 这里会自动应用分页拦截器
        Page<MergedData> result = mergedDataMapper.selectPage(pageObj, wrapper);
        
        return result;
    }
    
    public boolean saveMergedData(MergedData mergedData) {
        return mergedDataMapper.insert(mergedData) > 0;
    }
    
    public boolean updateMergedData(MergedData mergedData) {
        return mergedDataMapper.updateById(mergedData) > 0;
    }
    
    public boolean deleteMergedData(Long id) {
        return mergedDataMapper.deleteById(id) > 0;
    }
}

