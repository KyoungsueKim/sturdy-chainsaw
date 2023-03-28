import time

import questionary
from datetime import datetime, timedelta
from main import version
from base import *
from crawlers import investing_com as inv
from crawlers import telegram as tlg
from crawlers import yna
from crawlers import naver_blog as nblog
from logger import logger, log_file_name
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Telegram post checkpoint.
hedgehara = [0]
hyottchart = [0]
bumgore = [0]
Macrojunglefortarzan = [0]
MacroAllocation = [0]


# naver blog checkpoint.
gunhey = ['']


class actions:
    executor = {
        'default': ThreadPoolExecutor(1)
    }

    schedule = BackgroundScheduler(executor=executor)
    question = None
    is_job_done = True


def __safe_stop_question():
    actions.is_job_done = False
    if actions.question.application.is_running and not actions.question.application.is_done:
        actions.question.application.exit()
    actions.schedule.pause()


def __safe_start_question():
    actions.is_job_done = True
    actions.schedule.resume()


def naver_check_post(username, checkpoint: list):
    __safe_stop_question()

    clearConsole()
    print(f'네이버 블로그 {username} 글 검사 중. 잠시만 기달려주세요...')
    try:
        post = nblog.post(username, checkpoint)
        if post is not None:
            # Logging
            logger(f"[Info] Naver Blog {username} post update found")
            logger(post)
            logger('\n')

            sendText(f"{post['title']} \n{post['url']} \n\n {post['text']} \n\n\n출처: 네이버 블로그 {username}")
    except Exception as e:
        # sendText(f"네이버 블로그 {username} 글 검사 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def tlg_check_post(username, checkpoint: list):
    __safe_stop_question()

    clearConsole()
    print(f"텔레그램 {username} 글 검사 중. 잠시만 기다려주세요...")
    try:
        post = tlg.post(username, checkpoint)
        if post is not None:
            # Logging
            logger(f"[Info] Telegram {username} post update found")
            logger(post)
            logger('\n')

            # 개시글에 이미지가 존재한다면
            if post['image_url'] is not None:
                saveImages(post['image_url'])
                sendImages()

            sendText((f"{post['text']} \n\n" if post['text'] is not None else '') + f"출처: 텔레그램 {username}")

    except Exception as e:
        # sendText(f"텔레그램 {username} 글 검사 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def yna_check_economy():
    __safe_stop_question()

    clearConsole()
    print("연합뉴스 경제 뉴스 검사 중. 잠시만 기다려주세요...")
    try:
        article = yna.economy()
        if article is not None:
            logger("[Info] Yna economy news update found")
            logger(article)
            logger('\n')

            # if article['img_url'] is not None:
            #     saveImages(article['img_url'])
            #     sendImages()

            sendText(f"{article['title']} \n\n{article['url']}")

    except Exception as e:
        # sendText(f"연합뉴스 기사 검사 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def yna_check_break():
    __safe_stop_question()

    clearConsole()
    print("연합뉴스 긴급 뉴스 검사 중. 잠시만 기달려주세요...")
    try:
        article = yna.break_news()
        if article is not None:
            logger("[Info] Yna breaking news update found")
            logger(article)
            logger('\n')

            # if article['img_url'] is not None:
            #     saveImages(article['img_url'])
            #     sendImages()

            sendText(f"{article['title']} \n\n{article['url']}")

    except Exception as e:
        # sendText(f"연합뉴스 긴급 뉴스 기사 검사 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def inv_check_article():
    __safe_stop_question()

    clearConsole()
    print("investing.com 브런치 & 퇴근길 기사 검사 중. 잠시만 기다려주세요...")
    try:
        result = inv.article()
        if len(result) > 0:
            logger("[Info] Investing.com news update found")
            logger(result)
            logger('\n')

            saveImages(result['img_url'])
            sendImages()

            message = f"네이버 오디오클립과 인포스탁데일리가 전해드리는 {datetime.now().strftime('%m월 %d일')} {result['type']} 써머리입니다.\n\n"
            message += result['url'] + "\n\n"
            for article in result['article']:
                message += article + '\n\n'

            sendText(message)

    except Exception as e:
        # sendText(f"Investing.com 브런치 & 퇴근길 검사 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def inv_check_calendar():
    __safe_stop_question()

    clearConsole()
    print("investing.com 캘린더 확인 중. 잠시만 기다려주세요...")
    logger("[Info] Check Investing.com Calendar ...")
    try:
        events = inv.calendar()
        if len(events) > 0:
            message = ""
            message += "[알림] 주간 ★★★ 이벤트 브리핑입니다. \n\n\n"
            priv_job_date = datetime.now() - timedelta(days=(datetime.now().weekday() + 1))
            delta = timedelta(0)
            for event in events:
                date = datetime.strptime(event['datetime'], '%Y/%m/%d %H:%M:%S') + timedelta(minutes=1)

                # 이벤트가 이전에 스케쥴러에 추가한 이벤트의 시간과 똑같다면 겹치지 않기 위해 1분의 timedelta를 추가.
                delta = delta + timedelta(minutes=1) if priv_job_date == date else timedelta(0)

                actions.schedule.add_job(inv_check_event, 'date', run_date=date + delta + timedelta(seconds=30), args=[event['id']])
                priv_job_date = date

                event['title'] = event['title'].replace(f"{event['country']} ", "")
                message += f"{event['datetime']} (id: {event['id']}) \n{event['emoji']} {event['country']} {event['title']}\n\n"

            sendText(message)
            logger("[Info] Successfully Added events to schedule.")
            actions.schedule.print_jobs(out=open(log_file_name, 'w'))
        logger('\n')

    except Exception as e:
        # sendText(f"Investing.com 캘린더 확인 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def inv_check_event(*args):
    if len(args) <= 0:
        return

    __safe_stop_question()

    clearConsole()
    print(f"investing.com 이벤트(id: {args}) 결과 확인 중. 잠시만 기다려주세요...")
    logger(f"[Info] Check result of id: {args} in Investing.com Calendar ...")
    try:
        result: dict
        for id in args:
            result = inv.calendar_find(id)
            sendText(f"[안내] 이벤트가 공개되었습니다. \n\n{result['country']} {result['title']}"
                     + (f"\n발표치 {result['actual']} \n예상치 {result['forecast']} \n이전치 {result['previous']}" if result['forecast'] != '\xa0' else ""))
            time.sleep(1)
        logger(result)
        logger('\n')

    except Exception as e:
        # sendText(f"Investing.com 이벤트(id: {args}) 검사 중 에러가 발생했습니다. \n{e.args}")
        logger(e.args)

    finally:
        clearConsole()
        __safe_start_question()


def tutorial():
    print(f"[아주대학교 증권연구회 정보 크롤러 v{version}]")

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
        "1. 크롤링 체크포인터 확인",
        "2. 스케줄러 확인",
        "3. Investing.com 기사 확인",
        "4. Investing.com 캘린더 확인 및 예약",
        "5. Investing.com 이벤트 결과 확인",
        "6. 연합뉴스 경제 기사 확인",
        "7. 연합뉴스 긴급 속보 확인",
        "8. hedgehara 텔레그램 포스트 확인",
        "9. hyottchart 텔레그램 포스트 확인",
        "10. bumgore 텔레그램 포스트 확인",
        "11. Macrojunglefortarzan 텔레그램 포스트 확인",
        "12. MacroAllocation 텔레그램 포스트 확인",
        "13. 네이버 블로그 gunhey 포스트 확인"
    ]
    actions.question = questionary.select("메뉴를 선택하세요.", choices=choices, use_indicator=True, qmark="", use_shortcuts=True)
    result = actions.question.ask()
    clearConsole()

    # 크롤링 체크포인터 확인
    if result == choices[0]:
        print("[Investing.com 체크포인터] \n"
              f"퇴근길/브런치 id: {inv.current_id}\n\n"
              f"[연합뉴스 Yna 체크포인터] \n"
              f"국제뉴스 date: {yna.last_economy_date}\n"
              f"긴급뉴스 date: {yna.last_break_date}\n\n"
              f"[텔레그램 체크포인터] \n"
              f"hedgehara: {hedgehara[0]}\n"
              f"hyottchart: {hyottchart[0]}\n"
              f"bumgore: {bumgore[0]}\n"
              f"Macrojunglefortarzan: {Macrojunglefortarzan[0]}\n\n"
              f"[네이버 블로그 체크포인터] \n"
              f"gunhey: {gunhey[0]}", end="\n\n")
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

    # 연합뉴스 경제 기사 확인
    elif result == choices[5]:
        yna_check_economy()

    # 연합뉴스 긴급 속보 확인
    elif result == choices[6]:
        yna_check_break()

    # hedgehara 텔레그램 포스트 확인
    elif result == choices[7]:
        tlg_check_post('hedgehara', hedgehara)

    # hyottchart 텔레그램 포스트 확인
    elif result == choices[8]:
        tlg_check_post('hyottchart', hyottchart)

    # bumgore 텔레그램 포스트 확인
    elif result == choices[9]:
        tlg_check_post('bumgore', bumgore)

    # Macrojunglefortarzan 텔레그램 포스트 확인
    elif result == choices[10]:
        tlg_check_post('Macrojunglefortarzan', Macrojunglefortarzan)

    # MacroAllocation 텔레그램 포스트 확인
    elif result == choices[11]:
        tlg_check_post('MacroAllocation', MacroAllocation)

    # 네이버 블로그 gunhey 포스트 확인
    elif result == choices[12]:
        naver_check_post('gunhey', gunhey)
