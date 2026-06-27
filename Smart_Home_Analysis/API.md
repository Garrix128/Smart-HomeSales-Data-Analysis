# API接口文档

## 基础信息

- 基础URL: `http://localhost:8080/api`
- 数据格式: JSON
- 字符编码: UTF-8

## 响应格式

所有接口统一返回格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

## 接口列表

### 1. 销售数据接口

#### 1.1 获取销售趋势
- **URL**: `/sales/trend`
- **方法**: `GET`
- **参数**:
  - `limit` (可选): 返回记录数，默认30

**响应示例**:
```json
{
  "code": 200,
  "message": "操作成功",
  "data": [
    {
      "month": "2024-01",
      "totalSales": 100000.00,
      "orderCount": 100
    }
  ]
}
```

#### 1.2 获取月度趋势
- **URL**: `/sales/monthly`
- **方法**: `GET`

### 2. 分析结果接口

#### 2.1 获取地域分析
- **URL**: `/analysis/region`
- **方法**: `GET`

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "region": "北京",
      "totalSales": 500000.00,
      "orderCount": 500,
      "userCount": 300
    }
  ]
}
```

#### 2.2 获取产品分析
- **URL**: `/analysis/product`
- **方法**: `GET`

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "category": [
      {
        "category": "智能音箱",
        "totalSales": 200000.00,
        "salesVolume": 200
      }
    ],
    "topBrands": [
      {
        "brand": "品牌A",
        "totalSales": 150000.00
      }
    ]
  }
}
```

### 3. 用户行为接口

#### 3.1 获取会员分析
- **URL**: `/user/member`
- **方法**: `GET`

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "memberType": "会员",
      "count": 100,
      "avgConsumption": 5000.00,
      "avgOrders": 10
    }
  ]
}
```

### 4. 预测接口

#### 4.1 获取随机森林结果
- **URL**: `/prediction/random-forest`
- **方法**: `GET`

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "predictions": [
      {
        "predictionDate": "2024-01-01",
        "predictedSales": 100000.00,
        "actualSales": 95000.00
      }
    ],
    "featureImportance": [
      {
        "featureName": "价格",
        "importance": 0.35,
        "rank": 1
      }
    ]
  }
}
```

#### 4.2 获取特征重要性
- **URL**: `/prediction/features`
- **方法**: `GET`

### 5. 数据管理接口

#### 5.1 获取销售汇总列表
- **URL**: `/data/manage/sales`
- **方法**: `GET`

#### 5.2 获取销售汇总详情
- **URL**: `/data/manage/sales/{id}`
- **方法**: `GET`

#### 5.3 新增销售汇总
- **URL**: `/data/manage/sales`
- **方法**: `POST`
- **请求体**:
```json
{
  "salesDate": "2024-01-01",
  "totalSales": 100000.00,
  "orderCount": 100,
  "avgOrderAmount": 1000.00
}
```

#### 5.4 更新销售汇总
- **URL**: `/data/manage/sales`
- **方法**: `PUT`
- **请求体**: 同POST

#### 5.5 删除销售汇总
- **URL**: `/data/manage/sales/{id}`
- **方法**: `DELETE`

#### 5.6 地域分析CRUD
- 获取列表: `GET /data/manage/region`
- 新增: `POST /data/manage/region`
- 更新: `PUT /data/manage/region`
- 删除: `DELETE /data/manage/region/{id}`

## 错误码说明

- `200`: 操作成功
- `500`: 服务器错误
- 其他: 根据实际情况返回

## 注意事项

1. 所有日期格式为 `yyyy-MM-dd`
2. 金额字段为 `DECIMAL` 类型，保留2位小数
3. 所有接口支持跨域请求
4. 请求超时时间为30秒



