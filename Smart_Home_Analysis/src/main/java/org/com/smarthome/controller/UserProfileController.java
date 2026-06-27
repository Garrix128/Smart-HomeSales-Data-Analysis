package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.entity.User;
import org.com.smarthome.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

/**
 * 用户个人信息Controller
 */
@RestController
@RequestMapping("/api/user/profile")
@CrossOrigin
public class UserProfileController {
    
    @Autowired
    private UserService userService;
    
    /**
     * 获取当前用户信息
     */
    @GetMapping
    public Result<User> getCurrentUser(@RequestParam String username) {
        try {
            User user = userService.getUserByUsername(username);
            if (user == null) {
                return Result.error("用户不存在");
            }
            // 不返回密码
            user.setPassword(null);
            return Result.success(user);
        } catch (Exception e) {
            return Result.error("获取用户信息失败: " + e.getMessage());
        }
    }
    
    /**
     * 更新当前用户信息
     */
    @PutMapping
    public Result<Boolean> updateCurrentUser(@RequestBody Map<String, Object> params) {
        try {
            String username = (String) params.get("username");
            if (username == null || username.trim().isEmpty()) {
                return Result.error("用户名不能为空");
            }
            
            User user = userService.getUserByUsername(username);
            if (user == null) {
                return Result.error("用户不存在");
            }
            
            // 更新允许修改的字段
            if (params.containsKey("email")) {
                user.setEmail((String) params.get("email"));
            }
            if (params.containsKey("phone")) {
                user.setPhone((String) params.get("phone"));
            }
            if (params.containsKey("realName")) {
                user.setRealName((String) params.get("realName"));
            }
            if (params.containsKey("password") && params.get("password") != null) {
                String password = (String) params.get("password");
                if (!password.trim().isEmpty()) {
                    user.setPassword(password);
                }
            }
            
            boolean success = userService.updateUser(user);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
}



