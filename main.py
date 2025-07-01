import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class E2ETestAutomation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E2E 테스트 자동화 프로그램")
        self.root.geometry("800x800")
        
        self.driver = None
        self.test_steps = []
        self.current_step = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 설정 섹션
        setup_frame = ttk.LabelFrame(main_frame, text="테스트 설정", padding="10")
        setup_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # URL 입력
        ttk.Label(setup_frame, text="테스트 사이트 URL:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.url_var = tk.StringVar(value="http://localhost:5000/")
        ttk.Entry(setup_frame, textvariable=self.url_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # 로그인 ID
        ttk.Label(setup_frame, text="로그인 ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.id_var = tk.StringVar(value="secloudit-admin")
        ttk.Entry(setup_frame, textvariable=self.id_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # 로그인 Password
        ttk.Label(setup_frame, text="로그인 Password:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.pw_var = tk.StringVar(value="qwe1212!Q")
        ttk.Entry(setup_frame, textvariable=self.pw_var, width=50, show="*").grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # ID 입력란 selector
        ttk.Label(setup_frame, text="ID 입력란 selector 타입:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.login_id_selector_type_var = tk.StringVar(value="ID")
        ttk.Combobox(setup_frame, textvariable=self.login_id_selector_type_var, values=["ID", "CLASS_NAME", "TAG_NAME", "CSS_SELECTOR", "XPATH"], state="readonly", width=15).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.login_id_selector_type_var.set("ID")
        ttk.Label(setup_frame, text="ID 입력란 selector 값:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.login_id_selector_var = tk.StringVar(value="username")
        ttk.Entry(setup_frame, textvariable=self.login_id_selector_var, width=50).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        # PW 입력란 selector
        ttk.Label(setup_frame, text="PW 입력란 selector 타입:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.login_pw_selector_type_var = tk.StringVar(value="ID")
        ttk.Combobox(setup_frame, textvariable=self.login_pw_selector_type_var, values=["ID", "CLASS_NAME", "TAG_NAME", "CSS_SELECTOR", "XPATH"], state="readonly", width=15).grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.login_pw_selector_type_var.set("ID")
        ttk.Label(setup_frame, text="PW 입력란 selector 값:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.login_pw_selector_var = tk.StringVar(value="password")
        ttk.Entry(setup_frame, textvariable=self.login_pw_selector_var, width=50).grid(row=6, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        # 로그인 버튼 selector
        ttk.Label(setup_frame, text="로그인 버튼 selector 타입:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.login_btn_selector_type_var = tk.StringVar(value="ID")
        ttk.Combobox(setup_frame, textvariable=self.login_btn_selector_type_var, values=["ID", "CLASS_NAME", "TAG_NAME", "CSS_SELECTOR", "XPATH"], state="readonly", width=15).grid(row=7, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.login_btn_selector_type_var.set("ID")
        ttk.Label(setup_frame, text="로그인 버튼 selector 값:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.login_btn_selector_var = tk.StringVar(value="kc-login")
        ttk.Entry(setup_frame, textvariable=self.login_btn_selector_var, width=50).grid(row=8, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # 브라우저 시작 버튼
        ttk.Button(setup_frame, text="브라우저 시작 및 로그인", command=self.start_browser).grid(row=9, column=0, columnspan=2, pady=10)
        
        # 테스트 단계 섹션
        steps_frame = ttk.LabelFrame(main_frame, text="테스트 단계 추가", padding="10")
        steps_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 액션 타입 선택
        ttk.Label(steps_frame, text="액션 타입:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.action_var = tk.StringVar()
        action_combo = ttk.Combobox(steps_frame, textvariable=self.action_var, values=[
            "클릭", "텍스트 입력", "대기", "스크롤", "호버"
        ], state="readonly", width=15)
        action_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        action_combo.current(0)
        
        # 선택자 타입
        ttk.Label(steps_frame, text="선택자 타입:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        self.selector_type_var = tk.StringVar()
        selector_combo = ttk.Combobox(steps_frame, textvariable=self.selector_type_var, values=[
            "ID", "CLASS_NAME", "TAG_NAME", "CSS_SELECTOR", "XPATH"
        ], state="readonly", width=15)
        selector_combo.grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=2)
        selector_combo.current(0)
        
        # 선택자 값
        ttk.Label(steps_frame, text="선택자 값:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.selector_var = tk.StringVar()
        ttk.Entry(steps_frame, textvariable=self.selector_var, width=30).grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # 입력 값 (텍스트 입력시 사용)
        ttk.Label(steps_frame, text="입력 값:").grid(row=1, column=3, sticky=tk.W, padx=(20, 0), pady=2)
        self.input_value_var = tk.StringVar()
        ttk.Entry(steps_frame, textvariable=self.input_value_var, width=20).grid(row=1, column=4, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # 대기 시간
        ttk.Label(steps_frame, text="대기 시간(초):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.wait_time_var = tk.StringVar(value="3")
        ttk.Entry(steps_frame, textvariable=self.wait_time_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 단계 추가 버튼
        ttk.Button(steps_frame, text="단계 추가", command=self.add_step).grid(row=2, column=2, padx=(20, 0), pady=2)
        
        # 테스트 실행 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="테스트 실행", command=self.run_test).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="단계별 실행", command=self.run_step_by_step).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="테스트 중지", command=self.stop_test).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="브라우저 종료", command=self.close_browser).pack(side=tk.LEFT)
        
        # 테스트 단계 목록 및 로그
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # 테스트 단계 목록
        ttk.Label(list_frame, text="테스트 단계 목록:").grid(row=0, column=0, sticky=tk.W)
        
        steps_listframe = ttk.Frame(list_frame)
        steps_listframe.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.steps_listbox = tk.Listbox(steps_listframe, height=10)
        self.steps_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        steps_scrollbar = ttk.Scrollbar(steps_listframe, orient=tk.VERTICAL, command=self.steps_listbox.yview)
        steps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_listbox.config(yscrollcommand=steps_scrollbar.set)
        
        # 로그 영역
        ttk.Label(list_frame, text="실행 로그:").grid(row=0, column=1, sticky=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(list_frame, height=10, width=40)
        self.log_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 단계 삭제 버튼
        ttk.Button(list_frame, text="선택된 단계 삭제", command=self.delete_step).grid(row=2, column=0, pady=(5, 0))
        ttk.Button(list_frame, text="로그 지우기", command=self.clear_log).grid(row=2, column=1, pady=(5, 0))
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.columnconfigure(1, weight=1)
        list_frame.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def log(self, message):
        """로그 메시지 추가"""
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def start_browser(self):
        """브라우저 시작 및 로그인"""
        if not self.url_var.get():
            messagebox.showerror("오류", "URL을 입력해주세요.")
            return
        try:
            self.log("브라우저를 시작하는 중...")
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            self.log(f"사이트 접속: {self.url_var.get()}")
            self.driver.get(self.url_var.get())
            # 브라우저가 열린 뒤 자동 로그인 시도
            self.auto_login()
        except Exception as e:
            self.log(f"브라우저 시작 실패: {str(e)}")
            messagebox.showerror("오류", f"브라우저 시작 실패: {str(e)}")

    def auto_login(self):
        """자동 로그인 동작"""
        id_type = self.login_id_selector_type_var.get()
        id_selector = self.login_id_selector_var.get()
        pw_type = self.login_pw_selector_type_var.get()
        pw_selector = self.login_pw_selector_var.get()
        btn_type = self.login_btn_selector_type_var.get()
        btn_selector = self.login_btn_selector_var.get()
        id_value = self.id_var.get()
        pw_value = self.pw_var.get()
        by_map = {
            'ID': By.ID,
            'CLASS_NAME': By.CLASS_NAME,
            'TAG_NAME': By.TAG_NAME,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'XPATH': By.XPATH
        }
        if id_type and id_selector and pw_type and pw_selector and btn_type and btn_selector:
            try:
                wait = WebDriverWait(self.driver, 10)
                id_elem = wait.until(EC.presence_of_element_located((by_map[id_type], id_selector)))
                pw_elem = wait.until(EC.presence_of_element_located((by_map[pw_type], pw_selector)))
                btn_elem = wait.until(EC.element_to_be_clickable((by_map[btn_type], btn_selector)))
                # 입력창 클릭 후 값 입력
                id_elem.click()
                id_elem.clear()
                id_elem.send_keys(id_value)
                self.log("ID 입력 완료")
                pw_elem.click()
                pw_elem.clear()
                pw_elem.send_keys(pw_value)
                self.log("PW 입력 완료")
                # 로그인 버튼 클릭
                btn_elem.click()
                self.log("로그인 버튼 클릭 완료 (자동 로그인 시도)")
            except Exception as e:
                self.log(f"자동 로그인 실패: {str(e)}")
                messagebox.showwarning("경고", f"자동 로그인 실패: {str(e)}")
        else:
            self.log("자동 로그인 정보가 부족합니다. 수동으로 로그인하세요.")

    def add_step(self):
        """테스트 단계 추가"""
        action = self.action_var.get()
        selector_type = self.selector_type_var.get()
        selector = self.selector_var.get()
        input_value = self.input_value_var.get()
        wait_time = self.wait_time_var.get()
        
        if action in ["클릭", "텍스트 입력", "호버"] and not selector:
            messagebox.showerror("오류", "선택자 값을 입력해주세요.")
            return
            
        step = {
            'action': action,
            'selector_type': selector_type,
            'selector': selector,
            'input_value': input_value,
            'wait_time': int(wait_time) if wait_time.isdigit() else 3
        }
        
        self.test_steps.append(step)
        
        # 리스트박스에 표시
        step_text = f"{len(self.test_steps)}. {action}"
        if selector:
            step_text += f" - {selector_type}: {selector}"
        if input_value and action == "텍스트 입력":
            step_text += f" (값: {input_value})"
        if action == "대기":
            step_text += f" - {wait_time}초"
            
        self.steps_listbox.insert(tk.END, step_text)
        
        # 입력 필드 초기화
        self.selector_var.set("")
        self.input_value_var.set("")
        
        self.log(f"단계 추가됨: {step_text}")
        
    def delete_step(self):
        """선택된 단계 삭제"""
        selection = self.steps_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 단계를 선택해주세요.")
            return
            
        index = selection[0]
        self.test_steps.pop(index)
        self.steps_listbox.delete(index)
        
        # 리스트박스 번호 다시 매기기
        self.steps_listbox.delete(0, tk.END)
        for i, step in enumerate(self.test_steps):
            step_text = f"{i+1}. {step['action']}"
            if step['selector']:
                step_text += f" - {step['selector_type']}: {step['selector']}"
            if step['input_value'] and step['action'] == "텍스트 입력":
                step_text += f" (값: {step['input_value']})"
            if step['action'] == "대기":
                step_text += f" - {step['wait_time']}초"
            self.steps_listbox.insert(tk.END, step_text)
            
        self.log("단계가 삭제되었습니다.")
        
    def get_element(self, selector_type, selector):
        """요소 찾기"""
        wait = WebDriverWait(self.driver, 10)
        
        by_map = {
            'ID': By.ID,
            'CLASS_NAME': By.CLASS_NAME,
            'TAG_NAME': By.TAG_NAME,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'XPATH': By.XPATH
        }
        
        try:
            element = wait.until(EC.presence_of_element_located((by_map[selector_type], selector)))
            return element
        except TimeoutException:
            raise Exception(f"요소를 찾을 수 없습니다: {selector_type}={selector}")
            
    def execute_step(self, step):
        """단계 실행"""
        action = step['action']
        
        try:
            if action == "클릭":
                element = self.get_element(step['selector_type'], step['selector'])
                # 요소가 클릭 가능할 때까지 대기
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable((getattr(By, step['selector_type']), step['selector'])))
                element.click()
                self.log(f"클릭 완료: {step['selector']}")
                
            elif action == "텍스트 입력":
                element = self.get_element(step['selector_type'], step['selector'])
                element.clear()
                element.send_keys(step['input_value'])
                self.log(f"텍스트 입력 완료: {step['selector']} = {step['input_value']}")
                
            elif action == "대기":
                time.sleep(step['wait_time'])
                self.log(f"대기 완료: {step['wait_time']}초")
                
            elif action == "스크롤":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.log("페이지 하단으로 스크롤")
                
            elif action == "호버":
                element = self.get_element(step['selector_type'], step['selector'])
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                self.log(f"호버 완료: {step['selector']}")
                
            # 각 단계 후 잠시 대기
            time.sleep(1)
            
        except Exception as e:
            self.log(f"단계 실행 실패: {str(e)}")
            raise e
            
    def run_test(self):
        """전체 테스트 실행"""
        if not self.driver:
            messagebox.showerror("오류", "먼저 브라우저를 시작해주세요.")
            return
            
        if not self.test_steps:
            messagebox.showerror("오류", "테스트 단계를 추가해주세요.")
            return
            
        def run_in_thread():
            try:
                self.log("=== 테스트 실행 시작 ===")
                for i, step in enumerate(self.test_steps):
                    self.log(f"단계 {i+1} 실행 중...")
                    self.execute_step(step)
                    
                self.log("=== 테스트 실행 완료 ===")
                messagebox.showinfo("완료", "모든 테스트 단계가 완료되었습니다.")
                
            except Exception as e:
                self.log(f"테스트 실행 중 오류 발생: {str(e)}")
                messagebox.showerror("오류", f"테스트 실행 실패: {str(e)}")
                
        threading.Thread(target=run_in_thread, daemon=True).start()
        
    def run_step_by_step(self):
        """단계별 실행"""
        if not self.driver:
            messagebox.showerror("오류", "먼저 브라우저를 시작해주세요.")
            return
            
        if not self.test_steps:
            messagebox.showerror("오류", "테스트 단계를 추가해주세요.")
            return
            
        if self.current_step >= len(self.test_steps):
            messagebox.showinfo("완료", "모든 단계가 완료되었습니다.")
            self.current_step = 0
            return
            
        def run_single_step():
            try:
                step = self.test_steps[self.current_step]
                self.log(f"단계 {self.current_step + 1} 실행 중...")
                self.execute_step(step)
                self.current_step += 1
                
                if self.current_step >= len(self.test_steps):
                    self.log("=== 모든 단계 완료 ===")
                    self.current_step = 0
                    
            except Exception as e:
                self.log(f"단계 실행 중 오류 발생: {str(e)}")
                messagebox.showerror("오류", f"단계 실행 실패: {str(e)}")
                
        threading.Thread(target=run_single_step, daemon=True).start()
        
    def stop_test(self):
        """테스트 중지"""
        self.current_step = 0
        self.log("테스트가 중지되었습니다.")
        
    def close_browser(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.log("브라우저가 종료되었습니다.")
        else:
            messagebox.showinfo("정보", "실행 중인 브라우저가 없습니다.")
            
    def clear_log(self):
        """로그 지우기"""
        self.log_text.delete(1.0, tk.END)
        
    def run(self):
        """프로그램 실행"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """프로그램 종료시 정리"""
        if self.driver:
            self.driver.quit()
        self.root.destroy()

if __name__ == "__main__":
    # 필요한 패키지 설치 안내
    try:
        import selenium
    except ImportError:
        print("selenium 패키지가 필요합니다. 다음 명령어로 설치하세요:")
        print("pip install selenium")
        exit(1)
        
    print("E2E 테스트 자동화 프로그램을 시작합니다...")
    print("주의: ChromeDriver가 설치되어 있어야 합니다.")
    print("https://chromedriver.chromium.org/ 에서 다운로드 후 PATH에 추가하세요.")
    
    app = E2ETestAutomation()
    app.run()