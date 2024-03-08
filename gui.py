__version__ = "0.0.3"
import logging, webbrowser, time, subprocess, threading
import customtkinter as ctk
import utils as ut

from ctk_tooltip import CTkToolTip
from tkinter import scrolledtext, messagebox


# NOTE 제발 코드 정리좀 하자
# NOTE 단축키 가격 수정 기능, 영도 및 텍스트 룰렛 등 세부, ico 포함 안 하면 에러남 해결하기
# NOTE url 글자 수 부족할때 경고메세지 후 작업 중단이 안되고 그대로 실행되는 문제 있음 + toggle_enable_on_stop() 호출 하는데 event 필요하다고 뜸

def log_monitor(log_file_path, text_widget, root):
    last_line = ""
    with open(log_file_path, "r", encoding='utf-8') as file:
        file.seek(0,2)  # 파일의 끝으로 이동
        while True:
            current_line = file.readline().strip()
            if current_line != last_line and current_line != "":
                # print(current_line[7:])  # 콘솔에 변경된 줄 표시
                last_line = current_line
                # 메인 스레드에서 GUI 업데이트
                show_line = current_line[11:].replace(' - donater', '').replace(' - INFO -', '')
                root.after(1, lambda: update_text_widget(text_widget, show_line + "\n"))
            time.sleep(0.1)  # 항상 0.1초 대기

def update_text_widget(text_widget, line):
    text_widget.configure(state='normal')
    text_widget.insert(ctk.END, line)
    text_widget.configure(state='disabled')
    text_widget.yview(ctk.END)

def start_log_monitor(log_file_path, text_widget, root):  # 로그 모니터링 스레드 시작
    threading.Thread(target=log_monitor, args=(log_file_path, text_widget, root), daemon=True).start()   


settings = ut.load_settings()
if settings['system']['debug']:
    logger = ut.setup_logger('donater', 'logs/donater.log', level=logging.DEBUG)
else:
    logger = ut.setup_logger('donater', 'logs/donater.log', level=logging.INFO)


def open_link(event):
    webbrowser.open('https://chzzk.naver.com/451758d2f5fdf831c7650d717e379560')

def open_czz_link(event):
    webbrowser.open('https://chzzk.naver.com/451758d2f5fdf831c7650d717e379560')

def change_cursor(event):
    event.widget.configure(cursor="hand2")

def btn_click_event(event):
    global settings
    settings = ut.load_settings()
    settings['afreecahp']['use'] = afreecahp_var.get()
    settings['twip']['use'] = twip_var.get()
    settings['toonation']['use'] = toonation_var.get()
    settings['shortcut']['use'] = shotcut_var.get()
    settings['warudo']['use'] = warudo_var.get()
    settings['discord']['use'] = discord_var.get()

    settings['afreecahp']['alertbox_url'] = input1.get()
    settings['twip']['alertbox_url'] = input2.get()
    settings['toonation']['alertbox_url'] = input3.get()
    settings['discord']['webhook_url'] = input4.get()

    ut.save_settings(settings=settings)
    

def toggle_enable(event, enable=True):
    # 대상 위젯들의 활성화/비활성화 상태를 설정합니다.
    # 예시로, shotcut_setting_btn과 warudo_setting_btn의 상태를 변경합니다.
    widgets = [afreecahp_con, input1, twip_con, input2, toonation_con, input3, 
               discord_con, input4, start_btn, shotcut_con, shotcut_setting_btn, warudo_con, warudo_setting_btn]

    state = "normal" if enable else "disabled"
    for widget in widgets:
        widget.configure(state=state)

def update_button_state():
    global is_shotcut_setting_btn_enabled, is_warudo_setting_btn_enabled
    # 단축키 설정 버튼 상태 업데이트
    if is_shotcut_setting_btn_enabled: shotcut_setting_btn.configure(cursor="hand2")
    else: shotcut_setting_btn.configure(cursor="arrow") 
    # 와루도 설정 버튼 상태 업데이트
    if is_warudo_setting_btn_enabled: warudo_setting_btn.configure(cursor="hand2")
    else: warudo_setting_btn.configure(cursor="arrow")


def toggle_enable_on_start(event):
    global is_shotcut_setting_btn_enabled, is_warudo_setting_btn_enabled
    stop_btn.configure(state="normal")
    is_shotcut_setting_btn_enabled = is_warudo_setting_btn_enabled = False
    start_btn.configure(cursor='arrow')
    stop_btn.configure(cursor="hand2")
    update_button_state()  # 버튼 상태 업데이트 호출

def toggle_enable_on_stop(event):
    global is_shotcut_setting_btn_enabled, is_warudo_setting_btn_enabled
    stop_btn.configure(state="disabled")
    is_shotcut_setting_btn_enabled = is_warudo_setting_btn_enabled = True
    start_btn.configure(cursor='hand2')
    stop_btn.configure(cursor="arrow")
    update_button_state()  # 버튼 상태 업데이트 호출


def delete_shortcut(event, price):  # 단축키 설정에서 해당 가격의 단축키를 삭제합니다.
    global settings
    if price in settings['shortcut']:
        del settings['shortcut'][price]
        ut.save_settings(settings)  # 변경사항을 저장합니다.
        settings = ut.load_settings()  # 설정을 다시 불러와서 UI를 업데이트합니다.
        open_shortcut_settings()  # 이 함수를 호출하여 단축키 설정 창을 다시 열어서 변경사항을 반영합니다.

def add_shortcut():
    global settings, add_price_input, ctrl_var, shift_var, alt_var, add_key_input
    # 입력된 가격과 단축키 정보를 가져옵니다.
    price = int(add_price_input.get())
    ctrl = ctrl_var.get()
    shift = shift_var.get()
    alt = alt_var.get()
    key = add_key_input.get()

    # 단축키 문자열을 생성합니다.
    shortcut = ""
    if ctrl: shortcut += "Ctrl+"
    if shift: shortcut += "Shift+"
    if alt: shortcut += "Alt+"
    shortcut += key

    # 설정에 단축키를 추가합니다.
    settings['shortcut'][price] = shortcut

    ut.save_settings(settings)  # 변경사항을 저장합니다.
    settings = ut.load_settings()  # 설정을 다시 불러와서 UI를 업데이트합니다.
    open_shortcut_settings()  # 단축키 설정 창을 새로고침합니다.

# donate_croll 프로세스를 관리하기 위한 전역 변수
donate_croll_process = None
def start_donate_croll():
    # 서비스별 설정을 리스트로 관리
    services = [
        (afreecahp_var, input1, 23, "아프리카 도우미의 알림 주소를 올바르게 입력해 주세요."),
        (twip_var, input2, 33, "트윕의 알림 주소를 올바르게 입력해 주세요."),
        (toonation_var, input3, 32, "투네이션의 알림 주소를 올바르게 입력해 주세요."),
        (discord_var, input4, 53, "디스코드 웹훅의 주소를 올바르게 입력해 주세요.")
    ]

    warning_flag = False
    for var, input_field, min_length, warning_message in services:
        if var.get() and len(input_field.get()) < min_length:
            messagebox.showwarning("경고", warning_message)
            warning_flag = True
            break  # 첫 번째 경고 메시지가 표시된 후 반복을 중단합니다.

    # settings['shortcut']['use'] = shotcut_var.get()
    # settings['warudo']['use'] = warudo_var.get()

    if warning_flag:
        stop_donate_croll()
        toggle_enable_on_stop()
        return
    else:
        logger.info('#################################')
        logger.info('##### 도네이션 연동을 시작했다굴~ #####')
        logger.info('#################################')
        global donate_croll_process
        settings = ut.load_settings()
        settings['system']['status'] = 'live'
        ut.save_settings(settings=settings)
        # donate_croll.exe 실행
        donate_croll_process = subprocess.Popen(['server.exe', '--startwith', 'true'])
    
def stop_donate_croll():
    global donate_croll_process, settings
    settings = ut.load_settings()
    settings['system']['status'] = 'stop'
    ut.save_settings(settings=settings)

    # donate_croll.exe 종료
    if donate_croll_process is not None:
        logger.info('#################################')
        logger.info('##### 도네이션 연동을 종료한다굴~ #####')
        logger.info('#################################')
        for _ in range(100):  # 100번 반복
            settings = ut.load_settings()
            status = settings['system']['status']
            if status == 'stopped':
                break
            else:
                time.sleep(0.5)
        donate_croll_process.terminate()
        donate_croll_process = None

def on_closing():
    logger.info('#################################')
    logger.info('####### 프로그램을 종료한다굴~ #######')
    logger.info('#################################')
    stop_donate_croll()
    root.destroy()

# GUI 창을 생성
root = ctk.CTk()
root.title("도네이션 연동")
root.resizable(False, False)  # 가로세로 창의 크기 고정
root.iconbitmap('ico.ico')  # 아이콘인데 위에 노트 참고


screen_width = root.winfo_screenwidth()  # 가로 해상도
screen_height = root.winfo_screenheight()  # 세로 해상도

# 창을 화면 중앙에 배치하기 위한 x, y 좌표를 계산합니다.
x_coordinate = int(screen_width / 3)
y_coordinate = int(screen_height / 3)
root.geometry(f"+{x_coordinate}+{y_coordinate}")

custom_font = checkbox_font = ("맑은 고딕", 14, "bold")
console_font = ("맑은 고딕", 10)

# 초기 상태 설정
is_shotcut_setting_btn_enabled = is_warudo_setting_btn_enabled = is_system_setting_btn_enabled = True
shortcut_window = warudo_window = system_window = None
 
# 체크박스 상태를 저장할 변수들을 생성합니다.
afreecahp_var = ctk.BooleanVar(value=settings['afreecahp']['use'])
twip_var = ctk.BooleanVar(value=settings['twip']['use'])
toonation_var = ctk.BooleanVar(value=settings['toonation']['use'])
shotcut_var = ctk.BooleanVar(value=settings['shortcut']['use'])
warudo_var = ctk.BooleanVar(value=settings['warudo']['use'])
discord_var = ctk.BooleanVar(value=settings['discord']['use'])

debugmode_var = ctk.BooleanVar(value=settings['system']['debug'])
loadimg_var = ctk.BooleanVar(value=settings['system']['load_images'])

# 메인 윈도우 row 0 - 아프리카도우미 설정
afreecahp_con = ctk.CTkCheckBox(root, text="아프리카 연동", variable=afreecahp_var, font=checkbox_font)
afreecahp_con.grid(row=0, column=0, sticky="w", padx=(10,5), pady=10)
afreecahp_tooltip = CTkToolTip(afreecahp_con, message="아프리카 도우미 연동을 활성화합니다.", font=checkbox_font, alpha=0.8)
input1 = ctk.CTkEntry(root, width=400, font=custom_font, show="*")
input1.insert(0, settings['afreecahp']['alertbox_url'])
input1.grid(row=0, column=1, columnspan=4, sticky="w", padx=10)
input1_tooltip = CTkToolTip(input1, message="아프리카 도우미 알림 주소를 입력해주세요.", font=checkbox_font, alpha=0.8)
show_btn1 = ctk.CTkButton(root, text="V", font=checkbox_font, width=30)
show_btn1.grid(row=0, column=5, sticky="w", padx=(0,10))
show_btn1_tooltip = CTkToolTip(show_btn1, message="알림 주소를 확인할 수 있습니다.", font=checkbox_font, alpha=0.8)

# 메인 윈도우 row 1 - 트윕 설정
twip_con = ctk.CTkCheckBox(root, text="트윕 연동", variable=twip_var, font=checkbox_font)
twip_con.grid(row=1, column=0, sticky="w", padx=(10,5), pady=10)
twip_con_tooltip = CTkToolTip(twip_con, message="트윕 연동을 활성화합니다.", font=checkbox_font, alpha=0.8)
input2 = ctk.CTkEntry(root, width=400, font=custom_font, show="*")
input2.insert(0, settings['twip']['alertbox_url'])
input2.grid(row=1, column=1, columnspan=4, sticky="w", padx=10)
input2_tooltip = CTkToolTip(input2, message="트윕 알림 주소를 입력해주세요.", font=checkbox_font, alpha=0.8)
show_btn2 = ctk.CTkButton(root, text="V", font=checkbox_font, width=30)
show_btn2.grid(row=1, column=5, sticky="w", padx=(0,10))
show_btn2_tooltip = CTkToolTip(show_btn2, message="알림 주소를 확인할 수 있습니다.", font=checkbox_font, alpha=0.8)

# 메인 윈도우 row 2 - 투네이션 설정
toonation_con = ctk.CTkCheckBox(root, text="투네이션 연동", variable=toonation_var, font=checkbox_font)
toonation_con.grid(row=2, column=0, sticky="w", padx=(10,5), pady=10)
toonation_con_tooltip = CTkToolTip(toonation_con, message="투네이션 연동을 활성화합니다.", font=checkbox_font, alpha=0.8)
input3 = ctk.CTkEntry(root, width=400, font=custom_font, show="*")
input3.insert(0, settings['toonation']['alertbox_url'])
input3.grid(row=2, column=1, columnspan=4, sticky="w", padx=10)
input3_tooltip = CTkToolTip(input3, message="투네이션 알림 주소를 입력해주세요.", font=checkbox_font, alpha=0.8)
show_btn3 = ctk.CTkButton(root, text="V", font=checkbox_font, width=30)
show_btn3.grid(row=2, column=5, sticky="w", padx=(0,10))
show_btn3_tooltip = CTkToolTip(show_btn3, message="알림 주소를 확인할 수 있습니다.", font=checkbox_font, alpha=0.8)

# 메인 윈도우 row 3 - 디스코드 설정
discord_con = ctk.CTkCheckBox(root, text="디스코드 웹훅", variable=discord_var, font=checkbox_font)
discord_con.grid(row=3, column=0, sticky="w", padx=(10,5), pady=10)
discord_con_tooltip = CTkToolTip(discord_con, message="디스코드 웹훅 전송을 활성화합니다.", font=checkbox_font, alpha=0.8)
input4 = ctk.CTkEntry(root, width=400, font=custom_font, show="*")
input4.insert(0, settings['discord']['webhook_url'])
input4.grid(row=3, column=1, columnspan=4, sticky="w", padx=10)
input4_tooltip = CTkToolTip(input4, message="디스코드 웹훅 주소를 입력해주세요.", font=checkbox_font, alpha=0.8)
show_btn4 = ctk.CTkButton(root, text="V", font=checkbox_font, width=30)
show_btn4.grid(row=3, column=5, sticky="w", padx=(0,10))
show_btn4_tooltip = CTkToolTip(show_btn4, message="웹훅 주소를 확인할 수 있습니다.", font=checkbox_font, alpha=0.8)

# 메인 윈도우 row 4 - 연동 시작, 단축키 사용 및 설정, 와루도 사용 및 설정, 시스템 설정 
start_btn = ctk.CTkButton(root, text="연동 시작", font=custom_font, fg_color="#50FA7B", text_color='#282A36')
start_btn.grid(row=4, column=0, sticky="w", padx=10, pady=5)
start_btn.configure(cursor='hand2')
shotcut_con = ctk.CTkCheckBox(root, text="단축키 사용", variable=shotcut_var, font=checkbox_font)
shotcut_con.grid(row=4, column=1, sticky="w", padx=(10,10), pady=10)
shotcut_con_tooltip = CTkToolTip(shotcut_con, message="단축키 사용을 활성화합니다.", font=checkbox_font, alpha=0.8)
shotcut_setting_btn = ctk.CTkButton(root, text="단-설정", font=checkbox_font, width=30)
shotcut_setting_btn.grid(row=4, column=2, sticky="w", padx=(10,10))
shotcut_setting_btn.configure(cursor='hand2')
shotcut_setting_btn_tooltip = CTkToolTip(shotcut_setting_btn, message="가격대별 단축키 설정", font=checkbox_font, alpha=0.8)
warudo_con = ctk.CTkCheckBox(root, text="와루도 연동", variable=warudo_var, font=checkbox_font)
warudo_con.grid(row=4, column=3, sticky="w", padx=(10,10), pady=10)
warudo_con_tooltip = CTkToolTip(warudo_con, message="와루도 연동을 활성화합니다. 구독자 전용", font=checkbox_font, alpha=0.8)
warudo_setting_btn = ctk.CTkButton(root, text="와-설정", font=checkbox_font, width=30)
warudo_setting_btn.grid(row=4, column=4, sticky="w", padx=(10,10))
warudo_setting_btn.configure(cursor='hand2')
warudo_setting_btn_tooltip = CTkToolTip(warudo_setting_btn, message="와루도 연결 설정", font=checkbox_font, alpha=0.8)
like_btn = ctk.CTkButton(root, text="S", font=checkbox_font, width=30)
like_btn.grid(row=4, column=5, sticky="w", padx=(0,10))
like_btn_tooltip = CTkToolTip(like_btn, message="기분이 좋아지는 버튼", font=checkbox_font, alpha=0.8)

# 메인 윈도우 row 5 - 연동 정지, 크레딧
stop_btn = ctk.CTkButton(root, text="연동 정지", font=custom_font, state="disabled", fg_color="#FF5555", text_color='#282A36')
stop_btn.grid(row=5, column=0, sticky="w", padx=10, pady=5)
credit_label = ctk.CTkLabel(root, text="Made for 효굴효굴, Made by 사미육 | 2024-03-03", font=custom_font)
credit_label.grid(row=5, column=1, columnspan=5, sticky="w", padx=10)
credit_label.bind("<Button-1>", open_link)

# 메인 윈도우 row 6 - 콘솔박스
console_box = scrolledtext.ScrolledText(root, height=4, bg="#282A36", fg="#F8F8F2", font=console_font)
console_box.grid(row=6, column=0, columnspan=6, pady=5, padx=10)
console_box.configure(state='disabled')  # 초기 상태를 읽기 전용으로 설정

# 비밀번호를 보여주는 상태를 추적하는 변수들입니다.
password_shown1 = password_shown2 = password_shown3 = password_shown4 = False

def toggle_password_all(event):
    global password_shown3, password_shown2, password_shown1, password_shown4
    input1.configure(show="*")
    password_shown1 = False
    input2.configure(show="*")
    password_shown2 = False
    input3.configure(show="*")
    password_shown3 = False
    input4.configure(show="*")
    password_shown4 = False

def open_shortcut_settings():
    global is_shotcut_setting_btn_enabled, settings, shortcut_window
    global add_price_input, ctrl_var, shift_var, alt_var, add_key_input
    if not is_shotcut_setting_btn_enabled:
        return
    
    if shortcut_window is not None:  # 기존 단축키 설정 창이 열려있으면 닫음 -> 새로고침 됨
        shortcut_window.destroy()
        shortcut_window = None

    root.withdraw()  # 단축키 창 설정
    shortcut_window = ctk.CTkToplevel(root)
    shortcut_window.resizable(False, False)
    shortcut_window.title("단축키 설정")
    # shortcut_window.iconbitmap('ico.ico')  # 아이콘 설정 확인 해야함 하고 노트 남기기
    shortcut_settings = settings['shortcut']
    shortcut_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # 새 창 위치

    def on_closing():  # 새 창이 닫힐 때 실행될 함수
        global shortcut_window
        root.deiconify()  # 메인 창을 다시 보이게
        shortcut_window.destroy()
        shortcut_window = None  # 창 참조를 제거
    shortcut_window.protocol("WM_DELETE_WINDOW", on_closing)

    # 단축키 창 row 0
    text = "별풍선, 애드벌룬 자동으로 변환됩니다. 효굴효굴 치지직 놀러가기"
    info_label = ctk.CTkLabel(shortcut_window, text=text, font=custom_font)
    info_label.grid(row=0, column=0, columnspan=6, sticky="w", padx=10, pady=10)
    info_label.bind("<Enter>", change_cursor)
    info_label.bind("<Button-1>", open_czz_link)

    row_index = 1  # 아래는 단축키 반복 표시문
    for price, shortcut in shortcut_settings.items():
        if price == 'use':
            continue  # 'use' 키는 설정 값이 아니므로 건너뜁니다.

        price_label = ctk.CTkLabel(shortcut_window, text="가격(원)", font=custom_font)
        price_label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        price_input = ctk.CTkEntry(shortcut_window, width=100, font=custom_font)
        price_input.insert(1, price)
        price_input.grid(row=row_index, column=1, sticky="w", padx=5)
        spacer_label = ctk.CTkLabel(shortcut_window, text=":", font=custom_font)
        spacer_label.grid(row=row_index, column=2, sticky="w", padx=10, pady=5)
        action_label = ctk.CTkLabel(shortcut_window, text="단축키", font=custom_font)
        action_label.grid(row=row_index, column=3, sticky="w", padx=10, pady=5)
        action_input = ctk.CTkEntry(shortcut_window, width=250, font=custom_font)
        action_input.insert(1, shortcut)
        action_input.grid(row=row_index, column=4, columnspan=3, sticky="w", padx=5)

        # TODO 삭제버튼 창 새로고침 없이 바로 업데이트 수정 -> 후 순위
        del_btn = ctk.CTkButton(shortcut_window, text="-", font=checkbox_font, width=30)
        del_btn.grid(row=row_index, column=7, sticky="w", padx=(5,10))
        del_btn.bind("<Enter>", change_cursor)
        del_btn.bind("<Button-1>", lambda event, price=price: delete_shortcut(event, price))  # 삭제 버튼에 이벤트 바인딩
        row_index += 1

    add_shortcut_label = ctk.CTkLabel(shortcut_window, text='단축키 추가', font=custom_font) 
    add_shortcut_label.grid(row=row_index + 1, column=0, columnspan=6, sticky="w", padx=10, pady=(15, 5))
    add_shortcut_label_tooltip = CTkToolTip(add_shortcut_label, message="단축키 수정은 동일 금액 입력후 새로 사용할 단축키를 선택해 주세요", font=checkbox_font, alpha=0.8)
    
    add_price_label = ctk.CTkLabel(shortcut_window, text="가격(원)", font=custom_font)
    add_price_label.grid(row=row_index + 2, column=0, sticky="w", padx=10, pady=5)
    add_price_input = ctk.CTkEntry(shortcut_window, width=100, font=custom_font)
    add_price_input.grid(row=row_index + 2, column=1, sticky="w", padx=5)
    spacer_label = ctk.CTkLabel(shortcut_window, text=":", font=custom_font)
    spacer_label.grid(row=row_index + 2, column=2, sticky="w", padx=10, pady=5)

    ctrl_var = ctk.BooleanVar()
    shift_var = ctk.BooleanVar()
    alt_var = ctk.BooleanVar()

    available_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", \
                      "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",\
                      "num0", "num1", "num2", "num3", "num4", "num5", "num6", "num7", "num8", "num9", \
                    #   "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", \
                      "Left", "Right", "Up", "Down", "esc", "space", "BackSpace", "Enter", "Tab", "Delete", "Insert", "Home", "End", "PageUp", "PageDown"]  # 사용 가능한 키 목록

    add_ctrl_key = ctk.CTkCheckBox(shortcut_window, text="Ctrl", variable=ctrl_var, width=60, font=checkbox_font)
    add_ctrl_key.grid(row=row_index + 2, column=3, sticky="w", padx=5, pady=10)
    add_shift_key = ctk.CTkCheckBox(shortcut_window, text="Shift", variable=shift_var, width=60, font=checkbox_font)
    add_shift_key.grid(row=row_index + 2, column=4, sticky="w", padx=5, pady=10)
    add_alt_key = ctk.CTkCheckBox(shortcut_window, text="Alt", variable=alt_var, width=60, font=checkbox_font)
    add_alt_key.grid(row=row_index + 2, column=5, sticky="w", padx=5, pady=10)
    add_key_input = ctk.CTkOptionMenu(shortcut_window, values=available_keys, width=100, font=custom_font)
    add_key_input.grid(row=row_index + 2, column=6, sticky="w", padx=5)
    add_btn = ctk.CTkButton(shortcut_window, text="+", font=checkbox_font, width=30)
    add_btn.grid(row=row_index + 2, column=7, sticky="w", padx=(5,10))
    add_btn.bind("<Enter>", change_cursor)
    add_btn.bind("<Button-1>", lambda event: add_shortcut())


def open_warudo_settings():
    global is_warudo_setting_btn_enabled
    if not is_warudo_setting_btn_enabled:
        return
    # customtkinter 스타일의 새 창 생성
    root.withdraw()
    warudo_window = ctk.CTkToplevel(root)
    warudo_window.resizable(False, False)  # 창의 크기 조절을 비활성화합니다.
    warudo_window.title("와루도 설정")
    warudo_window.iconbitmap('ico.ico')
    
    # 새 창 크기 및 위치 설정
    # warudo_window.geometry("400x300")
    warudo_window.geometry(f"+{x_coordinate}+{y_coordinate}")

        # 새 창이 닫힐 때 실행될 함수
    def on_closing():
        # 기존 창 다시 보이게 하기
        root.deiconify()
        # 새 창 닫기
        warudo_window.destroy()
    warudo_window.protocol("WM_DELETE_WINDOW", on_closing)

    # 새 창 내용 예시
    port_label = ctk.CTkLabel(warudo_window, text="연결 포트", font=custom_font)
    port_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    port_input = ctk.CTkEntry(warudo_window, width=100, font=custom_font)
    port_input.insert(0, settings['warudo']['port'])
    port_input.grid(row=0, column=1, sticky="w", padx=10)

    action_label = ctk.CTkLabel(warudo_window, text="연결 액션", font=custom_font)
    action_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
    action_input = ctk.CTkEntry(warudo_window, width=100, font=custom_font)
    action_input.insert(0, settings['warudo']['action'])
    action_input.grid(row=1, column=1, sticky="w", padx=10)

    noti_label1 = ctk.CTkLabel(warudo_window, text="기능은 더 추가될 예정입니다~ ", font=custom_font)
    noti_label1.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)
    noti_label2 = ctk.CTkLabel(warudo_window, text="효굴효굴 치지직 놀러가기", font=custom_font)
    noti_label2.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)
    noti_label2.bind("<Enter>", change_cursor)
    noti_label2.bind("<Button-1>", open_czz_link)

def open_system_settings():
    global is_system_setting_btn_enabled, debugmode_var, loadimg_var, settings, save_btn
    if not is_system_setting_btn_enabled:
        return
    settings = ut.load_settings()
    # customtkinter 스타일의 새 창 생성
    root.withdraw()
    system_window = ctk.CTkToplevel(root)
    system_window.resizable(False, False)  # 창의 크기 조절을 비활성화합니다.
    system_window.title("시스템 설정")
    system_window.iconbitmap('ico.ico')
    
    # 새 창 크기 및 위치 설정
    system_window.geometry(f"+{x_coordinate}+{y_coordinate}")

        # 새 창이 닫힐 때 실행될 함수
    def on_closing():
        # 기존 창 다시 보이게 하기
        root.deiconify()
        # 새 창 닫기
        system_window.destroy()

    def savebtn_click_event(event):
        global settings
        settings = ut.load_settings()
        settings['system']['cycle_time'] = cycletime.get()
        settings['system']['debug'] = debugmode_var.get()
        settings['system']['load_images'] = loadimg_var.get()
        ut.save_settings(settings=settings)

    system_window.protocol("WM_DELETE_WINDOW", on_closing)

    system_label = ctk.CTkLabel(system_window, text="시스템 설정", font=custom_font)
    system_label.grid(row=0, column=0, columnspan=1, sticky="w", padx=10)

    debug_chk = ctk.CTkCheckBox(system_window, text="디버깅 모드", variable=debugmode_var, font=checkbox_font)
    debug_chk.grid(row=1, column=0, columnspan=1, sticky="w", padx=(10,5), pady=10)
    debug_chk_tooltip = CTkToolTip(debug_chk, message="디버깅 모드를 활성화합니다.", font=checkbox_font, alpha=0.8)

    img_chk = ctk.CTkCheckBox(system_window, text="이미지 로드", variable=loadimg_var, font=checkbox_font)
    img_chk.grid(row=2, column=0, columnspan=1, sticky="w", padx=(10,5), pady=10)
    img_chk_tooltip = CTkToolTip(img_chk, message="이미지 로드를 활성화합니다.", font=checkbox_font, alpha=0.8)

    cycletime_label = ctk.CTkLabel(system_window, text="순환사이클 총 시간(초)", font=custom_font)
    cycletime_label.grid(row=3, column=0, columnspan=1, sticky="ew", padx=10)

    cycletime = ctk.CTkEntry(system_window, width=50, font=custom_font)
    cycletime.insert(0, settings['system']['cycle_time'])
    cycletime.grid(row=3, column=1, columnspan=1, sticky="w", padx=10)

    build_info_label = ctk.CTkLabel(system_window, text="빌드 버전", font=custom_font)
    build_info_label.grid(row=4, column=0, columnspan=1, sticky="ew", padx=10)

    build_label = ctk.CTkLabel(system_window, text=settings['system']['build'], font=custom_font)
    build_label.grid(row=4, column=1, columnspan=1, sticky="w", padx=10)

    version_info_label = ctk.CTkLabel(system_window, text="빌드 버전", font=custom_font)
    version_info_label.grid(row=5, column=0, columnspan=1, sticky="ew", padx=10)

    version_label = ctk.CTkLabel(system_window, text='GUI 0.0.3, Server 0.0.2', font=custom_font)
    version_label.grid(row=5, column=1, columnspan=1, sticky="w", padx=10)

    license = ctk.CTkLabel(system_window, text="사용 라이브러리 및 라이센스", font=custom_font)
    license.grid(row=6, column=0,  columnspan=1, sticky="ew", padx=10)

    license_text = f'CustomTkinter - MIT\nCTKToolTip - CC0 1.0\npyppeteer - MIT\nPuppeteer - Apache-2.0'
    license1 = ctk.CTkLabel(system_window, text=license_text, font=custom_font)
    license1.grid(row=7, column=0, columnspan=1, sticky="ew", padx=10)

    save_btn = ctk.CTkButton(system_window, text="설정 저장", font=custom_font)
    save_btn.grid(row=8, column=0, columnspan=1, sticky="w", padx=10, pady=5)
    save_btn.configure(cursor='hand2')
    save_btn.bind("<Button-1>", savebtn_click_event)


# 비밀번호 보기 상태를 관리하는 딕셔너리
password_shown = {
    "input1": False,
    "input2": False,
    "input3": False,
    "input4": False
}

# 비밀번호 표시 상태를 토글하는 함수
def toggle_password(event, input_name):
    global password_shown
    input_field = globals()[input_name]  # input_name에 해당하는 전역 변수(입력 필드)를 가져옵니다.
    if password_shown[input_name]:
        input_field.configure(show="*")
        password_shown[input_name] = False
    else:
        input_field.configure(show="")
        password_shown[input_name] = True

# 민감정보 표시 토글 버튼
show_btn1.bind("<Button-1>", lambda event: toggle_password(event, "input1"))
show_btn2.bind("<Button-1>", lambda event: toggle_password(event, "input2"))
show_btn3.bind("<Button-1>", lambda event: toggle_password(event, "input3"))
show_btn4.bind("<Button-1>", lambda event: toggle_password(event, "input4"))
start_btn.bind("<Button-1>", toggle_password_all)

# 버튼 호버시 커서 모양 변경
show_btn1.bind("<Enter>", change_cursor)
show_btn2.bind("<Enter>", change_cursor)
show_btn3.bind("<Enter>", change_cursor)
show_btn4.bind("<Enter>", change_cursor)
credit_label.bind("<Enter>", change_cursor)
like_btn.bind("<Enter>", change_cursor)

# 버튼 위에 호버시 버튼 호버 이벤트 -> 함수명 변경해야함
show_btn1.bind("<Enter>", btn_click_event)
show_btn2.bind("<Enter>", btn_click_event)
show_btn3.bind("<Enter>", btn_click_event)
show_btn4.bind("<Enter>", btn_click_event)
start_btn.bind("<Enter>", btn_click_event)
stop_btn.bind("<Enter>", btn_click_event)
credit_label.bind("<Enter>", btn_click_event)
like_btn.bind("<Enter>", btn_click_event)
shotcut_setting_btn.bind("<Enter>", btn_click_event)
warudo_setting_btn.bind("<Enter>", btn_click_event)

# 연동 시작 및 정지 버튼 클릭 이벤트
start_btn.bind("<Button-1>", lambda event: toggle_enable(event, False))
stop_btn.bind("<Button-1>", lambda event: toggle_enable(event, True))
start_btn.bind("<Button-1>", toggle_enable_on_start)
stop_btn.bind("<Button-1>", toggle_enable_on_stop)
start_btn.bind("<Button-1>", lambda event: start_donate_croll())
stop_btn.bind("<Button-1>", lambda event: stop_donate_croll())

# 단축키, 와루도, 시스템 설정 버튼 클릭 이벤트
shotcut_setting_btn.bind("<Button-1>", lambda event: open_shortcut_settings())
warudo_setting_btn.bind("<Button-1>", lambda event: open_warudo_settings())
like_btn.bind("<Button-1>", lambda event: open_system_settings())

root.protocol("WM_DELETE_WINDOW", on_closing)  # 창을 종료할때 정지 버튼과 동일한 기능

# 로그 파일 경로
log_file_path = "logs/donater.log"
start_log_monitor(log_file_path, console_box, root)  # 로그 모니터링 스레드 시작
# update_text_widget(console_box, "도네이션 연동을 시작했다굴~")

time.sleep(0.1)
logger.info('#################################')
logger.info('######### 만나서 반갑다굴~ #########')
logger.info('#################################')

# GUI를 실행합니다.
root.mainloop()


#   pyinstaller -F --hidden-import=CTkToolTip --paths=venv\Lib\site-packages\CTkToolTip --icon=ico.ico gui.py
#   pyinstaller -F -w --add-data="ico.ico;." --icon=ico.ico gui.py -> 아이콘 안됨;
