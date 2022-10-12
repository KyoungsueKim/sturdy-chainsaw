import os.path
from datetime import datetime

log_file_stream = None


# 로그 파일 없으면 생성
def log_file():
    global log_file_stream
    if log_file_stream is None:
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        file = open(f'logs/logs_{datetime.now().strftime("%Y-%m-%d %I-%m-%S")}.txt', 'w')
        log_file_stream = file

    return log_file_stream


def logger(text: str):
    print(f"[{datetime.now()}] {text}" if text != "\n" else "\n", file=log_file(), flush=True)


if __name__ == '__main__':
    pass