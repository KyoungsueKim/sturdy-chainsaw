import logging
import time
from base import clearConsole
from actions import *
from logger import logger, log_file

release = True
version = "1.1.1"

if __name__ == '__main__':
    sys.stderr = log_file()
    clearConsole()
    tutorial()

    actions.schedule.start()
    if release:
        # cron
        # 매 주 일요일 Investing.com 켈린더 확인
        actions.schedule.add_job(inv_check_calendar, 'cron', day_of_week='sun', id='check_calendar')

        # interval
        # 6시간마다 한 번씩 Investing.com 기사 확인
        actions.schedule.add_job(inv_check_article, 'interval', hours=1)
        # 3시간마다 한 번씩 gunhey 네이버 블로그 확인
        actions.schedule.add_job(naver_check_post, 'interval', hours=3, args=['gunhey', gunhey])
        # 5분마다 한 번씩 연합뉴스 경제 기사 확인
        actions.schedule.add_job(yna_check_economy, 'interval', minutes=5)
        # 5분마다 한 번씩 연합뉴스 긴급 기사 확인
        actions.schedule.add_job(yna_check_break, 'interval', minutes=1, seconds=1)
        # 5분마다 한 번씩 hyottchart 텔레그램 포스트 확인
        actions.schedule.add_job(tlg_check_post, 'interval', minutes=5, seconds=2, args=['hyottchart', hyottchart])
        # 5분마다 한 번씩 bumgore 텔레그램 포스트 확인
        # actions.schedule.add_job(tlg_check_post, 'interval', minutes=5, seconds=3, args=['bumgore', bumgore])
        # 5분마다 한 번씩 Macrojunglefortarzan 텔레그램 포스트 확인
        actions.schedule.add_job(tlg_check_post, 'interval', minutes=5, seconds=4, args=['Macrojunglefortarzan', Macrojunglefortarzan])
        # 30초마다 한 번씩 hedgehara 텔레그램 포스트 확인
        # actions.schedule.add_job(tlg_check_post, 'interval', seconds=30, args=['hedgehara', hedgehara])
        # 5분마다 한 번씩 MacroAllocation 텔레그램 포스트 확인
        actions.schedule.add_job(tlg_check_post, 'interval', minutes=5, seconds=3, args=['MacroAllocation', MacroAllocation])

        logger("[Info] Start Sessions...")
        actions.schedule.print_jobs(out=log_file())
        logger("\n")
    else:
        pass

    time.sleep(1.5)
    clearConsole()
    show_menu()

    while True:
        if actions.is_job_done and not actions.question.application.is_running:
            show_menu()
