import time
from base import clearConsole
from actions import *
from logger import logger, log_file

release = True

if __name__ == '__main__':
    clearConsole()
    tutorial()

    actions.schedule.start()
    if release:
        # cron
        # 매 주 일요일 Investing.com 켈린더 확인
        actions.schedule.add_job(inv_check_calendar, 'cron', day_of_week='sun', id='check_calendar')

        # interval
        # 6시간마다 한 번씩 Investing.com 기사 확인
        actions.schedule.add_job(inv_check_article, 'interval', hours=6)
        # 5분마다 한 번씩 연합뉴스 기사 확인
        actions.schedule.add_job(yna_check_article, 'interval', minutes=5)
        # 30초마다 한 번씩 hedgehara 텔레그램 포스트 확인
        actions.schedule.add_job(tlg_check_post, 'interval', seconds=30, args=['hedgehara', hedgehara])

        logger("[Info] Start Sessions...")
        actions.schedule.print_jobs(out=log_file())
        logger("\n")
    else:
        pass

    time.sleep(3)
    clearConsole()
    show_menu()

    while True:
        if actions.is_job_done and not actions.question.application.is_running:
            show_menu()
