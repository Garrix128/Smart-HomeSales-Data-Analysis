# 智能家居销量数据分析系统

基于Hadoop的智能家居销量数据分析系统，采用前后端分离架构，使用PySpark进行大数据处理和分析。

## 技术栈

### 前端
- Vue 3.3.4
- Element Plus 2.3.12
- ECharts 5.4.3
- Vue Router 4.2.4
- Axios 1.5.0

### 后端
- SpringBoot 2.7.18
- MyBatis Plus 3.5.3.1
- MySQL 5.6.x
- JDK 1.8

### 数据处理
- PySpark 3.4.0
- Hadoop 3.3.6
- Python 3.10

## 项目结构

```
smart_home/
├── python_analysis/          # Python数据分析模块
│   ├── data/                 # 数据文件目录
│   ├── data_cleaning.py      # 数据清洗模块
│   ├── data_analysis.py      # 数据分析模块
│   ├── main.py              # 主程序入口
│   ├── spark_config.py      # Spark配置
│   └── requirements.txt     # Python依赖
│
├── Smart_Home_Analysis/      # SpringBoot后端项目
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── org/com/smarthome/
│   │   │   │       ├── SmartHomeApplication.java
│   │   │   │       ├── config/          # 配置类
│   │   │   │       ├── controller/      # 控制器
│   │   │   │       ├── service/         # 服务层
│   │   │   │       ├── mapper/          # 数据访问层
│   │   │   │       ├── entity/          # 实体类
│   │   │   │       └── common/          # 公共类
│   │   │   └── resources/
│   │   │       ├── application.yml      # 应用配置
│   │   │       └── db/
│   │   │           └── schema.sql       # 数据库脚本
│   │   └── test/
│   ├── frontend/             # Vue前端项目
│   │   ├── src/
│   │   │   ├── components/   # 组件
│   │   │   ├── views/        # 视图
│   │   │   ├── router/       # 路由
│   │   │   ├── utils/        # 工具类
│   │   │   └── App.vue
│   │   ├── public/
│   │   ├── package.json
│   │   └── vue.config.js
│   └── pom.xml
│
├── docker-compose.yml        # Docker编排文件
└── README.md                # 项目文档
```

## 功能模块

### 1. 数据清洗与存储模块
- 读取多个Excel数据源并进行数据整合
- 处理缺失值、异常值、重复数据
- 数据格式标准化（日期、数值、分类变量）
- 将清洗后的数据存储到HDFS

### 2. 数据分析模块
- 销售趋势分析（时间序列）
- 地域分布分析
- 用户画像分析
- 产品品类分析
- 随机森林预测模型

### 3. 后端API
- `GET /api/sales/trend` - 获取销售趋势数据
- `GET /api/analysis/region` - 获取地域分析数据
- `GET /api/analysis/product` - 获取产品分析数据
- `GET /api/user/member` - 获取会员分析数据
- `GET /api/prediction/random-forest` - 获取随机森林结果
- `GET /api/prediction/features` - 获取特征重要性
- `POST /api/data/manage/*` - 数据管理CRUD操作

### 4. 前端可视化
- 销售额时间趋势图（折线图）
- 地域分布热力图（地图）
- 产品品类占比图（饼图）
- 销售渠道分析图（柱状图）
- 用户画像分析图（雷达图）
- 随机森林特征重要性图（条形图）

## 安装和运行

### 环境要求
- JDK 1.8
- Maven 3.9.9
- Python 3.10
- Node.js 16+
- MySQL 5.6.x（只需安装，无需手动创建数据库和表）
- Hadoop 3.3.6（可选，如果不可用会自动保存到本地）
- Spark 3.4.0

### 1. 数据库准备

**重要：无需手动创建数据库和表！**

系统会在运行Python分析脚本时自动：
- 创建 `smart_home` 数据库（如果不存在）
- 创建所有必需的表结构（如果不存在）
- 将分析结果保存到MySQL

只需确保MySQL服务已启动，并且配置了正确的用户名和密码（默认：root/root）。

### 2. 后端启动

```bash
cd Smart_Home_Analysis
mvn clean package
java -jar target/Smart_Home_Analysis-1.0-SNAPSHOT.jar
```

后端服务将在 `http://localhost:8080` 启动

### 3. 前端启动

```bash
cd Smart_Home_Analysis/frontend
npm install
npm run serve
```

前端服务将在 `http://localhost:8081` 启动

### 4. Python数据分析（自动创建数据库和表）

```bash
cd python_analysis
pip install -r requirements.txt

# 配置Hadoop和Spark环境变量（可选）
export HADOOP_HOME=/path/to/hadoop
export SPARK_HOME=/path/to/spark
export PYSPARK_PYTHON=python3

# 运行数据清洗和分析
# 注意：此步骤会自动创建MySQL数据库和表，并保存分析结果
python main.py
```

**重要提示：**
- Python脚本会自动创建 `smart_home` 数据库和所有表结构
- 分析结果会自动保存到MySQL，后端可以直接读取
- 如果MySQL连接失败，请检查 `data_analysis.py` 中的MySQL配置

### 5. Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 配置说明

### application.yml
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/smart_home
    username: root
    password: root
```

### vue.config.js
```javascript
devServer: {
  port: 8081,
  proxy: {
    '/api': {
      target: 'http://localhost:8080'
    }
  }
}
```

## API文档

### 销售数据API

#### 获取销售趋势
```
GET /api/sales/trend?limit=30
```

#### 获取月度趋势
```
GET /api/sales/monthly
```

### 分析结果API

#### 获取地域分析
```
GET /api/analysis/region
```

#### 获取产品分析
```
GET /api/analysis/product
```

### 用户行为API

#### 获取会员分析
```
GET /api/user/member
```

### 预测API

#### 获取随机森林结果
```
GET /api/prediction/random-forest
```

#### 获取特征重要性
```
GET /api/prediction/features
```

### 数据管理API

#### 获取销售汇总列表
```
GET /api/data/manage/sales
```

#### 新增销售汇总
```
POST /api/data/manage/sales
Content-Type: application/json

{
  "salesDate": "2024-01-01",
  "totalSales": 100000.00,
  "orderCount": 100,
  "avgOrderAmount": 1000.00
}
```

#### 更新销售汇总
```
PUT /api/data/manage/sales
```

#### 删除销售汇总
```
DELETE /api/data/manage/sales/{id}
```

## 数据库表结构

### sales_summary - 销售汇总表
- id: 主键
- sales_date: 销售日期
- total_sales: 总销售额
- order_count: 订单数
- avg_order_amount: 平均订单金额

### region_analysis - 地域分析表
- id: 主键
- region: 地区
- total_sales: 总销售额
- order_count: 订单数
- user_count: 用户数

### user_behavior - 用户行为分析表
- id: 主键
- user_id: 用户ID
- total_consumption: 累计消费
- order_count: 订单数
- member_type: 会员类型

### product_analysis - 产品分析表
- id: 主键
- category: 产品类别
- brand: 品牌
- total_sales: 总销售额
- sales_volume: 销量

### prediction_result - 模型预测结果表
- id: 主键
- prediction_date: 预测日期
- predicted_sales: 预测销售额
- actual_sales: 实际销售额
- model_type: 模型类型

### feature_importance - 特征重要性表
- id: 主键
- feature_name: 特征名称
- importance: 重要性值
- rank: 排名
- model_type: 模型类型

## 开发说明

### 数据流程

```
原始Excel数据
    ↓
PySpark数据清洗 (data_cleaning.py)
    ↓
HDFS/本地存储 (清洗后的数据)
    ↓
PySpark数据分析 (data_analysis.py)
    ↓
自动创建MySQL数据库和表结构
    ↓
分析结果保存到MySQL
    ↓
SpringBoot API读取MySQL数据
    ↓
Vue前端展示可视化图表
```

**关键特性：**
- ✅ 无需手动创建数据库和表
- ✅ Python脚本自动初始化数据库结构
- ✅ 分析结果自动保存到MySQL
- ✅ 后端直接读取MySQL数据进行展示

### 注意事项
1. 确保Hadoop和Spark环境正确配置（HDFS可选，如果不可用会自动保存到本地）
2. **MySQL数据库无需提前创建**，Python脚本会自动创建
3. 前端需要配置代理指向后端API
4. 跨域请求已通过CorsConfig配置
5. 首次运行Python脚本前，确保MySQL服务已启动



