from playwright.sync_api import sync_playwright

def test_login_and_click_oss():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:5000")

        # 로그인
        page.fill('input#username', 'secloudit-admin')
        page.fill('input#password', 'qwe1212!Q')
        page.click('button#kc-login')

        # 왼쪽 사이드 메뉴의 '설정' 버튼 클릭
        page.click('button:has-text("설정")')

        # 확장된 메뉴의 'OSS' 버튼 클릭
        page.click('a:has-text("OSS")')

        # 결과 페이지 확인 (예: OSS 페이지의 타이틀이 있는지)
        assert page.url.endswith('/oss')
        assert page.inner_text('h5') == 'OSS'

        browser.close()

if __name__ == "__main__":
    test_login_and_click_oss()