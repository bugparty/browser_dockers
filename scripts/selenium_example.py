"""
使用 Selenium 连接 Docker Chrome（需要匹配的 ChromeDriver）

注意：推荐使用 chrome_automation.py (Playwright 版本)，无需管理驱动
此脚本仅供参考，需要额外安装 ChromeDriver
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def connect_with_selenium():
    """使用 Selenium 连接"""
    
    # 方法1：自动下载匹配的 ChromeDriver（推荐）
    try:
        options = Options()
        options.debugger_address = "127.0.0.1:9222"
        
        print("🔗 正在连接到 Chrome (Selenium)...")
        print("提示：首次运行会自动下载 ChromeDriver...")
        
        # 自动管理 ChromeDriver 版本
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"✅ 已连接")
        print(f"当前 URL: {driver.current_url}")
        
        # 测试操作
        driver.get('https://www.example.com')
        time.sleep(2)
        print(f"页面标题: {driver.title}")
        
        driver.save_screenshot('selenium_test.png')
        print("📸 截图已保存")
        
        time.sleep(5)
        driver.quit()
        
    except Exception as e:
        print(f"❌ Selenium 连接失败: {e}")
        print("\n推荐方案：")
        print("使用 chrome_automation.py (Playwright)")
        print("命令: python scripts/chrome_automation.py")
        return
    
    # 方法2：手动指定 ChromeDriver 路径
    # options = Options()
    # options.debugger_address = "127.0.0.1:9222"
    # service = Service(executable_path='/path/to/chromedriver')
    # driver = webdriver.Chrome(service=service, options=options)


if __name__ == "__main__":
    print("=" * 60)
    print("⚠️  推荐使用 Playwright 版本（chrome_automation.py）")
    print("=" * 60)
    print()
    
    # 检查依赖
    try:
        import selenium
        import webdriver_manager
        print("✅ 依赖已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("\n安装命令：")
        print("pip install selenium webdriver-manager")
        exit(1)
    
    connect_with_selenium()
