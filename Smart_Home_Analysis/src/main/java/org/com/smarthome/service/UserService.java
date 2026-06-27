package org.com.smarthome.service;

import org.com.smarthome.entity.User;
import org.com.smarthome.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class UserService {
    
    @Autowired
    private UserMapper userMapper;
    
    public Map<String, Object> login(String username, String password) {
        Map<String, Object> result = new HashMap<>();
        
        User user = userMapper.findByUsername(username);
        if (user == null) {
            result.put("success", false);
            result.put("message", "用户名不存在");
            return result;
        }
        
        String encryptedPassword = DigestUtils.md5DigestAsHex(password.getBytes());
        if (!user.getPassword().equals(encryptedPassword)) {
            result.put("success", false);
            result.put("message", "密码错误");
            return result;
        }
        
        if (user.getStatus() == 0) {
            result.put("success", false);
            result.put("message", "账户已被禁用");
            return result;
        }
        
        user.setLastLoginTime(new Date());
        userMapper.updateById(user);
        
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("id", user.getId());
        userInfo.put("username", user.getUsername());
        userInfo.put("email", user.getEmail());
        userInfo.put("role", user.getRole());
        userInfo.put("realName", user.getRealName());
        
        result.put("success", true);
        result.put("message", "登录成功");
        result.put("user", userInfo);
        
        return result;
    }
    
    public Map<String, Object> register(User user) {
        Map<String, Object> result = new HashMap<>();
        
        try {
            if (user.getUsername() == null || user.getUsername().trim().isEmpty()) {
                result.put("success", false);
                result.put("message", "用户名不能为空");
                return result;
            }
            
            if (user.getPassword() == null || user.getPassword().trim().isEmpty()) {
                result.put("success", false);
                result.put("message", "密码不能为空");
                return result;
            }
            
            User existingUser = userMapper.findByUsername(user.getUsername());
            if (existingUser != null) {
                result.put("success", false);
                result.put("message", "用户名已存在");
                return result;
            }
            
            String encryptedPassword = DigestUtils.md5DigestAsHex(user.getPassword().getBytes());
            user.setPassword(encryptedPassword);
            user.setRole("user");
            user.setStatus(1);
            user.setCreateTime(new Date());
            
            if (user.getEmail() == null || user.getEmail().trim().isEmpty()) {
                user.setEmail(null);
            }
            
            int insertResult = userMapper.insert(user);
            if (insertResult > 0) {
                result.put("success", true);
                result.put("message", "注册成功");
            } else {
                result.put("success", false);
                result.put("message", "注册失败");
            }
        } catch (Exception e) {
            result.put("success", false);
            result.put("message", "注册失败: " + e.getMessage());
            e.printStackTrace();
        }
        
        return result;
    }
    
    /**
     * 根据用户名获取用户信息
     */
    public User getUserByUsername(String username) {
        return userMapper.findByUsername(username);
    }
    
    /**
     * 更新用户信息（用于个人信息修改）
     */
    public boolean updateUser(User user) {
        if (user.getId() == null) {
            // 如果没有ID，根据用户名查找
            User existingUser = userMapper.findByUsername(user.getUsername());
            if (existingUser == null) {
                throw new RuntimeException("用户不存在");
            }
            user.setId(existingUser.getId());
        }
        
        // 如果提供了新密码，则加密
        if (user.getPassword() != null && !user.getPassword().trim().isEmpty()) {
            String encryptedPassword = DigestUtils.md5DigestAsHex(user.getPassword().getBytes());
            user.setPassword(encryptedPassword);
        } else {
            // 不更新密码，保留原密码
            User existingUser = userMapper.selectById(user.getId());
            if (existingUser != null) {
                user.setPassword(existingUser.getPassword());
            }
        }
        
        return userMapper.updateById(user) > 0;
    }
}

