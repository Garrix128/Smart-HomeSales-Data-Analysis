package org.com.smarthome.config;

import org.com.smarthome.entity.User;
import org.com.smarthome.mapper.UserMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.util.DigestUtils;
import java.util.Date;

@Component
public class InitAdminUser implements CommandLineRunner {
    
    private static final Logger logger = LoggerFactory.getLogger(InitAdminUser.class);
    
    @Autowired
    private UserMapper userMapper;
    
    @Override
    public void run(String... args) throws Exception {
        User adminUser = userMapper.findByUsername("admin");
        if (adminUser == null) {
            adminUser = new User();
            adminUser.setUsername("admin");
            adminUser.setPassword(DigestUtils.md5DigestAsHex("admin".getBytes()));
            adminUser.setEmail("admin@smarthome.com");
            adminUser.setRole("admin");
            adminUser.setStatus(1);
            adminUser.setRealName("系统管理员");
            adminUser.setCreateTime(new Date());
            
            userMapper.insert(adminUser);
            logger.info("管理员账户创建成功: admin/admin");
        } else {
            logger.info("管理员账户已存在: admin");
        }
    }
}


