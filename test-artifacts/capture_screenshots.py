import asyncio
from playwright.async_api import async_playwright
import os

async def take_screenshots():
    async with async_playwright() as p:
        # 创建截图目录
        os.makedirs('/root/.openclaw/workspace/TestPlatform/screenshots', exist_ok=True)
        
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # 1. 登录页截图
        print("正在截取登录页面...")
        await page.goto('http://localhost:5173/login')
        await page.wait_for_timeout(2000) # 等待动画
        await page.screenshot(path='/root/.openclaw/workspace/TestPlatform/screenshots/login.png')
        
        # 2. 模拟登录并进入 Dashboard
        print("正在尝试模拟登录...")
        await page.fill('input[placeholder*="用户名"]', 'admin')
        await page.fill('input[placeholder*="密码"]', 'admin123')
        await page.click('button:has-text("登 录")')
        
        # 等待跳转到首页
        await page.wait_for_url('**/dashboard')
        await page.wait_for_timeout(3000) # 等待图表加载
        
        # 3. Dashboard 截图
        print("正在截取控制面板...")
        await page.screenshot(path='/root/.openclaw/workspace/TestPlatform/screenshots/dashboard.png')
        
        # 4. 用例列表截图
        print("正在截取用例中心...")
        await page.goto('http://localhost:5173/testcases')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='/root/.openclaw/workspace/TestPlatform/screenshots/testcases.png')
        
        await browser.close()
        print("所有截图已完成！")

if __name__ == "__main__":
    asyncio.run(take_screenshots())
