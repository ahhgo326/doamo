import yaml, json, websocket, requests, logging, os, pyautogui
from logging.handlers import TimedRotatingFileHandler

# NOTE 제발 코드 정리좀 하자
# NOTE 와루도 연결 유지 클래스

def setup_logger(name, log_file, level=logging.DEBUG):
    """로거 설정을 위한 함수, 로그 파일을 하나의 파일에 계속 저장"""
    # 로거 생성
    logger = logging.getLogger(name)
    if not logger.handlers:  # 로거에 핸들러가 없는 경우에만 설정
        logger.setLevel(level)

        # FileHandler 설정
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)

        # 스트림 핸들러 설정
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)

        # 로그 포맷 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # 로거에 핸들러 추가
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

#######################################################################################
def load_settings():
    # logger.debug("설정 파일 로드를 시도합니다.")
    try:
        with open("config.yaml", "r", encoding='utf-8') as file:
            settings = yaml.safe_load(file)
            # logger.debug("설정 파일 로드 성공.")
        return settings
    except FileNotFoundError:
        # logger.error("config.yaml 파일을 찾을 수 없습니다.")
        exit(1)
    except Exception as e:
        # logger.exception(f"설정 파일 로드 중 오류 발생: {str(e)}")
        exit(1)

def save_settings(settings):
    # logger.debug("설정 파일 저장을 시도합니다.")
    try:
        with open("config.yaml", "w", encoding='utf-8') as file:
            yaml.safe_dump(settings, file)
            # logger.debug("설정 파일 저장 성공.")
    except FileNotFoundError:
        # logger.error("config.yaml 파일을 찾을 수 없습니다.")
        exit(1)
    except Exception as e:
        # logger.exception(f"설정 파일 저장 중 오류 발생: {str(e)}")
        exit(1)

def check_browser():
    settings = load_settings()
    if not os.path.exists('bin\chrome.exe'):
        pass

def check_config():
    """설정 파일의 유효성을 검사하고, 없으면 기본 구성으로 생성합니다."""
    default_settings = {
        'afreecahp': {
            'alertbox_url': 'afreecahp_alert_url',
            'use': False
        },
        'discord': {
            'use': True,
            'webhook_url': 'discord_webhook_url'
        },
        'shortcut': {
            'use': True,
        },
        'system': {
            'build': '124.0.6324.0(dev)',
            'cycle_time': 1.5,
            'debug': False,
            'load_images': False,
            'status': 'live'
        },
        'toonation': {
            'alertbox_url': 'toonation_alert_url',
            'use': True
        },
        'twip': {
            'alertbox_url': 'twip_alert_url',
            'use': True
        },
        'warudo': {
            'action': 'donation',
            'port': 19190,
            'use': False
        }
    }
    try:
        settings = load_settings()
        if settings is None:
            raise ValueError("설정 파일이 비어있습니다.")
        required_keys = ['afreecahp', 'discord', 'shortcut', 'system', 'toonation', 'twip', 'warudo']
        for key in required_keys:
            if key not in settings:
                raise KeyError(f"{key} 설정이 누락되었습니다.")
        # logger.info("설정 파일 검사 성공.")
    except FileNotFoundError:
        # logger.info("config.yaml 파일이 없어 기본 설정으로 생성합니다.")
        save_settings(default_settings)
    except Exception as e:
        # logger.error(f"설정 파일 검사 중 오류 발생: {str(e)}")
        exit(1)
#######################################################################################

settings = load_settings()
if settings['system']['debug']:
    logger = setup_logger('donater', 'logs/donater.log', level=logging.DEBUG)
else:
    logger = setup_logger('donater', 'logs/donater.log', level=logging.INFO)


#######################################################################################
def send_warudo_websocket(data):
    settings = load_settings()
    data = int(data)
    port = str(settings['warudo']['port'])
    action = settings['warudo']['action']
    try:
        if settings['warudo']['use']:
            logger.debug("디버거 와루도 | 웹소켓 연결을 시도합니다.")
            warudo_url = f"ws://localhost:{port}"
            ws = websocket.create_connection(url=warudo_url)
            message = json.dumps({"action": action, "data": data})
            logger.debug(f"디버거 와루도 | 웹소켓 연결됨 {warudo_url}, 메시지: {message}")
            ws.send(message)
            logger.info(f"와루도 | Warudo {data} 전송 완료.")
            ws.close()
            logger.debug("디버거 와루도 | 웹소켓 연결을 종료합니다.")
    except Exception as e:
        if settings['system']['debug']:
            logger.exception(f"디버거 와루도 | 웹소켓 전송 중 오류 발생: {str(e)}")
        else:
            logger.error(f"디버거 와루도 | {port}, {action} 연결할 수 없습니다. 설정을 확인해 주세요.")

def send_discord_webhook(data):
    settings = load_settings()
    webhook_url = settings['discord']['webhook_url']
    try:
        if settings['discord']['use']:
            # data가 int 타입인지 확인하고, 아니라면 str로 변환
            if not isinstance(data, int):
                data = str(data)
            json_data = {"content": data}
            logger.debug("디버거 디스코드 | 웹훅 전송을 시도합니다.")
            requests.post(url=webhook_url, json=json_data)
            logger.info(f"디스코드 | {json_data}")
    except Exception as e:
        if settings['system']['debug']:
            logger.exception(f"디버거 | 디스코드 웹훅 전송 중 오류 발생: {str(e)}")
        else:
            logger.error(f"디스코드 웹훅 전송 중 오류 발생: {str(e)}")
#######################################################################################

#######################################################################################
def add_shortcut(price, shortcut):
    settings = load_settings()
    try:
        shortcut_settings = settings.get('shortcut', {})
        shortcut_settings[int(price)] = shortcut
        settings['shortcut'] = shortcut_settings
        save_settings(settings)
        logger.info(f'단축키 | {price}: {shortcut} 추가(수정)')
    except Exception as e:
        if settings['system']['debug']:
            logger.exception(f"디버거 | 단축키 등록 중 오류 발생: {str(e)}")
        else:
            logger.error(f"단축키 등록 중 오류 발생: {str(e)}")

def del_shortcut(price):
    settings = load_settings()
    if 'shortcut' in settings and int(price) in settings['shortcut']:
        del settings['shortcut'][int(price)]
        save_settings(settings)
        logger.info(f'단축키 | {price} 삭제')
    else:
        logger.warning(f'단축키 | {price} 가격에 해당하는 단축키를 찾을 수 없습니다.')

# 설정 파일에서 가격을 키로 단축키를 검색해서 단축키 실행
def price_shortcut_execute(price):
    shortcut_settings = load_settings()['shortcut']
    try:
        if shortcut_settings['use']:
            price_shortcut = shortcut_settings.get(price)
            if price_shortcut:
                logger.info(f'단축키 | {price} - {price_shortcut} 입력')
                shortcut = price_shortcut.split('+')
                pyautogui.hotkey(*shortcut)
    except Exception as e:
        if settings['system']['debug']:
            logger.exception(f"디버거 | 단축키 입력 중 오류 발생: {str(e)}")
        else:
            logger.error(f"단축키 입력 중 오류 발생: {str(e)}")

#######################################################################################
if __name__ == "__main__":
    send_warudo_websocket(2100)

