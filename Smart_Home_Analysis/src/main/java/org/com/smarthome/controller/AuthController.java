package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.entity.User;
import org.com.smarthome.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin
public class AuthController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody Map<String, String> params) {
        String username = params.get("username");
        String password = params.get("password");
        
        if (username == null || password == null) {
            return Result.error("用户名和密码不能为空");
        }
        
        Map<String, Object> result = userService.login(username, password);
        boolean success = (Boolean) result.get("success");
        
        if (success) {
            return Result.success("登录成功", result);
        } else {
            return Result.error((String) result.get("message"));
        }
    }
    
    @PostMapping("/register")
    public Result<Map<String, Object>> register(@RequestBody Map<String, String> params) {
        try {
            String username = params.get("username");
            String password = params.get("password");
            String email = params.get("email");
            
            if (username == null || username.trim().isEmpty()) {
                return Result.error("用户名不能为空");
            }
            
            if (password == null || password.trim().isEmpty()) {
                return Result.error("密码不能为空");
            }
            
            User user = new User();
            user.setUsername(username.trim());
            user.setPassword(password);
            if (email != null && !email.trim().isEmpty()) {
                user.setEmail(email.trim());
            }
            
            Map<String, Object> result = userService.register(user);
            boolean success = (Boolean) result.get("success");
            
            if (success) {
                return Result.success("注册成功", result);
            } else {
                return Result.error((String) result.get("message"));
            }
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("注册失败: " + e.getMessage());
        }
    }
}

