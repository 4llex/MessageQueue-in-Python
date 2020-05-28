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

def send_AA(mq_tx):
    mq_tx.send('AA')
    print('PHY->MAC: AA')


def send_ff(mq_tx):
    print('PHY -> MAC: F')
    while True:
        mq_tx.send('F')
        #print('PHY -> MAC: F')
        time.sleep(4.6e-3)
        #time.sleep(1)

def read_L2_message(flag,mq_rx,mq_tx):
    data = mq_rx.receive()
    cprint('    %s' %(datetime.now()), 'blue')
    cprint('    MAC->PHY: %s (%s)' %(data[0], data[0].encode('hex')), 'red')
    if data[0] == 'A':
        send_AA(mq_tx)
        t1 = threading.Thread(target=send_ff(mq_tx))
        t1.start()
            # if flag==0:
            #     flag = 1
            #     t1 = threading.Thread(target=send_ff)
            #     t1.start()
    


def main():
    mq_tx = posix_ipc.MessageQueue("/mqControlFromPhy", posix_ipc.O_CREAT )
    mq_rx = posix_ipc.MessageQueue("/mqControlToPhy", posix_ipc.O_CREAT )


    flag = 0
    cprint(' ===> Waiting for L2 layer command! ', 'yellow')

    t2 = threading.Thread(target=read_L2_message(flag,mq_rx,mq_tx))
    t2.start()
        
        
        
            
        

if __name__ == "__main__":
    main()

    