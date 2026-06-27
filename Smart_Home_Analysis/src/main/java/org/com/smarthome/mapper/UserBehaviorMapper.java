package org.com.smarthome.mapper;

import org.com.smarthome.entity.UserBehavior;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface UserBehaviorMapper extends BaseMapper<UserBehavior> {
    
    @Select("SELECT " +
            "member_type, " +
            "SUM(user_count) as user_count, " +
            "AVG(avg_consumption) as avg_consumption, " +
            "SUM(total_sales) as total_sales " +
            "FROM user_profile " +
            "WHERE member_type IS NOT NULL " +
            "AND member_type != '' " +
            "AND member_type != '0' " +
            "AND (member_type = '是' OR member_type = '否' OR member_type LIKE '%会员%' OR member_type LIKE '%否%') " +
            "GROUP BY member_type " +
            "ORDER BY member_type DESC")
    List<Map<String, Object>> getMemberAnalysis();
}
