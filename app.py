import streamlit as st
import time
import utils as ut


if 'afreehp_thread_alive' not in st.session_state:
    st.session_state.afreehp_thread_alive = False
if 'twip_thread_alive' not in st.session_state:
    st.session_state.twip_thread_alive = False
if 'toon_thread_alive' not in st.session_state:
    st.session_state.toon_thread_alive = False
if 'warudo_thread_alive' not in st.session_state:
    st.session_state.warudo_thread_alive = False


settings = ut.load_settings()

st.title('와루도 도네이션 연동')
st.subheader('새로고침 금지')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["대시보드", "수동 연동", "가격 설정", "연동 설정", "시스템 설정"])

def refresh_thread_status():
    st.session_state.afreehp_thread_alive = ut.is_afreeca_croll_process_alive()
    st.session_state.twip_thread_alive = ut.is_twip_thread_alive()
    st.session_state.toon_thread_alive = ut.is_toon_thread_alive()
    st.session_state.warudo_thread_alive = ut.is_warudo_thread_alive()

    if st.session_state.warudo_thread_alive: warudo_status_container.success("와루도 연동 상태: 연동중")
    else: warudo_status_container.error("와루도 연동 상태: 연동중이 아님")
    if st.session_state.twip_thread_alive: twip_status_container.success("트윕 연동 상태: 연동중")
    else: twip_status_container.error("트윕 연동 상태: 연동중이 아님")
    if st.session_state.toon_thread_alive: toon_status_container.success("투네이션 연동 상태: 연동중")
    else: toon_status_container.error("투네이션 연동 상태: 연동중이 아님")
    if st.session_state.afreehp_thread_alive: afreehp_status_container.success("아프리카 도우미 연동 상태: 연동중")
    else: afreehp_status_container.error("아프리카 도우미 연동 상태: 연동중이 아님")

def all_connect():
    with st.spinner("와루도 연동을 시작합니다."):
        ut.start_warudo_thread()
        time.sleep(3)
        refresh_thread_status()
    with st.spinner("트윕 연동을 시작합니다."):
        refresh_thread_status()
        ut.start_twip_thread()
        time.sleep(3)
        refresh_thread_status()
    with st.spinner("투네이션 연동을 시작합니다."):
        refresh_thread_status()
        ut.start_toon_thread()
        time.sleep(3)
        refresh_thread_status()
    with st.spinner("아프리카 연동을 시작합니다."):
        refresh_thread_status()
        ut.start_afreeca_croll_process()
        time.sleep(3)
        refresh_thread_status()

def all_disconnect():
    with st.spinner("와루도 연동을 종료합니다."):
        ut.stop_warudo_thread()
        time.sleep(3)
        refresh_thread_status()
    with st.spinner("트윕 연동을 종료합니다."):
        ut.stop_twip_thread()
        time.sleep(3)
        refresh_thread_status()
    with st.spinner("투네이션 연동을 종료합니다."):
        ut.stop_toon_thread()
        time.sleep(3)
        refresh_thread_status()
    with st.spinner("아프리카 연동을 종료합니다."):
        ut.stop_afreeca_croll_process()
        time.sleep(3)
        refresh_thread_status()


with tab1:
    st.subheader('대시보드')
    warudo_status_container = st.empty()
    twip_status_container = st.empty()
    toon_status_container = st.empty()
    afreehp_status_container = st.empty()
    refresh_thread_status()

    if st.button("상태 검사 시작", use_container_width=True):
        with st.spinner("상태 검사를 시작합니다."):
            for _ in range(5):
                refresh_thread_status()
                time.sleep(0.5)
    
    st.divider()
    st.subheader('원클릭 연동 시작')
    st.write('연동 시작전 와루도 실행과 로딩을 완료해 주세요, 이미 늦었다면 수동연동에서 와루도만 켜주면됨')
    if st.button("연동 일괄 시작", use_container_width=True):
        all_connect()

    st.divider()
    st.subheader('원클릭 연동 종료')
    if st.button("연동 일괄 종료", type='primary', use_container_width=True):
        all_disconnect()
        st.success('모든 연동 종료 완료, 프로그램 종료해도됨')
        ut.save_settings(settings)
            

with tab2:
    st.subheader('와루도 연동')
    if st.button("와루도 연동 시작", use_container_width=True, help='와루도 개별 연동을 시작합니다.'):
        with st.spinner("와루도 연동을 시작합니다."):
            ut.save_settings(settings)
            ut.start_warudo_thread()
            while True:
                try:
                    refresh_thread_status()
                    if st.session_state.warudo_thread_alive:
                        st.success("와루도 연동이 시작 되었습니다.")
                        break
                    else:
                        time.sleep(1)
                        continue
                except Exception as e:
                    st.error(f"와루도 연동을 시작하지 못했습니다. {e}")
                    break
    
    if st.button('와루도 연동 종료', use_container_width=True):
        with st.spinner("와루도 연동을 종료합니다."):
            ut.save_settings(settings)
            ut.stop_warudo_thread()
            refresh_thread_status()
            st.success("와루도 연동이 종료되었습니다.")

    st.divider()
    st.subheader('트윕 연동')
    if st.button("트윕 연동 시작", use_container_width=True, help='트윕 개별 연동을 시작합니다.'):
        with st.spinner("트윕 연동을 시작합니다."):
            ut.save_settings(settings)
            ut.start_twip_thread()
            while True:
                try:
                    refresh_thread_status()
                    if st.session_state.twip_thread_alive:
                        st.success("트윕 연동이 시작 되었습니다.")
                        break
                    else:
                        time.sleep(1)
                        continue
                except Exception as e:
                    st.error(f"트윕 연동을 시작하지 못했습니다. {e}")
                    break

    if st.button('트윕 연동 종료', use_container_width=True):
        with st.spinner("트윕 연동을 종료합니다."):
            ut.save_settings(settings)
            ut.stop_twip_thread()
            refresh_thread_status()
            st.success("트윕 연동이 종료되었습니다.")

    st.divider()
    st.subheader('투네이션 연동')
    if st.button("투네이션 연동 시작", use_container_width=True, help='투네이션 개별 연동을 시작합니다.'):
        with st.spinner("투네이션 연동을 시작합니다."):
            ut.save_settings(settings)
            ut.start_toon_thread()
            while True:
                try:
                    refresh_thread_status()
                    if st.session_state.toon_thread_alive:
                        st.success("투네이션 연동이 시작 되었습니다.")
                        break
                    else:
                        time.sleep(1)
                        continue
                except Exception as e:
                    st.error(f"투네이션 연동을 시작하지 못했습니다. {e}")
                    break

    if st.button('투네이션 연동 종료', use_container_width=True):
        with st.spinner("투네이션 연동을 종료합니다."):
            ut.save_settings(settings)
            ut.stop_toon_thread()
            refresh_thread_status()
            st.success("투네이션 연동이 종료되었습니다.")

    st.divider()
    st.subheader('아프리카 도우미 연동')
    if st.button("아프리카, 치지직, 유튜브 연동 시작", use_container_width=True, help='아프리카, 치지직, 유튜브 개별 연동을 시작합니다.'):
        with st.spinner("아프리카 연동을 시작합니다."):
            ut.save_settings(settings)
            ut.start_afreeca_croll_process()
            while True:
                try:
                    refresh_thread_status()
                    if st.session_state.afreehp_thread_alive:
                        st.success("아프리카 도우미 연동이 시작 되었습니다.")
                        break
                    else:
                        time.sleep(1)
                        continue
                except Exception as e:
                    st.error(f"아프리카 도우미 연동을 시작하지 못했습니다. {e}")
                    break

    if st.button("아프리카 연동 종료", use_container_width=True):
        with st.spinner("아프리카 연동을 종료합니다."):
            ut.save_settings(settings)
            ut.stop_afreeca_croll_process()
            refresh_thread_status()
            st.success("아프리카 도우미 연동을 종료합니다.")
    st.divider()


with tab3:
    # 가격설정 탭
    st.subheader('의상 가격 설정')
    settings['price1']['hair'] = st.number_input("헤어 가격", value=settings['price1']['hair'])
    settings['price1']['clothes'] = st.number_input("의상 가격", value=settings['price1']['clothes'])
    settings['price1']['choker'] = st.number_input("초커 가격", value=settings['price1']['choker'])
    settings['price1']['earrings'] = st.number_input("귀걸이 가격", value=settings['price1']['earrings'])
    settings['price1']['glasses'] = st.number_input("안경 가격", value=settings['price1']['glasses'])
    settings['price1']['nails'] = st.number_input("네일 가격", value=settings['price1']['nails'])
    settings['price1']['necklace'] = st.number_input("목걸이 가격", value=settings['price1']['necklace'])
    if st.button("의상 설정 저장", use_container_width=True):
        ut.save_settings(settings)
        st.success("의상 설정이 저장되었습니다.")

    # st.divider()

    # st.subheader('액션 가격 설정')
    # settings['price2']['throw'] = st.number_input("던지기 가격", min_value=1000)
    # settings['price2']['mecha_throw'] = st.number_input("마구 던지기 가격", min_value=1000)
    # settings['price2']['tail_show'] = st.number_input("꼬리 보여주기 가격", min_value=1000)
    # settings['price2']['hack_punch'] = st.number_input("핵 펀치 가격", min_value=1000)
    # settings['price2']['cat_pose'] = st.number_input("냥냥 포즈 가격", min_value=1000)
    # settings['price2']['hand_stand'] = st.number_input("물구나무서기 가격", min_value=1000)
    # settings['price2']['dogeja'] = st.number_input("도게자 가격", min_value=1000)
    # if st.button("액션 설정 저장", use_container_width=True):
    #     ut.save_settings(settings)
    #     st.success("액션 설정이 저장되었습니다.")
    
    
    # st.divider()

    # st.subheader('별 눈알 가격 설정')
    # st.write('연동중에 수정하면 무슨일 일어날지 모름')
    # # 별 눈 고정 가격 추가
    # if settings['price3']['eye_star_fix']:
    #     eye_star_fix_prices = ', '.join([f"{price}원" for price in settings['price3']['eye_star_fix']])
    #     st.text_input("별 눈 리스트", value=eye_star_fix_prices, disabled=True)
    # else:
    #     st.text_input("별 눈 고정 가격", value="설정된 가격이 없습니다.", disabled=True)
    # new_eye_star_fix_price = st.number_input("별 눈 고정 가격 추가 및 제거(~원 일때)", min_value=1000)
    # if st.button('별 눈 가격 추가', use_container_width=True):
    #     if new_eye_star_fix_price not in settings['price3']['eye_star_fix']:
    #         settings['price3']['eye_star_fix'].append(new_eye_star_fix_price)
    #         settings['price3']['eye_star_fix'].sort()  # 가격을 오름차순으로 정렬
    #         ut.save_settings(settings)  # 설정을 저장합니다.
    #         st.experimental_rerun()  # 스트림릿 앱을 다시 실행하여 최신화합니다.
    # if st.button('별 눈 가격 제거', use_container_width=True):
    #     try:
    #         # 입력된 가격을 제거합니다.
    #         remove_price = new_eye_star_fix_price
    #         if remove_price in settings['price3']['eye_star_fix']:
    #             settings['price3']['eye_star_fix'].remove(remove_price)
    #             settings['price3']['eye_star_fix'].sort()  # 가격을 오름차순으로 정렬
    #             ut.save_settings(settings)  # 설정을 저장합니다.
    #             st.experimental_rerun()  # 스트림릿 앱을 다시 실행하여 최신화합니다.
    #         else:
    #             st.error("제거하려는 가격이 목록에 없습니다.")
    #     except Exception as e:
    #         st.error("가격 제거 중 오류가 발생했습니다.")

    # st.divider()
    # st.subheader('하트 눈알 가격 설정')
    # st.write('연동중에 수정하면 무슨일 일어날지 모름')
    # # 하트 눈 고정 가격 추가
    # if settings['price3']['eye_heart_fix']:
    #     eye_heart_fix_prices = ', '.join([f"{price}원" for price in settings['price3']['eye_heart_fix']])
    #     st.text_input("하트 눈 리스트", value=eye_heart_fix_prices, disabled=True)
    # else:
    #     st.text_input("하트 눈 고정 가격", value="설정된 가격이 없습니다.", disabled=True)
    # new_eye_heart_fix_price = st.number_input("하트 눈 고정 가격 추가 및 제거(~원 일때)", min_value=1000)
    # if st.button('하트 눈 가격 추가', use_container_width=True):
    #     if new_eye_heart_fix_price not in settings['price3']['eye_heart_fix']:
    #         settings['price3']['eye_heart_fix'].append(new_eye_heart_fix_price)
    #         settings['price3']['eye_heart_fix'].sort()  # 가격을 오름차순으로 정렬
    #         ut.save_settings(settings)  # 설정을 저장합니다.
    #         st.experimental_rerun()  # 스트림릿 앱을 다시 실행하여 최신화합니다.

    # if st.button('하트 눈 가격 제거', use_container_width=True):
    #     try:
    #         # 입력된 가격을 제거합니다.
    #         remove_price = new_eye_heart_fix_price
    #         if remove_price in settings['price3']['eye_heart_fix']:
    #             settings['price3']['eye_heart_fix'].remove(remove_price)
    #             settings['price3']['eye_heart_fix'].sort()  # 가격을 오름차순으로 정렬
    #             ut.save_settings(settings)  # 설정을 저장합니다.
    #             st.experimental_rerun()  # 스트림릿 앱을 다시 실행하여 최신화합니다.
    #         else:
    #             st.error("제거하려는 가격이 목록에 없습니다.")
    #     except Exception as e:
    #         st.error("가격 제거 중 오류가 발생했습니다.")

    # if st.button("표정 설정 저장", use_container_width=True):
    #     ut.save_settings(settings)
    #     st.success("표정 설정이 저장되었습니다.")


with tab4:
    # TODO 설정 변경 후 저장시 다시 최신값 로딩
    # TODO 설정 초기화 구현

    st.subheader('아프리카 설정')
    settings['afreehp']['use'] = st.checkbox(label="아프리카 연동", value=settings['afreehp']['use'])
    settings['afreehp']['debug'] = st.checkbox(label="아프리카 도우미 디버깅 모드 활성화", value=settings['afreehp']['debug'])
    settings['afreehp']['alertbox_url'] = st.text_input(label="아프리카 알림창 url", value=settings['afreehp']['alertbox_url'])
    settings['afreehp']['idx'] = st.text_input(label="아프리카 IDX", value=settings['afreehp']['idx'], disabled=True)
    if st.button("아프리카 설정 저장", use_container_width=True):
        ut.save_settings(settings)
        st.success("아프리카 설정이 저장되었습니다.")
    st.divider()

    st.subheader('투네이션 설정')
    settings['toon']['use'] = st.checkbox(label="투네이션 연동", value=settings['toon']['use'])
    settings['toon']['debug'] = st.checkbox(label="투네이션 디버깅 모드 활성화", value=settings['toon']['debug'])
    settings['toon']['alertbox_url'] = st.text_input(label="투네이션 알림창 url", value=settings['toon']['alertbox_url'])
    settings['toon']['payload'] = st.text_input(label="투네이션 payload", value=settings['toon']['payload'], disabled=True)
    if st.button("투네이션 설정 저장", use_container_width=True):
        ut.save_settings(settings)
        st.success("투네이션 설정이 저장되었습니다.")

    st.divider()

    st.subheader('트윕 설정')
    settings['twip']['use'] = st.checkbox(label="트윕 연동", value=settings['twip']['use'])
    settings['twip']['debug'] = st.checkbox(label="트윕 디버깅 모드 활성화", value=settings['twip']['debug'])
    settings['twip']['alertbox_url'] = st.text_input(label="트윕 알림창 url", value=settings['twip']['alertbox_url'])
    settings['twip']['token'] = st.text_input(label="트윕 api 토큰", value=settings['twip']['token'])
    settings['twip']['idx'] = st.text_input(label="트윕 IDX", value=settings['twip']['idx'])
    if st.button("트윕 설정 저장", use_container_width=True):
        ut.save_settings(settings)
        st.success("트윕 설정이 저장되었습니다.")
    st.divider()

    st.subheader('디스코드 설정')
    settings['discord']['use'] = st.checkbox(label="디스코드 연동", value=settings['discord']['use'])
    settings['discord']['amount_hide'] = st.checkbox(label="디스코드 메세지 금액 숨김", value=settings['discord']['amount_hide'])
    settings['discord']['webhook_url'] = st.text_input(label="디스코드 웹훅 url", value=settings['discord']['webhook_url'])
    if st.button("디스코드 설정 저장", use_container_width=True):
        ut.save_settings(settings)
        st.success("디스코드 설정이 저장되었습니다.")
    st.divider()

    st.subheader('연동 설정 초기화')
    st.button("연동 설정 초기화", on_click=ut.save_settings(settings), use_container_width=True, type="primary", disabled=True)

with tab5:
    st.subheader('와루도 설정')
    settings['warudo']['debug'] = st.checkbox(label="와루도 디버깅 모드 활성화", value=settings['warudo']['debug'])
    settings['warudo']['action'] = st.text_input(label="와루도 연결 액션", value=settings['warudo']['action'])
    settings['warudo']['socket_url'] = st.text_input(label="와루도 소켓 url", value=settings['warudo']['socket_url'])

    settings['warudo']['minimum_time_min'] = st.text_input(label="와루도 최소 보장 시간(분)", value=settings['warudo']['minimum_time_min'])
    settings['warudo']['queue_check_time_sec'] = st.text_input(label="와루도 큐 체크 시간(초)", value=settings['warudo']['queue_check_time_sec'])
    settings['warudo']['safe_delete_time_sec'] = st.text_input(label="와루도 안전 삭제 시간(초)", value=settings['warudo']['safe_delete_time_sec'])

    st.button("와루도 설정 저장", on_click=ut.save_settings(settings), use_container_width=True)
    st.divider()

    st.subheader('와루도 설정 초기화')
    st.button("와루도 설정 초기화", on_click=ut.save_settings(settings), use_container_width=True, type="primary", disabled=True)