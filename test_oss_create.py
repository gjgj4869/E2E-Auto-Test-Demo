from playwright.sync_api import sync_playwright
import time

def test_oss_create():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:5000")
        # 로그인
        page.fill('input#username', 'secloudit-admin')
        page.fill('input#password', 'qwe1212!Q')
        # page.click('submit:has-text("SIGN IN")')
        page.click('#kc-login')

        time.sleep(2)

        # 왼쪽 메뉴 '설정' 클릭
        page.click('button:has-text("설정")')
        # 확장 메뉴 'OSS' 클릭
        page.click('a:has-text("OSS")')
        
        # + 생성 버튼 클릭
        page.click('button:has-text("생성")')

        time.sleep(2)
        
        # 팝업 입력
        page.fill('input[placeholder="이름 입력"]', 'test-git')
        page.fill('textarea[placeholder="설명 입력"]', 'test-git')
        page.fill('input[placeholder="URL 입력"]', 'https://gitlab-local.innogrid.com')
        # 유형 콤보박스 (react-select)
        page.fill('input[id^="react-select"][type="text"]', 'Gitlab')
        page.keyboard.press('Enter')
        # 사용자명/비밀번호/토큰
        page.fill('input[placeholder="사용자명 입력"]', 'root')
        page.fill('input[placeholder="비밀번호 입력"]', 'qwe1212!Q')
        page.fill('input[placeholder="토큰 입력"]', '')
        
        # 생성 버튼 클릭 (팝업 오른쪽 아래)
        popup = page.locator('[role="dialog"]')  # 팝업을 감싸는 컨테이너
        popup.locator('button:has-text("생성")').click()
        # page.click('button:has-text("생성")')

        time.sleep(3)

        ##Jenkins 생성
        # + 생성 버튼 클릭
        page.click('button:has-text("생성")')

        time.sleep(2)

        page.fill('input[placeholder="이름 입력"]', 'test-jenkins')
        page.fill('textarea[placeholder="설명 입력"]', 'test-jenkins')
        page.fill('input[placeholder="URL 입력"]', 'https://jenkins-local.innogrid.com')
        # 유형 콤보박스 (react-select)
        page.fill('input[id^="react-select"][type="text"]', 'Jenkins')
        page.keyboard.press('Enter')
        # 사용자명/비밀번호/토큰
        page.fill('input[placeholder="사용자명 입력"]', 'admin')
        page.fill('input[placeholder="토큰 입력"]', '')
        
        # 생성 버튼 클릭 (팝업 오른쪽 아래)
        popup = page.locator('[role="dialog"]')  # 팝업을 감싸는 컨테이너
        popup.locator('button:has-text("생성")').click()

        time.sleep(3)
        
        #oss 삭제
        clear_oss(page)

        # 결과 확인을 위해 잠시 대기
        time.sleep(6)
        browser.close()

def clear_oss(page):
    # 1. "test-git"이 포함된 행 찾기
    row = page.locator('tr', has_text="test-git")
    # 삭제 버튼 클릭 (두 번째 svg 버튼)
    row.locator('button:has(svg)').nth(1).click()

    # 2. 팝업 등장 대기 (role="dialog" 기준)
    dialog = page.locator('[role="dialog"]')
    dialog.wait_for(state="visible", timeout=5000)

    # # 3. 입력창에 "test-git" 입력
    dialog.locator('input[type="text"]').fill("test-git")

    # # 4. 팝업 내부 오른쪽 아래 "삭제" 버튼 클릭
    dialog.locator('button:has-text("삭제")').click()

    time.sleep(3)
    
    # 1. "test-jenkins"이 포함된 행 찾기
    row = page.locator('tr', has_text="test-jenkins")
    row.locator('button:has(svg)').nth(1).click()

    # 2. 팝업 등장 대기 (role="dialog" 기준)
    dialog = page.locator('[role="dialog"]')
    dialog.wait_for(state="visible", timeout=5000)

    # # 3. 입력창에 "test-git" 입력
    dialog.locator('input[type="text"]').fill("test-jenkins")

    # # 4. 팝업 내부 오른쪽 아래 "삭제" 버튼 클릭
    dialog.locator('button:has-text("삭제")').click()

    time.sleep(3)

if __name__ == "__main__":
    test_oss_create() 
