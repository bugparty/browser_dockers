"""
Docker Chrome 浏览器自动化测试工具

功能：
- 连接 Docker 容器中运行的 Chrome 浏览器
- 支持页面导航、截图、JavaScript 执行
- WebGL 检测
- 反爬虫指纹检测
- 浏览器特征测试

使用方法：
    python chrome_automation.py

依赖：
    pip install playwright

前置条件：
    1. Docker 容器正在运行: docker ps | findstr chrome
    2. 端口 9222 已映射: localhost:9222 -> container:9223
"""

import asyncio
from playwright.async_api import async_playwright
from typing import Optional
import sys


class ChromeAutomation:
    def __init__(self, cdp_url: str = "http://localhost:9222"):
        self.cdp_url = cdp_url
        self.browser = None
        self.page = None
        
    async def connect(self):
        """连接到 Chrome 浏览器"""
        print(f"🔗 正在连接到 Chrome ({self.cdp_url})...")
        playwright = await async_playwright().start()
        
        try:
            self.browser = await playwright.chromium.connect_over_cdp(self.cdp_url)
            print(f"✅ 已连接到浏览器 v{self.browser.version}")
            
            # 获取或创建页面
            contexts = self.browser.contexts
            if contexts and contexts[0].pages:
                self.page = contexts[0].pages[0]
            else:
                context = contexts[0] if contexts else await self.browser.new_context()
                self.page = await context.new_page()
                
            print(f"📄 当前页面: {self.page.url}")
            return True
            
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            print("\n💡 排查步骤：")
            print("1. 检查容器运行: docker ps")
            print("2. 检查端口映射: docker port <容器名>")
            print("3. 测试端点: curl http://localhost:9222/json/version")
            return False
    
    async def goto(self, url: str, wait_until: str = "networkidle"):
        """访问指定 URL"""
        if not self.page:
            print("❌ 未连接到浏览器")
            return False
            
        print(f"\n🌐 正在访问: {url}")
        try:
            await self.page.goto(url, wait_until=wait_until)
            await asyncio.sleep(1)
            title = await self.page.title()
            print(f"📌 页面标题: {title}")
            return True
        except Exception as e:
            print(f"❌ 访问失败: {e}")
            return False
    
    async def screenshot(self, filename: str = "screenshot.png"):
        """截图"""
        if not self.page:
            return False
            
        try:
            await self.page.screenshot(path=filename)
            print(f"📸 截图已保存: {filename}")
            return True
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False
    
    async def check_webgl(self) -> dict:
        """检测 WebGL 支持"""
        if not self.page:
            return {"error": "未连接"}
            
        result = await self.page.evaluate('''() => {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (!gl) return { error: 'WebGL 不可用' };
            
            const info = gl.getExtension('WEBGL_debug_renderer_info');
            return {
                vendor: gl.getParameter(info.UNMASKED_VENDOR_WEBGL),
                renderer: gl.getParameter(info.UNMASKED_RENDERER_WEBGL),
                version: gl.getParameter(gl.VERSION),
                maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE)
            };
        }''')
        
        return result
    
    async def check_fingerprint(self) -> dict:
        """检测浏览器指纹"""
        if not self.page:
            return {}
            
        result = await self.page.evaluate('''() => {
            return {
                userAgent: navigator.userAgent,
                webdriver: navigator.webdriver,
                platform: navigator.platform,
                language: navigator.language,
                hardwareConcurrency: navigator.hardwareConcurrency,
                deviceMemory: navigator.deviceMemory,
                screenResolution: `${screen.width}x${screen.height}`,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                cookieEnabled: navigator.cookieEnabled
            };
        }''')
        
        return result
    
    async def run_demo(self):
        """运行演示测试"""
        if not await self.connect():
            return
        
        # 1. 检测浏览器指纹
        print("\n🔍 浏览器指纹检测:")
        fingerprint = await self.check_fingerprint()
        for key, value in fingerprint.items():
            status = "✅" if (key == "webdriver" and value == False) else "ℹ️"
            print(f"  {status} {key}: {value}")
        
        # 2. 检测 WebGL
        print("\n🎨 WebGL 支持检测:")
        webgl = await self.check_webgl()
        if 'error' in webgl:
            print(f"  ❌ {webgl['error']}")
        else:
            print(f"  ✅ Vendor: {webgl['vendor']}")
            print(f"  ✅ Renderer: {webgl['renderer']}")
            print(f"  ✅ Version: {webgl['version']}")
            print(f"  ✅ Max Texture Size: {webgl['maxTextureSize']}")
        
        # 3. 访问反爬虫检测网站
        if await self.goto("https://bot.sannysoft.com"):
            await asyncio.sleep(3)
            await self.screenshot("bot_detection.png")
        
        # 4. 访问示例网站
        if await self.goto("https://www.example.com"):
            await self.screenshot("example.png")
        
        print("\n✨ 演示完成！")
        print("提示：浏览器将继续运行，可通过 VNC (localhost:5900) 查看")
        print("按 Ctrl+C 断开连接...")
        
        try:
            await asyncio.sleep(300)
        except KeyboardInterrupt:
            print("\n👋 正在断开连接...")


async def main():
    """主函数"""
    automation = ChromeAutomation()
    await automation.run_demo()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        sys.exit(0)
