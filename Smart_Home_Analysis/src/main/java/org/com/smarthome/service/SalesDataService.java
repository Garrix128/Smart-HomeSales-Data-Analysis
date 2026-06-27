package org.com.smarthome.service;

import org.com.smarthome.entity.SalesSummary;
import org.com.smarthome.mapper.SalesDataMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;

@Service
public class SalesDataService {
    
    @Autowired
    private SalesDataMapper salesDataMapper;
    
    public List<SalesSummary> getSalesTrend(Integer limit) {
        return salesDataMapper.getRecentSalesTrend(limit != null ? limit : 30);
    }
    
    public List<Map<String, Object>> getMonthlyTrend() {
        return salesDataMapper.getMonthlyTrend();
    }
}



