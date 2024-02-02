import os.path
import sys
from datetime import datetime

class Config:
    log_file_name = f'logs/logs_{datetime.now().strftime("%Y-%m-%d %I-%M-%S")}.txt'
    dir_name = os.path.dirname(log_file_name)


def logger(text):
    if not os.path.exists(Config.dir_name):
        os.makedirs(Config.dir_name, exist_ok=True)

    with open(Config.log_file_name, 'w') as file:
        print(f"[{datetime.now().strftime('%Y/%m/%d %I:%M:%S')}] {text}" if text != "\n" else "\n", file=sys.stderr, flush=True)


if __name__ == '__main__':
    pass