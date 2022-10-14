import time

import questionary
from datetime import datetime, timedelta
from base import *
from crawlers import investing_com as inv
from crawlers import telegram as tlg
from crawlers import yna
from logger import logger, log_file
from apscheduler.schedulers.background import BackgroundScheduler
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Telegram post checkpoint.
hedgehara = [0]
hyottchart = [0]

class actions:
    schedule = BackgroundScheduler()
    question = None
    is_job_done = True


def __safe_stop_question():
    actions.is_job_done = False
    if actions.question.application.is_running:
        actions.question.application.exit()
    actions.schedule.pause()


def __safe_start_question():
    actions.is_job_done = True
    actions.schedule.resume()


def tlg_check_post(username, checkpoint: list):
    __safe_stop_question()

    clearConsole()
    print(f"텔레그램 {username} 글 검사 중. 잠시만 기다려주세요...")
    post = tlg.post(username, checkpoint)
    if post is not None:
        # Logging
        logger(f"[Info] Telegram {username} post update found")
        logger(post)
        logger('\n')

        # 개시글에 이미지가 존재한다면
        image_url = post['image_url'] if post['image_url'] is not None else post['link_priv_image']
        if image_url is not None:
            saveImages(image_url)
            sendImages()

        sendText(f"[알림] 텔레그램 {username}에서 새로운 글이 업로드되었습니다. \n{post['url']} \n\n{post['text']}")

    clearConsole()
    __safe_start_question()


def yna_check_article():
    __safe_stop_question()

    clearConsole()
    print("연합뉴스 기사 검사 중. 잠시만 기다려주세요...")
    article = yna.article()
    if article is not None:
        logger("[Info] Yna news update found")
        logger(article)
        logger('\n')

        if article['img_url'] is not None:
            saveImages(article['img_url'])
            sendImages()

        sendText(f"[알림] 연합뉴스에서 새로운 기사가 작성되었습니다. \n\n{article['url']} \n\n제목: {article['title']} \n\n")

    clearConsole()
    __safe_start_question()


def inv_check_article():
    __safe_stop_question()

    clearConsole()
    print("investing.com 브런치 & 퇴근길 기사 검사 중. 잠시만 기다려주세요...")
    article = inv.article()
    if article is not None:
        logger("[Info] Investing.com news update found")
        logger(article)
        logger('\n')

        sendText(f"[알림] {article}")

    clearConsole()
    __safe_start_question()


def inv_check_calendar():
    __safe_stop_question()

    clearConsole()
    print("investing.com 캘린더 확인 중. 잠시만 기다려주세요...")
    logger("[Info] Check Investing.com Calendar ...")

    events = inv.calendar()
    if len(events) > 0:
        sendText("[알림] 주간 ★★★ 이벤트 브리핑입니다.")
    for event in events:
        date = datetime.strptime(event['datetime'], '%Y/%m/%d %H:%M:%S') + timedelta(minutes=10)
        actions.schedule.add_job(inv_check_event, 'date', run_date=date, args=[event['id']])

        sendText(f"{event['datetime']} (id: {event['id']}) \n{event['country']} {event['title']}")
        time.sleep(1.5)

    logger("[Info] Successfully Added events to schedule.")
    actions.schedule.print_jobs(out=log_file())
    logger('\n')

    clearConsole()
    __safe_start_question()


def inv_check_event(id: str):
    __safe_stop_question()

    clearConsole()
    print(f"investing.com 이벤트(id: {id}) 결과 확인 중. 잠시만 기다려주세요...")
    logger(f"[Info] Check result of id: {id} in Investing.com Calendar ...")

    result = inv.calendar_find(id)
    logger(result)
    logger('\n')

    sendText(
        f"[안내] 이벤트 발표치가 공개되었습니다. \n\n{result['country']} {result['title']} \n발표치 {result['actual']} \n예상치 {result['forecast']} \n이전치 {result['previous']}")

    clearConsole()
    __safe_start_question()


def tutorial():
    print("[아주대학교 증권연구회 정보 크롤러 v1.0.0]")

    openImagePath()
    questionary.confirm("카톡창과 이미지 폴더 창을 적절히 배치하세요. 그 뒤 마우스 커서 위치 캡처를 위해 이미지 폴더가 열린 탐색기의 빈 공간으로 옮기고 엔터를 누르세요.",
                        default=True, qmark="").ask()
    print("이미지 폴더 탐색기 커서 위치: ", pyautogui.position())
    position.explorer = pyautogui.position()

    questionary.confirm("이번엔 마우스 커서를 카톡 채팅방 입력칸에 올리고 엔터를 누르세요.", default=True, qmark="").ask()
    print("카톡 채팅방 입력칸 커서 위치: ", pyautogui.position())
    position.text = pyautogui.position()
    print("설정이 완료되었습니다.")


def show_menu():
    choices = [
        "1. 마우스 포인터 위치 체크",
        "2. 스케줄러 확인",
        "3. Investing.com 기사 확인",
        "4. Investing.com 캘린더 확인 및 예약",
        "5. Investing.com 이벤트 결과 확인",
        "6. 연합뉴스 기사 확인",
        "7. hedgehara 텔레그램 포스트 확인",
        "8. hyottchart 텔레그램 포스트 확인"
    ]
    actions.question = questionary.select("메뉴를 선택하세요.", choices=choices, use_indicator=True, qmark="", use_shortcuts=True)
    result = actions.question.ask()
    clearConsole()

    # 마우스 포인터 위치 체크
    if result == choices[0]:
        print("현재 마우스 위치: ", pyautogui.position(), end="\n\n")
        show_menu()

    # 스케줄러 확인
    elif result == choices[1]:
        actions.schedule.print_jobs()
        print()
        show_menu()

    # Investing.com 기사 확인
    elif result == choices[2]:
        inv_check_article()

    # Investing.com 캘린더 확인 및 예약
    elif result == choices[3]:
        inv_check_calendar()

    # Investing.com 이벤트 결과 확인
    elif result == choices[4]:
        __safe_stop_question()
        id = questionary.text("확인하려는 이벤트의 id를 입력해주세요. ", qmark="").ask()
        inv_check_event(str(id))

    # 연합뉴스 기사 확인
    elif result == choices[5]:
        yna_check_article()

    # hedgehara 텔레그램 포스트 확인
    elif result == choices[6]:
        tlg_check_post('hedgehara', hedgehara)

    # hyottchart 텔레그램 포스트 확인
    elif result == choices[7]:
        tlg_check_post('hyottchart', hyottchart)
