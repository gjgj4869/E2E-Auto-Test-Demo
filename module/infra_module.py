from playwright.sync_api import sync_playwright, TimeoutError
import time
import logging

# 각 모듈에 로거 설정
logger = logging.getLogger(__name__)

def create_infra(page, oss_list):
    try:
        page.click('button:has-text("설정")')
        # 확장 메뉴 '자원' 클릭
        page.click('a:has-text("자원")')
        logger.info("Navigated to Infra page.")

        page.click('button:has-text("생성")')
        page.get_by_role("textbox", name="이름 입력").fill("test-localstack")
        page.get_by_role("textbox", name="설명 입력").fill("test-localstack")
        page.get_by_text("Gitlab 선택").click()
        page.get_by_role("option", name="test-git").click()
        page.get_by_text("Jenkins 선택").click()
        page.get_by_role("option", name="test-jenkins").click()
        page.get_by_text("ArgoCD 선택").click()
        page.get_by_role("option", name="test-argocd").click()
        page.get_by_text("Harbor 선택").click()
        page.get_by_role("option", name="test-harbor").click()
        page.get_by_text("K8S 선택").click()
        page.get_by_role("option", name="test-k8s").click()
        page.get_by_text("Sonarqube 선택").click()
        page.get_by_role("option", name="test-sonarqube").click()
        
        # "생성" 버튼 클릭 및 API 응답 검증
        try:
            with page.expect_response("**/api/graphql") as response_info:
                page.get_by_role("button", name="생성").click()
            
            response = response_info.value
            if not response.ok:
                response_body = response.text()
                error_message = f"Failed to create Infra 'test-localstack' via API. Status: {response.status}, Response: {response_body}"
                logger.error(error_message)
                raise Exception(error_message)
            
            logger.info(f"Successfully created Infra 'test-localstack'. API call was successful (Status: {response.status}).")
            time.sleep(1)

        except Exception as e:
            logger.error(f"An error occurred while creating Infra 'test-localstack'. Error: {e}")
            raise

    except Exception as e:
        logger.error(f"Failed to navigate to Infra page or complete Infra creation. Error: {e}")
        raise

def delete_infra(page):
    try:
        page.click('button:has-text("설정")')
        # 확장 메뉴 '자원' 클릭
        page.click('a:has-text("자원")')
        logger.info("Navigated to Infra page for deletion.")

        row = page.locator('tr', has_text="test-localstack")
        # 삭제 버튼 클릭 (두 번째 svg 버튼)
        row.locator('button:has(svg)').nth(1).click()

        # 팝업 등장 대기
        dialog = page.locator('[role="dialog"]')
        dialog.wait_for(state="visible", timeout=5000)

        # 입력창에 이름 입력
        dialog.locator('input[type="text"]').fill("test-localstack")

        # "삭제" 버튼 클릭 및 API 응답 검증
        try:
            with page.expect_response("**/api/graphql") as response_info:
                dialog.locator('button:has-text("삭제")').click()
            
            response = response_info.value
            if not response.ok:
                response_body = response.text()
                error_message = f"Failed to delete Infra 'test-localstack' via API. Status: {response.status}, Response: {response_body}"
                logger.error(error_message)
                raise Exception(error_message)
            
            logger.info(f"Successfully deleted Infra 'test-localstack'. API call was successful (Status: {response.status}).")
            time.sleep(2)

        except Exception as e:
            logger.error(f"An error occurred while deleting Infra 'test-localstack'. Error: {e}")
            raise

    except Exception as e:
        logger.error(f"Failed to navigate to Infra page or complete Infra deletion. Error: {e}")
        raise