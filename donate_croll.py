__version__ = "0.0.2"
import utils as ut
import os, re, logging, argparse, asyncio

from config import AF_EVENT_XP, AF_AMOUNT_XP, AF_DONATE_SERVICE_XP, AF_MSG_XP, AF_NICK_XP
from config import TW_AMOUNT_XP, TW_EVENT_XP, TW_MSG_XP, TW_NICK_XP
from config import TO_AMOUNT_XP, TO_EVENT_XP, TO_MSG_XP, TO_NICK_XP, TO_VIDEO_CHECK_XP

from pyppeteer import launch

# NOTE 제발 코드 정리좀 하자

settings = ut.load_settings()
if settings['system']['debug']:
    logger = ut.setup_logger('donater', 'logs/donater.log', level=logging.DEBUG)
else:
    logger = ut.setup_logger('donater', 'logs/donater.log', level=logging.INFO)


class ServiceState:
    '''
    예시)
    afreeca_state = ServiceState()
    if afreeca_state.is_changed(nick_name_text, amount_text, message_text):
    afreeca_state.update(nick_name_text, amount_text, message_text)
    '''
    def __init__(self):
        self.last_nick_name = ""
        self.last_amount = ""
        self.last_message = ""

    def update(self, nick_name, amount, message):
        logger.debug(f'디버거 업데이트 "{self.last_nick_name}" -> "{nick_name}", "{self.last_amount}" -> "{amount}", "{self.last_message}" -> "{message}"')
        self.last_nick_name = nick_name
        self.last_amount = amount
        self.last_message = message

    def is_changed(self, nick_name, amount, message):
        logger.debug(f'디버거 감지 "{self.last_nick_name}" =? "{nick_name}", "{self.last_amount}" =? "{amount}", "{self.last_message}" =? "{message}"')
        return (nick_name != self.last_nick_name or
                amount != self.last_amount or
                message != self.last_message)
    
afreeca_state = ServiceState()
twip_state = ServiceState()
toonation_state = ServiceState()

async def get_info(page, nick_xp, amount_xp, msg_xp):
    nick_name = await page.xpath(nick_xp)
    amount = await page.xpath(amount_xp)
    message = await page.xpath(msg_xp)

    nick_name_text = await page.evaluate('(element) => element.textContent', nick_name[0])
    if nick_name_text is not None: nick_name_text = nick_name_text.replace(' ', '')  # 공백 제거
    amount_text = await page.evaluate('(element) => element.textContent', amount[0])
    message_text = await page.evaluate('(element) => element.textContent', message[0])
    return nick_name_text, amount_text, message_text


async def afreecahp(page):
    try:
        if await page.xpath(AF_EVENT_XP):
            donate_service = await page.xpath(AF_DONATE_SERVICE_XP)
            donate_service_text = await page.evaluate('(element) => element.textContent', donate_service[0])

            nick_name_text, amount_text, message_text = await get_info(page=page, nick_xp=AF_NICK_XP, amount_xp=AF_AMOUNT_XP, msg_xp=AF_MSG_XP)
            logger.debug(f"디버거 - 기부 서비스: {donate_service_text}, 닉네임: {nick_name_text}, 금액: {amount_text}, 메세지: {message_text}")

            # 이전 값과 다를때
            if afreeca_state.is_changed(nick_name_text, amount_text, message_text):
                afreeca_state.update(nick_name_text, amount_text, message_text)
                amount = int(re.sub("[^0-9]", "", amount_text))  # 텍스트 에서 숫자만 추출

                if "별풍선" in donate_service_text or "애드벌룬" in donate_service_text: amount = amount*100

                if "별풍선" in donate_service_text: donate_service_text = '아프리카 - 별풍선'
                elif "애드벌룬" in donate_service_text: donate_service_text = '아프리카 - 애드벌룬'
                elif "치즈" in donate_service_text: donate_service = '치지직 - 치즈'
                elif "슈퍼채팅" in donate_service_text: donate_service = '유튜브 - 슈퍼채팅'
                logger.info(f"기부 서비스: {donate_service_text}, 닉네임: {nick_name_text}, 금액: {amount_text}, 메세지: {message_text}")
                return {'donate_service': donate_service_text, 'nick_name': nick_name_text, 'amount': amount, 'message': message_text}
            else:
                return None
    except Exception as e:
        logging.exception(f'아프리카 도우미 크롤러 에러 발생 {e}')
        return None

async def twip(page):
    try:
        if await page.xpath(TW_EVENT_XP):
            nick_name_text, amount_text, message_text = await get_info(page=page, nick_xp=TW_NICK_XP, amount_xp=TW_AMOUNT_XP, msg_xp=TW_MSG_XP)
            if not '[YouTube 영상]' in message_text:
                logger.debug(f"디버거 - 기부 서비스: 트윕, 닉네임: {nick_name_text}, 금액: {amount_text}, 메세지: {message_text}")
                # 이전 값과 다를때
                if twip_state.is_changed(nick_name_text, amount_text, message_text):
                    twip_state.update(nick_name_text, amount_text, message_text)
                    amount = int(re.sub("[^0-9]", "", amount_text))  # 텍스트 에서 숫자만 추출
                    logger.info(f"기부 서비스: '트윕 - 도네이션', 닉네임: {nick_name_text}, 금액: {amount_text}, 메세지: {message_text}")
                    return {'donate_service': '트윕 - 도네이션', 'nick_name': nick_name_text, 'amount': amount, 'message': message_text}
    except:
        return None

async def toonation(page):
    try:
        if await page.xpath(TO_EVENT_XP):
            nick_name_text, amount_text, message_text = await get_info(page=page, nick_xp=TO_NICK_XP, amount_xp=TO_AMOUNT_XP, msg_xp=TO_MSG_XP)
            logger.debug(f"디버거 - 기부 서비스: 투네이션, 닉네임: {nick_name_text}, 금액: {amount_text}, 메세지: {message_text}")
            # 이전 값과 다를때
            if toonation_state.is_changed(nick_name_text, amount_text, message_text):
                toonation_state.update(nick_name_text, amount_text, message_text)
                amount = int(re.sub("[^0-9]", "", amount_text))  # 텍스트 에서 숫자만 추출
                logger.info(f"기부 서비스: '투네이션 - 도네이션', 닉네임: {nick_name_text}, 금액: {amount_text}, 메세지: {message_text}")
                return {'donate_service': '투네이션 - 도네이션', 'nick_name': nick_name_text, 'amount': amount, 'message': message_text}
    except:
        return None

async def main():
    # 설정 변수
    settings = ut.load_settings()
    system_settings = settings['system']
    afreecahp_settings = settings['afreecahp']
    toonation_settings = settings['toonation']
    twip_settings = settings['twip']

    # 디버깅용 설정 로그 기록
    logger.info(settings)

    urls = {}
    if afreecahp_settings.get('use', False):
        urls['afreeca'] = afreecahp_settings['alertbox_url']
    if twip_settings.get('use', False):
        urls['twip'] = twip_settings['alertbox_url']
    if toonation_settings.get('use', False):
        urls['toonation'] = toonation_settings['alertbox_url']

    active_tabs_count = len(urls)
    wait_time_per_tab = float(system_settings['cycle_time']) / active_tabs_count

    launch_args = [
        # '--no-sandbox',  # 샌드박스 비활성화 (필요한 경우)
        # '--disable-setuid-sandbox',  # UID 샌드박스 비활성화 (필요한 경우)
        f'--blink-settings=imagesEnabled={system_settings["load_images"]}',  # 이미지 로딩 비활성화
        '--mute-audio',  # 브라우저의 소리를 끔
        '--disable-blink-features=AutomationControlled'  # 자동화된 제어 감지 비활성화
    ]
    
    # logger.debug('디버거 - 브라우저 소환')
    browser = await launch(executablePath=f"{os.path.join('bin', 'chrome.exe')}", 
                           headless=not system_settings['debug'], ignoreHTTPSErrors=True, dumpio=system_settings['debug'], args=launch_args)  # args 변수를 launch 함수에 전달
    
    # 각 탭으로 알림 페이지를 열어서 n초 마다 순환 하는 방식
    # logger.debug('디버거 - 브라우저 탭 생성')
    pages = {}
    for service, url in urls.items():
        page = await browser.newPage()
        await page.goto(url)
        pages[service] = page

    logger.info(f'도네이션 연동시작')
    # logger.debug('디버거 - 도네이션 연동 순환')
    try:
        while True:
            system_status = ut.load_settings()['system']['status']
            if system_status == 'stop':
                # logger.info(f'도네이션 연동을 중지합니다.')
                break
            elif system_status == 'pause': 
                # logger.info(f'도네이션 연동을 일시중지합니다.')
                await asyncio.sleep(1)
                continue

            for service, page in pages.items():
                result = None
                if service == 'afreeca': 
                    logger.debug(f'현재탭: {service}')
                    result = await afreecahp(page=page)
                        
                elif service == 'twip': 
                    logger.debug(f'현재탭: {service}')
                    result = await twip(page=page)

                elif service == 'toonation': 
                    logger.debug(f'현재탭: {service}')
                    result = await toonation(page=page)

                if result is not None:
                    # amount 는 무조건 int 타입
                    ut.send_discord_webhook(data=f"{result['donate_service']} {result['nick_name']} {result['amount']}원")
                    ut.send_warudo_websocket(data=result['amount'])
                    ut.price_shortcut_execute(price=result['amount'])
                
                await asyncio.sleep(wait_time_per_tab)  # 각 탭 사이에 짧은 균등한 대기 시간 추가 
                
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
    finally:
        await browser.close()
        print("브라우저가 성공적으로 종료되었습니다.")
        system_settings['status'] = 'stopped'
        ut.save_settings(settings)

if __name__ == "__main__":
    # argparse를 사용하여 커맨드 라인 인자 처리
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--startwith', type=str, choices=['true', 'false'])
    args = parser.parse_args()

    if args.startwith == 'true':
        print(1)
        # 설정 파일 로드하는 부분
        if __name__ == "__main__":
            asyncio.run(main())
    else:
        print(0)


# pyinstaller -F -w donate_croll.py