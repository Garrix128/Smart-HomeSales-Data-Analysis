package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.service.UserBehaviorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * 用户行为分析Controller
 */
@RestController
@RequestMapping("/api/user")
@CrossOrigin
public class UserBehaviorController {
    
    @Autowired
    private UserBehaviorService userBehaviorService;
    
    /**
     * 获取会员分析数据
     */
    @GetMapping("/member")
    public Result<List<Map<String, Object>>> getMemberAnalysis() {
        try {
            List<Map<String, Object>> data = userBehaviorService.getMemberAnalysis();
            return Result.success(data);
        } catch (Exception e) {
            return Result.error("获取会员分析数据失败: " + e.getMessage());
        }
    }
}



