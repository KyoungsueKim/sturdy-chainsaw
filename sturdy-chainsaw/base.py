import subprocess
import sys, os, time
import requests, platform, pyautogui
import chromedriver_autoinstaller as AutoChrome
from pyperclip import copy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = None

WAIT_TIME = 5


class position:
    text = [0, 0]
    explorer = [0, 0]


def getSoup(url: str) -> BeautifulSoup:
    req = requests.get(url=url, verify=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def getDynamicSoup(url: str, commands: list) -> BeautifulSoup:
    global driver
    driver_path = "chromedriver"

    try:
        # 아직 드라이버가 없다면
        if driver is None:
            # 크롬 드라이버 저장 경로가 없다면 새로 생성
            if not os.path.isdir(driver_path):
                print("chromedriver 폴더를 새로 생성합니다.")
                os.makedirs(driver_path)

            # 크롬 드라이버 자동 업데이트
            AutoChrome.install(path=driver_path, no_ssl=True)

            version = AutoChrome.get_chrome_version().split('.')[0]

            service = Service(f'{driver_path}/{version}/chromedriver')
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ['enable-logging'])
            options.add_argument("--headless")

            # 드라이버 생성
            driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        # 커맨드 실행
        commands.append('window.scrollTo(0, document.body.scrollHeight)')
        for command in commands:
            driver.implicitly_wait(5)
            time.sleep(1)
            driver.execute_script(command)
        driver.implicitly_wait(5)
        time.sleep(1)

        # soup 리턴
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    except Exception as e:
        print(f"드라이버 생성 에러. {e.args}", file=sys.stderr)


def openImagePath():
    if not os.path.isdir('images'):
        os.mkdir('images')
    path = os.path.abspath('images')
    command = f'explorer {path}' if platform.system() == 'Windows' else f'open {path}'
    os.system(command)


def sendText(text):
    copy(text)
    pyautogui.moveTo(position.text)
    pyautogui.click()
    time.sleep(0.1)

    ctrl = 'ctrl' if platform.system() == 'Windows' else 'command'
    pyautogui.hotkey(ctrl, 'v')
    time.sleep(1)
    pyautogui.press('Enter')


def sendImages():
    # 컨트롤 키 배정
    ctrl = 'ctrl' if platform.system() == 'Windows' else 'command'

    if platform.system() == 'Windows':  # windows
        # 1. 파일탐색기로 가서 클릭
        pyautogui.click(position.explorer)

        # 2. Ctrl + A를 눌러 파일 전체 선택 후 마우스 30만큼 오른쪽으로 이동
        pyautogui.hotkey(ctrl, 'a')
        pyautogui.moveTo(position.explorer[0] + 30, position.explorer[1], duration=1)
        time.sleep(0.1)

        # 3. 카톡창으로 드래그
        pyautogui.dragTo(position.text, duration=2, button='left')
        time.sleep(0.1)

        # 4. 카톡창 한번 클릭하고 엔터 눌러서 보내기.
        pyautogui.click(position.text)
        time.sleep(0.1)
        pyautogui.press('Enter')

        for i in range(WAIT_TIME):
            time.sleep(1)
            print(i, end=" ")

    else:  # mac os
        # 1. 파일탐색기 가서 한번 클릭.
        pyautogui.click(position.explorer)
        time.sleep(0.1)

        # 2. Ctrl + A 누르고 Ctrl + C로 전체 복사 하기
        pyautogui.hotkey(ctrl, 'a')
        time.sleep(0.1)
        pyautogui.hotkey(ctrl, 'c')

        # 3. 카카오톡 채팅창 가서 한번 클릭
        pyautogui.click(position.text)
        time.sleep(1)

        # 4. 붙여넣기 하고 엔터 두 번 눌러서 최종 발송하기
        pyautogui.hotkey(ctrl, 'v')
        pyautogui.press('Enter')
        time.sleep(0.1)
        pyautogui.press('Enter')

        for i in range(WAIT_TIME):
            time.sleep(1)
            print(i, end=" ")

    # 5. 이미지 폴더 내용 싹 비우기
    deleteImages()


def saveImages(url: str, index=0):
    path = os.path.abspath('images')
    type = os.path.splitext(url)[-1]
    os.system(f'curl {url} > {path}/{index}{type}')
    time.sleep(WAIT_TIME) # For download wait


def deleteImages():
    for file in os.scandir('images'):
        os.remove(file.path)


def clearConsole():
    print("\n" * 10)
    os.system('cls' if platform.system() == 'Windows' else 'clear')