#! /usr/bin/env python
# 
# stubL1 for L1/L2 integration.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc              # pip install posix_ipc
import time
from termcolor import cprint  # sudo apt-get install -y python-termcolor
from datetime import datetime
import threading



def send_ff():
    #print('Thread 1')
    while True:
            cprint('Conteudo da thread 1', 'red')
            #time.sleep(1)


def main():

    flag = 0
    cprint(' ===> Waiting for L2 layer command! ', 'yellow')
    
    while True:
        
        cprint('Main','blue')
        time.sleep(1)
        if flag == 0:
            flag = 1
            t1 = threading.Thread(target=send_ff)
            t1.start()
        
  


if __name__ == "__main__":
    main()

    