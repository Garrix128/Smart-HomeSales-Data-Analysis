package org.com.smarthome.service;

import org.com.smarthome.entity.User;
import org.com.smarthome.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 用户管理Service（管理员端）
 */
@Service
public class UserManageService {
    
    @Autowired
    private UserMapper userMapper;
    
    /**
     * 分页查询用户
     */
    public Map<String, Object> getUserPage(Integer page, Integer size, String search) {
        if (size == null || size <= 0) {
            size = 10;
        }
        if (size > 200) {
            size = 200;
        }
        if (page == null || page <= 0) {
            page = 1;
        }
        
        Page<User> pageObj = new Page<>(page, size);
        QueryWrapper<User> wrapper = new QueryWrapper<>();
        
        if (search != null && !search.trim().isEmpty()) {
            String searchTerm = search.trim();
            wrapper.and(w -> w
                .like("username", searchTerm)
                .or().like("email", searchTerm)
                .or().like("real_name", searchTerm)
            );
        }
        
        wrapper.orderByDesc("create_time");
        Page<User> result = userMapper.selectPage(pageObj, wrapper);
        
        Map<String, Object> map = new HashMap<>();
        map.put("records", result.getRecords());
        map.put("total", result.getTotal());
        map.put("current", result.getCurrent());
        map.put("size", result.getSize());
        
        return map;
    }
    
    /**
     * 获取所有用户
     */
    public List<User> getAllUsers() {
        return userMapper.selectList(null);
    }
    
    /**
     * 根据ID获取用户
     */
    public User getUserById(Long id) {
        return userMapper.selectById(id);
    }
    
    /**
     * 创建用户（管理员或普通用户）
     */
    public boolean createUser(User user) {
        if (user.getUsername() == null || user.getUsername().trim().isEmpty()) {
            throw new RuntimeException("用户名不能为空");
        }
        
        if (user.getPassword() == null || user.getPassword().trim().isEmpty()) {
            throw new RuntimeException("密码不能为空");
        }
        
        // 检查用户名是否已存在
        User existingUser = userMapper.findByUsername(user.getUsername());
        if (existingUser != null) {
            throw new RuntimeException("用户名已存在");
        }
        
        // 加密密码
        String encryptedPassword = DigestUtils.md5DigestAsHex(user.getPassword().getBytes());
        user.setPassword(encryptedPassword);
        
        // 设置默认值
        if (user.getRole() == null || user.getRole().trim().isEmpty()) {
            user.setRole("user");
        }
        if (user.getStatus() == null) {
            user.setStatus(1);
        }
        user.setCreateTime(new Date());
        
        return userMapper.insert(user) > 0;
    }
    
    /**
     * 更新用户信息
     */
    public boolean updateUser(User user) {
        if (user.getId() == null) {
            throw new RuntimeException("用户ID不能为空");
        }
        
        User existingUser = userMapper.selectById(user.getId());
        if (existingUser == null) {
            throw new RuntimeException("用户不存在");
        }
        
        // 如果修改了用户名，检查是否重复
        if (user.getUsername() != null && !user.getUsername().equals(existingUser.getUsername())) {
            User checkUser = userMapper.findByUsername(user.getUsername());
            if (checkUser != null && !checkUser.getId().equals(user.getId())) {
                throw new RuntimeException("用户名已存在");
            }
        }
        
        // 如果提供了新密码，则加密
        if (user.getPassword() != null && !user.getPassword().trim().isEmpty()) {
            String encryptedPassword = DigestUtils.md5DigestAsHex(user.getPassword().getBytes());
            user.setPassword(encryptedPassword);
        } else {
            // 不更新密码，保留原密码
            user.setPassword(existingUser.getPassword());
        }
        
        return userMapper.updateById(user) > 0;
    }
    
    /**
     * 删除用户
     */
    public boolean deleteUser(Long id) {
        return userMapper.deleteById(id) > 0;
    }
    
    /**
     * 更新用户状态
     */
    public boolean updateUserStatus(Long id, Integer status) {
        User user = new User();
        user.setId(id);
        user.setStatus(status);
        return userMapper.updateById(user) > 0;
    }
}

