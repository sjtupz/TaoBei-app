#!/usr/bin/env python3
"""
测试运行脚本
提供便捷的测试执行和报告生成功能
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def setup_environment():
    """设置测试环境"""
    print("🔧 设置测试环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    # 检查依赖是否安装
    success, _, _ = run_command("pip show pytest")
    if not success:
        print("📦 安装Python依赖...")
        success, stdout, stderr = run_command("pip install -r requirements.txt")
        if not success:
            print(f"❌ 依赖安装失败: {stderr}")
            return False
    
    # 检查Playwright浏览器
    success, _, _ = run_command("playwright --version")
    if not success:
        print("🌐 安装Playwright浏览器...")
        success, stdout, stderr = run_command("playwright install")
        if not success:
            print(f"❌ Playwright安装失败: {stderr}")
            return False
    
    print("✅ 环境设置完成")
    return True


def run_tests(test_type="all", feature=None, scenario=None, browser="chromium", 
              headless=True, report_format="html", parallel=False):
    """运行测试"""
    
    # 构建pytest命令
    cmd_parts = ["pytest"]
    
    # 添加标记过滤
    if test_type == "ui":
        cmd_parts.extend(["-m", "ui"])
    elif test_type == "api":
        cmd_parts.extend(["-m", "api"])
    elif test_type == "login":
        cmd_parts.extend(["-m", "login"])
    elif test_type == "register":
        cmd_parts.extend(["-m", "register"])
    elif test_type == "smoke":
        cmd_parts.extend(["-m", "smoke"])
    
    # 添加特定功能文件
    if feature:
        if feature == "login":
            cmd_parts.append("features/login.feature")
        elif feature == "register":
            cmd_parts.append("features/register.feature")
    
    # 添加场景过滤
    if scenario:
        cmd_parts.extend(["-k", f'"{scenario}"'])
    
    # 添加浏览器配置
    if not headless:
        cmd_parts.append("--headed")
    
    # 添加并行执行
    if parallel:
        cmd_parts.extend(["-n", "auto"])
    
    # 添加报告生成
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    if report_format == "html":
        cmd_parts.extend([
            "--html=reports/report.html", 
            "--self-contained-html"
        ])
    elif report_format == "json":
        cmd_parts.extend([
            "--json-report", 
            "--json-report-file=reports/report.json"
        ])
    elif report_format == "allure":
        cmd_parts.extend(["--alluredir=reports/allure-results"])
    elif report_format == "all":
        cmd_parts.extend([
            "--html=reports/report.html", 
            "--self-contained-html",
            "--json-report", 
            "--json-report-file=reports/report.json",
            "--alluredir=reports/allure-results"
        ])
    
    # 添加详细输出
    cmd_parts.extend(["-v", "--tb=short"])
    
    # 执行测试
    cmd = " ".join(cmd_parts)
    print(f"🚀 执行测试命令: {cmd}")
    
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print("✅ 测试执行完成")
        print(stdout)
        
        # 如果生成了Allure报告，提供查看命令
        if "allure" in report_format:
            print("\n📊 查看Allure报告:")
            print("allure serve reports/allure-results")
        
        return True
    else:
        print("❌ 测试执行失败")
        print(stderr)
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="淘贝应用自动化测试运行器")
    
    parser.add_argument(
        "--type", 
        choices=["all", "ui", "api", "login", "register", "smoke"],
        default="all",
        help="测试类型 (默认: all)"
    )
    
    parser.add_argument(
        "--feature",
        choices=["login", "register"],
        help="运行特定功能的测试"
    )
    
    parser.add_argument(
        "--scenario",
        help="运行包含指定关键词的测试场景"
    )
    
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="浏览器类型 (默认: chromium)"
    )
    
    parser.add_argument(
        "--headed",
        action="store_true",
        help="显示浏览器界面 (默认: 无头模式)"
    )
    
    parser.add_argument(
        "--report",
        choices=["html", "json", "allure", "all"],
        default="html",
        help="报告格式 (默认: html)"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="并行执行测试"
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="只设置环境，不运行测试"
    )
    
    args = parser.parse_args()
    
    print("🎯 淘贝应用自动化测试运行器")
    print("=" * 50)
    
    # 设置环境
    if not setup_environment():
        sys.exit(1)
    
    if args.setup:
        print("✅ 环境设置完成，退出")
        return
    
    # 运行测试
    success = run_tests(
        test_type=args.type,
        feature=args.feature,
        scenario=args.scenario,
        browser=args.browser,
        headless=not args.headed,
        report_format=args.report,
        parallel=args.parallel
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()