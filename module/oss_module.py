from playwright.sync_api import sync_playwright
import time
import logging

# 각 모듈에 로거 설정
logger = logging.getLogger(__name__)

def login(page, username, password):
    try:
        page.goto("http://localhost:5000")
        page.fill('input#username', username)
        page.fill('input#password', password)
        page.click('#kc-login')
        time.sleep(2)
        logger.info(f"Successfully logged in with user: {username}")
    except Exception as e:
        logger.error(f"Failed to login with user: {username}. Error: {e}")
        raise

def create_oss(page, oss_list):
    try:
        # 왼쪽 메뉴 '설정' 클릭
        page.click('button:has-text("설정")')
        # 확장 메뉴 'OSS' 클릭
        page.click('a:has-text("OSS")')
        logger.info("Navigated to OSS page.")

        for oss in oss_list:
            try:
                page.click('button:has-text("생성")')
                time.sleep(2)
                page.fill('input[placeholder="이름 입력"]', oss["name"])
                page.fill('textarea[placeholder="설명 입력"]', oss["desc"])
                page.fill('input[placeholder="URL 입력"]', oss["url"])
                page.fill('input[id^="react-select"][type="text"]', oss["type"])
                page.keyboard.press('Enter')
                if oss.get("username"):
                    page.fill('input[placeholder="사용자명 입력"]', oss["username"])
                if oss.get("password"):
                    page.fill('input[placeholder="비밀번호 입력"]', oss["password"])
                if oss.get("token"):
                    page.fill('input[placeholder="토큰 입력"]', oss["token"])
                if oss.get("kubeconfig"):
                    page.get_by_role("checkbox").check()
                    with open(oss["kubeconfig"], "r") as f:
                        k8s_config = f.read()
                        page.fill('textarea[placeholder="KubeConfig 입력"]', k8s_config)
                popup = page.locator('[role="dialog"]')
                
                # "생성" 버튼 클릭으로 인해 발생하는 GraphQL API 응답을 기다립니다.
                # **매우 중요:** 아래의 URL 패턴은 실제 API 엔드포인트에 맞게 수정해야 합니다.
                # 브라우저 개발자 도구의 네트워크 탭에서 확인하세요.
                try:
                    with page.expect_response("**/api/graphql") as response_info:
                        popup.locator('button:has-text("생성")').click()
                    
                    response = response_info.value
                    
                    # 응답 상태 코드가 2xx가 아닌 경우 실패로 간주합니다.
                    if not response.ok:
                        response_body = response.text()
                        error_message = f"Failed to create OSS '{oss['name']}' via API. Status: {response.status}, Response: {response_body}"
                        logger.error(error_message)
                        raise Exception(error_message)
                    
                    logger.info(f"Successfully created OSS '{oss['name']}'. API call was successful (Status: {response.status}).")
                    time.sleep(1) # UI가 안정화될 시간을 잠시 줍니다.

                except Exception as e:
                    # expect_response 타임아웃 또는 기타 예외 처리
                    logger.error(f"An error occurred while creating OSS '{oss['name']}'. Error: {e}")
                    raise
            except Exception as e:
                logger.error(f'Failed to create OSS: {oss["name"]}. Error: {e}')
                # Optionally re-raise or handle the error
    except Exception as e:
        logger.error(f"Failed to navigate to OSS page or complete OSS creation. Error: {e}")
        raise

def delete_oss(page, oss_names):
    try:
        # 왼쪽 메뉴 '설정' 클릭
        page.click('button:has-text("설정")')
        # 확장 메뉴 'OSS' 클릭
        page.click('a:has-text("OSS")')
        logger.info("Navigated to OSS page for deletion.")

        for name in oss_names:
            try:
                row = page.locator('tr', has_text=name)
                row.locator('button:has(svg)').nth(1).click()
                dialog = page.locator('[role="dialog"]')
                dialog.wait_for(state="visible", timeout=5000)
                time.sleep(1)
                dialog.locator('input[type="text"]').fill(name)
                time.sleep(1)
                
                # "삭제" 버튼 클릭 및 API 응답 검증
                try:
                    with page.expect_response("**/api/graphql") as response_info:
                        dialog.locator('button:has-text("삭제")').click()
                    
                    response = response_info.value
                    if not response.ok:
                        response_body = response.text()
                        error_message = f"Failed to delete OSS '{name}' via API. Status: {response.status}, Response: {response_body}"
                        logger.error(error_message)
                        raise Exception(error_message)
                    
                    logger.info(f"Successfully deleted OSS '{name}'. API call was successful (Status: {response.status}).")
                    time.sleep(2)

                except Exception as e:
                    logger.error(f"An error occurred while deleting OSS '{name}'. Error: {e}")
                    raise
            except Exception as e:
                logger.error(f"Failed to delete OSS: {name}. Error: {e}")
                # Optionally re-raise or handle the error
    except Exception as e:
        logger.error(f"Failed to navigate to OSS page or complete OSS deletion. Error: {e}")
        raise 