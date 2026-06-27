package org.com.smarthome.controller;

import org.com.smarthome.common.Result;
import org.com.smarthome.entity.User;
import org.com.smarthome.service.UserManageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * 用户管理Controller（管理员端）
 */
@RestController
@RequestMapping("/api/user/manage")
@CrossOrigin
public class UserManageController {
    
    @Autowired
    private UserManageService userManageService;
    
    /**
     * 获取所有用户列表（分页）
     */
    @GetMapping("/page")
    public Result<Map<String, Object>> getUserPage(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String search) {
        try {
            Map<String, Object> result = userManageService.getUserPage(page, size, search);
            return Result.success(result);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取所有用户列表
     */
    @GetMapping("/list")
    public Result<List<User>> getAllUsers() {
        try {
            List<User> users = userManageService.getAllUsers();
            return Result.success(users);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    /**
     * 根据ID获取用户
     */
    @GetMapping("/{id}")
    public Result<User> getUserById(@PathVariable Long id) {
        try {
            User user = userManageService.getUserById(id);
            return Result.success(user);
        } catch (Exception e) {
            return Result.error("查询失败: " + e.getMessage());
        }
    }
    
    /**
     * 创建用户（管理员或普通用户）
     */
    @PostMapping
    public Result<Boolean> createUser(@RequestBody User user) {
        try {
            boolean success = userManageService.createUser(user);
            return success ? Result.success("创建成功", true) : Result.error("创建失败");
        } catch (Exception e) {
            return Result.error("创建失败: " + e.getMessage());
        }
    }
    
    /**
     * 更新用户信息
     */
    @PutMapping
    public Result<Boolean> updateUser(@RequestBody User user) {
        try {
            boolean success = userManageService.updateUser(user);
            return success ? Result.success("更新成功", true) : Result.error("更新失败");
        } catch (Exception e) {
            return Result.error("更新失败: " + e.getMessage());
        }
    }
    
    /**
     * 删除用户
     */
    @DeleteMapping("/{id}")
    public Result<Boolean> deleteUser(@PathVariable Long id) {
        try {
            boolean success = userManageService.deleteUser(id);
            return success ? Result.success("删除成功", true) : Result.error("删除失败");
        } catch (Exception e) {
            return Result.error("删除失败: " + e.getMessage());
        }
    }
    
    /**
     * 启用/禁用用户
     */
    @PutMapping("/{id}/status")
    public Result<Boolean> updateUserStatus(@PathVariable Long id, @RequestBody Map<String, Integer> params) {
        try {
            Integer status = params.get("status");
            boolean success = userManageService.updateUserStatus(id, status);
            return success ? Result.success("操作成功", true) : Result.error("操作失败");
        } catch (Exception e) {
            return Result.error("操作失败: " + e.getMessage());
        }
    }
}



