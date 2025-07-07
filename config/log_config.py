import logging
import logging.handlers

def setup_logging():
    """
    프로젝트 전반에 사용될 로깅을 설정합니다.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,  # INFO 레벨 이상의 로그를 모두 출력
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # 콘솔에 로그 출력
            logging.handlers.RotatingFileHandler(
                'app.log',          # 로그 파일 이름
                maxBytes=10*1024*1024, # 10MB
                backupCount=5       # 최대 5개 로그 파일 유지
            )
        ]
    )
