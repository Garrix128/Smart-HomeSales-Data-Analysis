#!/bin/bash

echo "=========================================="
echo "智能家居销量数据分析系统启动脚本"
echo "=========================================="

# 检查Java环境
if ! command -v java &> /dev/null; then
    echo "错误: 未找到Java环境，请先安装JDK 1.8"
    exit 1
fi

# 检查Maven环境
if ! command -v mvn &> /dev/null; then
    echo "错误: 未找到Maven，请先安装Maven 3.9.9"
    exit 1
fi

# 检查MySQL
if ! command -v mysql &> /dev/null; then
    echo "警告: 未找到MySQL客户端，请确保MySQL服务已启动"
fi

echo "1. 启动MySQL数据库..."
echo "   请确保MySQL服务已启动，并已创建smart_home数据库"

echo "2. 编译并启动SpringBoot后端..."
cd Smart_Home_Analysis
mvn clean package -DskipTests
if [ $? -eq 0 ]; then
    echo "   后端编译成功，启动中..."
    java -jar target/Smart_Home_Analysis-1.0-SNAPSHOT.jar &
    BACKEND_PID=$!
    echo "   后端已启动，PID: $BACKEND_PID"
    echo "   访问地址: http://localhost:8080"
else
    echo "   后端编译失败"
    exit 1
fi

cd ..

echo "3. 启动Vue前端..."
cd Smart_Home_Analysis/frontend
if [ ! -d "node_modules" ]; then
    echo "   安装前端依赖..."
    npm install
fi
echo "   前端启动中..."
npm run serve &
FRONTEND_PID=$!
echo "   前端已启动，PID: $FRONTEND_PID"
echo "   访问地址: http://localhost:8081"

cd ../..

echo "=========================================="
echo "系统启动完成！"
echo "后端: http://localhost:8080"
echo "前端: http://localhost:8081"
echo "=========================================="
echo "按Ctrl+C停止所有服务"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait



