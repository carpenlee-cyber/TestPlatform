import pytest
from playwright.sync_api import sync_playwright, expect
import os
import time

# 基础配置
BASE_URL = "http://localhost:5173"
USERNAME = "admin"
PASSWORD = "admin123"

def run_e2e_test():
    results = []
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. 登录成功并验证跳转到 /dashboard
            print("Step 1: Testing Login and Redirect...")
            page.goto(f"{BASE_URL}/login")
            
            # 等待登录页面加载
            page.wait_for_selector('input[placeholder="请输入用户名"]')
            
            # 输入用户名和密码
            page.fill('input[placeholder="请输入用户名"]', USERNAME)
            page.fill('input[placeholder="请输入密码"]', PASSWORD)
            
            # 监听控制台和网络
            page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
            page.on("requestfailed", lambda request: print(f"Request failed: {request.url} {request.failure.error_text}"))
            page.on("response", lambda response: print(f"Response: {response.status} {response.url}") if "/api/" in response.url else None)

            # 点击登录按钮
            print("Clicking login button...")
            page.click('button:has-text("登 录")')
            
            # 手动轮询
            max_retries = 20
            while max_retries > 0:
                if "/dashboard" in page.url:
                    break
                time.sleep(0.5)
                max_retries -= 1
            
            if "/dashboard" in page.url or page.query_selector(".dashboard-page"):
                results.append({"step": "Login & Redirect", "status": "PASS", "message": "Successfully redirected to /dashboard"})
            else:
                # 检查是否有错误消息
                error_msg = page.query_selector(".el-message")
                msg_text = error_msg.inner_text() if error_msg else "No UI message"
                results.append({"step": "Login & Redirect", "status": "FAIL", "message": f"Redirect failed. Current URL: {page.url}, UI Message: {msg_text}"})
            
            # 2. 验证 Dashboard 统计数据是否加载
            print("Step 2: Verifying Dashboard Stats...")
            # 等待统计卡片中的数值加载（假设非 0 或是通过 API 加载出来的）
            # 我们寻找具有特定类的元素
            page.wait_for_selector(".stat-value")
            stats_elements = page.query_selector_all(".stat-value")
            
            if len(stats_elements) >= 4:
                results.append({"step": "Dashboard Stats", "status": "PASS", "message": f"Found {len(stats_elements)} stat values"})
            else:
                results.append({"step": "Dashboard Stats", "status": "FAIL", "message": f"Found only {len(stats_elements)} stat values"})
            
            # 3. 验证测试用例列表页是否可以正常打开
            print("Step 3: Opening Test Cases Page...")
            # 点击侧边栏或直接跳转
            page.goto(f"{BASE_URL}/test-cases")
            page.wait_for_selector(".test-cases-page", timeout=5000)
            results.append({"step": "Test Cases Page", "status": "PASS", "message": "Test cases page loaded successfully"})
            
            # 4. 验证 Bug 列表页是否可以正常打开
            print("Step 4: Opening Bugs Page...")
            page.goto(f"{BASE_URL}/bugs")
            page.wait_for_selector(".bugs-page", timeout=5000)
            results.append({"step": "Bugs Page", "status": "PASS", "message": "Bugs page loaded successfully"})
            
        except Exception as e:
            print(f"Error during test: {e}")
            results.append({"step": "Global", "status": "ERROR", "message": str(e)})
            # 截图保存现场
            page.screenshot(path="/root/.openclaw/workspace/TestPlatform/test-artifacts/screenshots/e2e_error.png")
        
        finally:
            browser.close()
            
    return results

def generate_report(results):
    report_path = "/root/.openclaw/workspace/TestPlatform/STABILITY-E2E-REPORT.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Stability E2E Test Report\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Environment:** Frontend (5173), Backend (8088)\n\n")
        
        f.write("| Step | Status | Message |\n")
        f.write("| --- | --- | --- |\n")
        
        for res in results:
            status_emoji = "✅" if res["status"] == "PASS" else "❌"
            f.write(f"| {res['step']} | {status_emoji} {res['status']} | {res['message']} |\n")
            
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    test_results = run_e2e_test()
    generate_report(test_results)
