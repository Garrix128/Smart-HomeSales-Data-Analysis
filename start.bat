@echo off
chcp 65001 >nul
echo ==========================================
echo 智能家居销量数据分析系统启动脚本
echo ==========================================

echo 1. 检查Java环境...
java -version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Java环境，请先安装JDK 1.8
    pause
    exit /b 1
)

echo 2. 检查Maven环境...
mvn -version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Maven，请先安装Maven 3.9.9
    pause
    exit /b 1
)

echo 3. 编译并启动SpringBoot后端...
cd Smart_Home_Analysis
call mvn clean package -DskipTests
if errorlevel 1 (
    echo 后端编译失败
    pause
    exit /b 1
)

echo 后端启动中...
start "后端服务" java -jar target/Smart_Home_Analysis-1.0-SNAPSHOT.jar

cd ..

echo 4. 启动Vue前端...
cd Smart_Home_Analysis\frontend
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)

echo 前端启动中...
start "前端服务" cmd /k "npm run serve"

cd ..\..

echo ==========================================
echo 系统启动完成！
echo 后端: http://localhost:8080
echo 前端: http://localhost:8081
echo ==========================================
pause



