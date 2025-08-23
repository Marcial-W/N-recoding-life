#!/bin/bash

# iOS构建脚本
# 用于自动化构建iOS应用

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_step "检查依赖..."
    
    # 检查Xcode
    if ! command -v xcodebuild &> /dev/null; then
        print_error "Xcode未安装或未配置"
        exit 1
    fi
    
    # 检查CocoaPods
    if ! command -v pod &> /dev/null; then
        print_error "CocoaPods未安装"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js未安装"
        exit 1
    fi
    
    print_message "所有依赖检查通过"
}

# 清理项目
clean_project() {
    print_step "清理项目..."
    
    # 清理Xcode构建
    xcodebuild clean -workspace App.xcworkspace -scheme App -configuration Release
    
    # 清理Pods
    pod deintegrate
    pod cache clean --all
    
    # 清理DerivedData
    rm -rf ~/Library/Developer/Xcode/DerivedData/*
    
    print_message "项目清理完成"
}

# 安装依赖
install_dependencies() {
    print_step "安装依赖..."
    
    # 安装Node.js依赖
    cd ../..
    npm install
    cd ios/App
    
    # 安装Pods
    pod install --repo-update
    
    print_message "依赖安装完成"
}

# 构建项目
build_project() {
    print_step "构建项目..."
    
    local configuration=${1:-Release}
    local scheme=${2:-App}
    
    # 构建项目
    xcodebuild build \
        -workspace App.xcworkspace \
        -scheme $scheme \
        -configuration $configuration \
        -destination 'generic/platform=iOS' \
        -derivedDataPath build \
        CODE_SIGN_IDENTITY="" \
        CODE_SIGNING_REQUIRED=NO \
        CODE_SIGNING_ALLOWED=NO
    
    print_message "项目构建完成"
}

# 构建归档文件
build_archive() {
    print_step "构建归档文件..."
    
    local scheme=${1:-App}
    local archive_path="./build/App.xcarchive"
    
    # 创建归档
    xcodebuild archive \
        -workspace App.xcworkspace \
        -scheme $scheme \
        -configuration Release \
        -archivePath $archive_path \
        -destination 'generic/platform=iOS' \
        CODE_SIGN_IDENTITY="" \
        CODE_SIGNING_REQUIRED=NO \
        CODE_SIGNING_ALLOWED=NO
    
    print_message "归档文件创建完成: $archive_path"
}

# 导出IPA
export_ipa() {
    print_step "导出IPA文件..."
    
    local archive_path=${1:-"./build/App.xcarchive"}
    local export_path=${2:-"./build/App.ipa"}
    local export_options_plist="./exportOptions.plist"
    
    # 创建导出选项文件
    cat > $export_options_plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>development</string>
    <key>teamID</key>
    <string></string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>uploadBitcode</key>
    <false/>
    <key>uploadSymbols</key>
    <false/>
</dict>
</plist>
EOF
    
    # 导出IPA
    xcodebuild -exportArchive \
        -archivePath $archive_path \
        -exportPath $export_path \
        -exportOptionsPlist $export_options_plist
    
    print_message "IPA文件导出完成: $export_path"
}

# 运行测试
run_tests() {
    print_step "运行测试..."
    
    xcodebuild test \
        -workspace App.xcworkspace \
        -scheme App \
        -destination 'platform=iOS Simulator,name=iPhone 14,OS=latest' \
        -derivedDataPath build
    
    print_message "测试完成"
}

# 代码签名
code_sign() {
    print_step "代码签名..."
    
    local identity=${1:-"iPhone Developer"}
    local provisioning_profile=${2:-""}
    
    if [ -n "$provisioning_profile" ]; then
        xcodebuild build \
            -workspace App.xcworkspace \
            -scheme App \
            -configuration Release \
            -destination 'generic/platform=iOS' \
            CODE_SIGN_IDENTITY="$identity" \
            PROVISIONING_PROFILE="$provisioning_profile" \
            CODE_SIGNING_REQUIRED=YES \
            CODE_SIGNING_ALLOWED=YES
    else
        print_warning "未提供配置文件，跳过代码签名"
    fi
}

# 显示帮助信息
show_help() {
    echo "iOS构建脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  clean              清理项目"
    echo "  install            安装依赖"
    echo "  build [config]     构建项目 (默认: Release)"
    echo "  archive [scheme]   构建归档文件 (默认: App)"
    echo "  export [archive]   导出IPA文件"
    echo "  test               运行测试"
    echo "  sign [identity]    代码签名"
    echo "  full               完整构建流程"
    echo "  help               显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 clean"
    echo "  $0 install"
    echo "  $0 build Debug"
    echo "  $0 full"
}

# 完整构建流程
full_build() {
    print_step "开始完整构建流程..."
    
    check_dependencies
    clean_project
    install_dependencies
    build_project
    build_archive
    export_ipa
    
    print_message "完整构建流程完成！"
}

# 主函数
main() {
    local action=${1:-"help"}
    
    case $action in
        "clean")
            clean_project
            ;;
        "install")
            install_dependencies
            ;;
        "build")
            build_project $2
            ;;
        "archive")
            build_archive $2
            ;;
        "export")
            export_ipa $2 $3
            ;;
        "test")
            run_tests
            ;;
        "sign")
            code_sign $2 $3
            ;;
        "full")
            full_build
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@" 