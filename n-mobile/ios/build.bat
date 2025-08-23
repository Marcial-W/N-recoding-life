@echo off
REM iOS构建脚本 (Windows版本)
REM 用于自动化构建iOS应用

setlocal enabledelayedexpansion

REM 颜色定义
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM 打印带颜色的消息
:print_message
echo %GREEN%[INFO]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

:print_step
echo %BLUE%[STEP]%NC% %~1
goto :eof

REM 检查依赖
:check_dependencies
call :print_step "检查依赖..."

REM 检查Xcode (在Windows上不可用，但保留检查)
where xcodebuild >nul 2>&1
if %errorlevel% neq 0 (
    call :print_warning "Xcode未安装或未配置 (在Windows上需要macOS)"
)

REM 检查CocoaPods (在Windows上不可用，但保留检查)
where pod >nul 2>&1
if %errorlevel% neq 0 (
    call :print_warning "CocoaPods未安装 (在Windows上需要macOS)"
)

REM 检查Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    call :print_error "Node.js未安装"
    exit /b 1
)

call :print_message "依赖检查完成"
goto :eof

REM 清理项目
:clean_project
call :print_step "清理项目..."

REM 清理Node.js依赖
if exist "node_modules" (
    rmdir /s /q "node_modules"
)

REM 清理构建文件
if exist "build" (
    rmdir /s /q "build"
)

call :print_message "项目清理完成"
goto :eof

REM 安装依赖
:install_dependencies
call :print_step "安装依赖..."

REM 安装Node.js依赖
cd ..\..
call npm install
cd ios\App

call :print_message "依赖安装完成"
goto :eof

REM 构建项目
:build_project
call :print_step "构建项目..."

set "configuration=%~1"
if "%configuration%"=="" set "configuration=Release"

call :print_message "构建配置: %configuration%"
call :print_warning "在Windows上无法直接构建iOS项目，需要macOS环境"

goto :eof

REM 构建归档文件
:build_archive
call :print_step "构建归档文件..."

call :print_warning "在Windows上无法直接构建iOS归档文件，需要macOS环境"

goto :eof

REM 导出IPA
:export_ipa
call :print_step "导出IPA文件..."

call :print_warning "在Windows上无法直接导出IPA文件，需要macOS环境"

goto :eof

REM 运行测试
:run_tests
call :print_step "运行测试..."

REM 运行Node.js测试
cd ..\..
call npm test
cd ios\App

call :print_message "测试完成"
goto :eof

REM 代码签名
:code_sign
call :print_step "代码签名..."

call :print_warning "在Windows上无法进行iOS代码签名，需要macOS环境"

goto :eof

REM 显示帮助信息
:show_help
echo iOS构建脚本 (Windows版本)
echo.
echo 用法: %0 [选项]
echo.
echo 选项:
echo   clean              清理项目
echo   install            安装依赖
echo   build [config]     构建项目 (默认: Release)
echo   archive [scheme]   构建归档文件 (默认: App)
echo   export [archive]   导出IPA文件
echo   test               运行测试
echo   sign [identity]    代码签名
echo   full               完整构建流程
echo   help               显示此帮助信息
echo.
echo 注意: 在Windows上，iOS相关的构建步骤需要macOS环境
echo.
echo 示例:
echo   %0 clean
echo   %0 install
echo   %0 build Debug
echo   %0 full
goto :eof

REM 完整构建流程
:full_build
call :print_step "开始完整构建流程..."

call check_dependencies
call clean_project
call install_dependencies
call build_project
call build_archive
call export_ipa

call :print_message "完整构建流程完成！"
goto :eof

REM 主函数
:main
set "action=%~1"
if "%action%"=="" set "action=help"

if "%action%"=="clean" goto clean_project
if "%action%"=="install" goto install_dependencies
if "%action%"=="build" goto build_project
if "%action%"=="archive" goto build_archive
if "%action%"=="export" goto export_ipa
if "%action%"=="test" goto run_tests
if "%action%"=="sign" goto code_sign
if "%action%"=="full" goto full_build
if "%action%"=="help" goto show_help
goto show_help

REM 执行主函数
call :main %* 