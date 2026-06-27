package org.com.smarthome.service;

import org.com.smarthome.mapper.UserBehaviorMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;

@Service
public class UserBehaviorService {
    
    @Autowired
    private UserBehaviorMapper userBehaviorMapper;
    
    public List<Map<String, Object>> getMemberAnalysis() {
        return userBehaviorMapper.getMemberAnalysis();
    }
}



