from playwright.sync_api import sync_playwright, TimeoutError
import time
import logging

# 각 모듈에 로거 설정
logger = logging.getLogger(__name__)

def create_service(page):
    try:
        page.locator("a").filter(has_text="서비스").click()
        time.sleep(2)
        logger.info("Navigated to Service page.")

        page.click('button:has-text("생성")')
        time.sleep(2)
        page.get_by_role("textbox", name="이름 입력", exact=True).click()
        page.get_by_role("textbox", name="이름 입력", exact=True).fill("test-devopsit-service-01")
        page.get_by_role("textbox", name="설명 입력").click()
        page.get_by_role("textbox", name="설명 입력").fill("test-devopsit-service-01")
        page.get_by_role("textbox", name="프로젝트 이름 입력").click()
        page.get_by_role("textbox", name="프로젝트 이름 입력").fill("test-devopsit-project-01")
        page.get_by_text("자원 선택").click()
        page.get_by_role("option", name="test-localstack").click()
        page.get_by_text("스타트 킷 선택").click()
        page.get_by_role("option", name="React").click()
        
        # "생성" 버튼 클릭 및 API 응답 검증
        try:
            with page.expect_response("**/api/graphql") as response_info:
                page.get_by_role("button", name="생성").click()
            
            response = response_info.value
            if not response.ok:
                response_body = response.text()
                error_message = f"Failed to create Service 'test-devopsit-service-01' via API. Status: {response.status}, Response: {response_body}"
                logger.error(error_message)
                raise Exception(error_message)
            
            logger.info(f"Successfully created Service 'test-devopsit-service-01'. API call was successful (Status: {response.status}).")
            time.sleep(2)

        except Exception as e:
            logger.error(f"An error occurred while creating Service 'test-devopsit-service-01'. Error: {e}")
            raise

    except Exception as e:
        logger.error(f"Failed to navigate to Service page or complete Service creation. Error: {e}")
        raise

TARGET_TEXT = "GIT_SOURCE_REPOSITORY_URL"

def move_project_build(page):
    page.locator("a").filter(has_text="서비스").click()
    time.sleep(2)

    # 서비스 링크를 찾을 때까지 최대 5번 새로고침하며 시도
    for attempt in range(5):
        try:
            # 10초의 타임아웃으로 서비스 링크를 찾습니다.
            service_link = page.get_by_role("link", name="test-devopsit-service-01")
            service_link.wait_for(state="visible", timeout=10000)
            service_link.click()
            print("✅ 'test-devopsit-service-01' 서비스를 클릭했습니다.")
            break  # 성공 시 루프 탈출
        except TimeoutError:
            print(f"⏳ 서비스를 찾지 못했습니다. (시도 {attempt + 1}/5)")
            if attempt < 4:
                print("🔁 페이지를 새로고침하고 다시 시도합니다.")
                page.reload(wait_until="domcontentloaded")
                time.sleep(2)  # 새로고침 후 UI 안정화를 위한 대기
            else:
                print("❌ 5번 시도했지만 서비스를 찾지 못했습니다. 테스트를 중단합니다.")
                raise # 5번 모두 실패 시 에러 발생

    # row = page.locator('tr', has_text="test-devopsit-service-01")
    # row.click()

    page.get_by_role("link", name="프로젝트").nth(2).click()

    # project_row = page.locator('tr', has_text="test-devopsit-project-01")
    # project_row.click()
    page.get_by_role("link", name="test-devopsit-project-01").click()

    page.locator("a").filter(has_text="파이프라인 구성").click()

    for attempt in range(10):
        print(f"🔁 새로고침 시도 {attempt + 1}회...")
        page.reload(wait_until="domcontentloaded")

        time.sleep(5)

        try:
            # 텍스트가 있는 요소를 찾을 수 있는지 확인
            page.locator(f"text={TARGET_TEXT}").wait_for(timeout=2000)
            print("✅ 원하는 텍스트를 찾았습니다!")
            break
        except TimeoutError:
            print("⏳ 아직 텍스트가 보이지 않음, 다음 새로고침으로 재시도")

    
    page.locator("div:nth-child(6) > .grid > div:nth-child(2) > .w-full > .form-input").click()
    page.locator("div:nth-child(6) > .grid > div:nth-child(2) > .w-full > .form-input").fill("latest")
    page.get_by_text("save저장").click()
    page.get_by_text("build빌드").click()

def delete_service(page):
    page.locator("a").filter(has_text="서비스").click()
    time.sleep(2)

    row = page.locator('tr', has_text="test-devopsit-service-01")
    # 삭제 버튼 클릭 (두 번째 svg 버튼)
    row.locator('button:has(svg)').nth(1).click()

    # 팝업 등장 대기 (role="dialog" 기준)
    dialog = page.locator('[role="dialog"]')
    dialog.wait_for(state="visible", timeout=5000)

    # 입력창에 입력
    dialog.locator('input[type="text"]').fill("test-devopsit-service-01")

    # 팝업 내부 오른쪽 아래 "삭제" 버튼 클릭
    dialog.locator('button:has-text("삭제")').click()

    time.sleep(4)