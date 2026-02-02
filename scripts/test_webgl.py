"""
测试 Docker Chrome 的 WebGL 支持
"""
import asyncio
from playwright.async_api import async_playwright

async def test_webgl():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        
        # 获取页面
        if browser.contexts and browser.contexts[0].pages:
            page = browser.contexts[0].pages[0]
        else:
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = await context.new_page()
        
        # 测试 WebGL
        result = await page.evaluate('''() => {
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
        
        print('\n🎨 WebGL 测试结果:')
        if 'error' in result:
            print(f'  ❌ {result["error"]}')
        else:
            print(f'  ✅ Vendor: {result["vendor"]}')
            print(f'  ✅ Renderer: {result["renderer"]}')
            print(f'  ✅ Version: {result["version"]}')
            print(f'  ✅ Max Texture Size: {result["maxTextureSize"]}')

if __name__ == "__main__":
    asyncio.run(test_webgl())
