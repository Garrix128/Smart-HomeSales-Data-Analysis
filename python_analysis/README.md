# Python数据分析模块

## 功能说明

本模块使用**本地Spark**进行数据清洗和分析，分析结果自动保存到MySQL。

## 操作流程

### 步骤0: 初始化用户表（首次运行必须执行）
**文件**: `00_初始化用户表.py`

**功能**:
- 创建 `sys_user` 用户表
- 创建管理员账户（admin/admin）

**运行方式**:
```bash
cd python_analysis
python 00_初始化用户表.py
```

**输出**:
- MySQL数据库 `smart_home.sys_user` 表
- 管理员账户：用户名 `admin`，密码 `admin`

---

### 步骤1: 数据清洗
**文件**: `01_数据清洗.py`

**功能**:
- 读取Excel文件（5个数据文件）
- 清洗数据（处理缺失值、异常值、重复值）
- 合并用户数据和销售数据
- **自动去除所有重复列**
- 保存为单个CSV文件

**运行方式**:
```bash
cd python_analysis
python 01_数据清洗.py
```

**输出**:
- `output/cleaned_data/merged_data.csv` - 合并后的清洗数据（单个文件）

---

### 步骤2: 清洗合并后的数据上传
**文件**: `02_清洗合并后的数据上传.py`

**功能**:
- 从CSV文件读取合并后的数据
- 上传到MySQL数据库的`merged_data`表
- 自动创建数据库和表结构

**运行方式**:
```bash
python 02_清洗合并后的数据上传.py
```

**输出**:
- MySQL数据库 `smart_home.merged_data` 表

---

### 步骤3: 数据分析
**文件**: `03_数据分析.py`

**功能**:
- 从MySQL的`merged_data`表读取数据
- 执行多种数据分析：
  - 销售趋势分析
  - 地域分析
  - 产品品类分析
  - 用户行为分析
  - 随机森林预测模型
- 将分析结果直接保存到MySQL数据库

**运行方式**:
```bash
python 03_数据分析.py
```

**输出** (MySQL数据库 `smart_home`):
- `sales_summary` - 销售汇总表
- `region_analysis` - 地域分析表
- `product_analysis` - 产品分析表
- `user_profile` - 用户画像分析表
- `promotion_analysis` - 促销效果分析表
- `prediction_result` - 预测结果表
- `feature_importance` - 特征重要性表
- `model_evaluation` - 模型评估指标表（RMSE、MAE、R²等）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置MySQL连接

编辑以下文件中的MySQL配置：
- `02_清洗合并后的数据上传.py`
- `03_数据分析.py` (或 `data_analysis_to_mysql.py`)

修改以下配置：
```python
self.mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456'  # 修改为你的MySQL密码
}
```

## 完整运行流程

```bash
# 步骤0: 初始化用户表（首次运行必须执行）
python 00_初始化用户表.py

# 步骤1: 数据清洗
python 01_数据清洗.py

# 步骤2: 数据上传
python 02_清洗合并后的数据上传.py

# 步骤3: 数据分析
python 03_数据分析.py
```

**注意**: 步骤0只需要在首次运行时执行一次，用于创建用户表和管理员账户。

## 注意事项

1. **首次运行**: 会自动创建数据库和表结构
2. **数据覆盖**: 每次运行会清空旧数据并插入新数据
3. **MySQL必需**: 步骤2和步骤3都需要MySQL数据库
4. **数据流程**: 数据清洗 -> 上传到MySQL -> 从MySQL分析 -> 保存分析结果到MySQL
