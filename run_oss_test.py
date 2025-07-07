from playwright.sync_api import sync_playwright
from module.oss_module import login, create_oss, delete_oss
from module.infra_module import create_infra, delete_infra
from module.service_module import create_service, delete_service, move_project_build
import time
from log_config import setup_logging

# 로깅 설정
setup_logging()

def main():
    oss_list = [
        {
            "name": "test-git",
            "desc": "test-git",
            "url": "https://gitlab-local.innogrid.com",
            "type": "Gitlab",
            "username": "root",
            "password": "qwe1212!Q",
            "token": ""
        },
        {
            "name": "test-jenkins",
            "desc": "test-jenkins",
            "url": "https://jenkins-local.innogrid.com",
            "type": "Jenkins",
            "username": "admin",
            "token": ""
        },
        {
            "name": "test-argocd",
            "desc": "test-argocd",
            "url": "https://argocd-local.innogrid.com",
            "type": "Argocd",
            "username": "admin",
            "password": "qwe1212!Q"
        },
        {
            "name": "test-harbor",
            "desc": "test-harbor",
            "url": "https://harbor-local.innogrid.com",
            "type": "Harbor",
            "username": "admin",
            "password": "qwe1212!Q"
        },
        {
            "name": "test-k8s",
            "desc": "test-k8s",
            "url": "https://192.168.190.45:6443",
            "type": "K8s",
            "kubeconfig": "k8s_config.yaml"
        },
        {
            "name": "test-sonarqube",
            "desc": "test-sonarqube",
            "url": "https://sonarqube-local.innogrid.com",
            "type": "Sonarqube",
            "username": "admin",
            "password": "qwe1212!Q"
        }
    ]
    oss_names = [oss["name"] for oss in oss_list]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        login(page, "secloudit-admin", "qwe1212!Q")
        # create_oss(page, oss_list)
        # time.sleep(4)
        # create_infra(page, oss_list)
        create_service(page)
        move_project_build(page)

        # delete_service(page)
        # time.sleep(6)
        # delete_infra(page)
        # delete_oss(page, oss_names)
        time.sleep(6)
        browser.close()

if __name__ == "__main__":
    main() 