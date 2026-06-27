package org.com.smarthome.mapper;

import org.com.smarthome.entity.MergedData;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface MergedDataMapper extends BaseMapper<MergedData> {
    
    @Select("SELECT * FROM merged_data ORDER BY id DESC LIMIT #{limit}")
    List<MergedData> getRecentData(Integer limit);
}



