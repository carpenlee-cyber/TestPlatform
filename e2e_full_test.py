import json
import time
import os
import random
from playwright.sync_api import sync_playwright, expect

# 基础配置
BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:5173")
ASSETS_PATH = "/root/.openclaw/workspace/TestPlatform/test-artifacts/test_cases_assets.json"
REPORT_PATH = "/root/.openclaw/workspace/TestPlatform/FULL-STABILITY-V3-REPORT.md"
SCREENSHOT_DIR = "/root/.openclaw/workspace/TestPlatform/test-artifacts/screenshots"

def random_delay():
    """频率自律：每个测试步骤间加入 1-2 秒的随机延迟"""
    time.sleep(random.uniform(1.0, 2.0))

def run_step(page, step):
    action = step.get("action")
    params = step.get("params", {})
    description = step.get("description", "Executing step")
    
    print(f"  - Action: {action} | {description}")
    
    if action == "goto":
        url = params.get("url")
        if url.startswith("/"):
            url = f"{BASE_URL}{url}"
        page.goto(url)
    elif action == "fill":
        page.fill(params.get("selector"), str(params.get("value")))
    elif action == "click":
        page.click(params.get("selector"), force=True)
    elif action == "select_option":
        # Click the select first to open dropdown
        page.click(params.get("selector"))
        random_delay()
        # Click the option in the dropdown (ElementPlus uses .el-select-dropdown__item)
        label = params.get("label")
        page.click(f".el-select-dropdown__item:visible:has-text(\"{label}\")")
    elif action == "wait_url":
        target_url = params.get("url")
        page.wait_for_url(lambda url: target_url in url, timeout=10000)
    elif action == "wait_text":
        selector = params.get("selector", "body")
        text = params.get("text")
        expect(page.locator(selector)).to_contain_text(text, timeout=10000)
    elif action == "wait_gone":
        selector = params.get("selector")
        page.wait_for_selector(selector, state="hidden", timeout=10000)
    elif action == "wait_for":
        page.wait_for_selector(params.get("selector"), timeout=10000)
    elif action == "eval":
        result = page.evaluate(params.get("expression"))
        if not result:
            raise Exception(f"Evaluation failed for: {params.get('expression')}")
    else:
        raise Exception(f"Unknown action: {action}")
    
    random_delay()

def run_test_case(page, test_case):
    print(f"Running TC: {test_case['id']} - {test_case['name']}")
    steps = test_case.get("steps", [])
    
    try:
        for step in steps:
            run_step(page, step)
        return {"status": "PASS", "message": "All steps completed successfully"}
    except Exception as e:
        screenshot_path = f"{SCREENSHOT_DIR}/error_{test_case['id']}.png"
        page.screenshot(path=screenshot_path)
        print(f"  [ERROR] {e} | Screenshot: {screenshot_path}")
        return {"status": "FAIL", "message": str(e)}

def generate_report(results):
    total = len(results)
    passed = len([r for r in results if r["status"] == "PASS"])
    failed = total - passed
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# FULL STABILITY V3 E2E REPORT\n\n")
        f.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Environment:** {BASE_URL}\n")
        f.write(f"**Summary:** Total: {total} | Passed: {passed} | Failed: {failed}\n\n")
        
        f.write("| ID | Name | Status | Message |\n")
        f.write("| --- | --- | --- | --- |\n")
        for res in results:
            emoji = "✅" if res["status"] == "PASS" else "❌"
            f.write(f"| {res['id']} | {res['name']} | {emoji} {res['status']} | {res['message']} |\n")

    print(f"Report generated at: {REPORT_PATH}")

def main():
    if not os.path.exists(ASSETS_PATH):
        print(f"Assets file not found: {ASSETS_PATH}")
        return

    with open(ASSETS_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 增加超时时间以应对可能的卡顿
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(15000)
        
        # 监听错误
        page.on("requestfailed", lambda request: print(f"  [DEBUG] Request failed: {request.url} ({request.failure.error_text})"))
        
        for tc in test_cases:
            res = run_test_case(page, tc)
            res.update({"id": tc["id"], "name": tc["name"]})
            results.append(res)
            
        browser.close()

    generate_report(results)

if __name__ == "__main__":
    main()
