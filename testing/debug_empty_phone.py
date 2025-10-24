from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('http://localhost:5173/login')
    
    # 等待页面加载
    time.sleep(2)
    
    # 清空手机号输入框（如果有内容）
    phone_input = page.locator('input[placeholder*="手机号"], input[name="phone"], #phone')
    if phone_input.count() > 0:
        phone_input.first.clear()
        print('手机号输入框已清空')
    
    # 点击获取验证码按钮
    get_code_btn = page.locator('button:has-text("获取验证码"), .get-code-btn, #get-code')
    if get_code_btn.count() > 0:
        get_code_btn.first.click()
        print('已点击获取验证码按钮')
    
    # 等待可能的错误消息
    time.sleep(3)
    
    # 检查页面上所有可见的文本
    all_elements = page.locator('*').all()
    print('\n页面上的所有可见文本:')
    for element in all_elements:
        try:
            if element.is_visible():
                text = element.text_content().strip()
                if text and len(text) < 100:  # 只显示短文本
                    print(f'  - {text}')
        except:
            continue
    
    browser.close()