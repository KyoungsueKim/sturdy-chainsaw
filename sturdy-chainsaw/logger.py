import os.path
from datetime import datetime

class Config:
    log_file_name = f'logs/logs_{datetime.now().strftime("%Y-%m-%d %I-%M-%S")}.txt'


def logger(text):
    with open(Config.log_file_name, 'w') as file:
        print(f"[{datetime.now().strftime('%Y/%m/%d %I:%M:%S')}] {text}" if text != "\n" else "\n", file=file, flush=True)


if __name__ == '__main__':
    pass