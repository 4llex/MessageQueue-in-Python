#! /usr/bin/env python
# 
# stubL1 for L1/L2 integration.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc    # pip install posix_ipc
import time
from termcolor import cprint # sudo apt-get install -y python-termcolor
from datetime import datetime

def main():
    mq_rx = posix_ipc.MessageQueue("/mqPduToPhy", posix_ipc.O_CREAT )
    cprint(' ===> Waiting PDUs from MAC layer! ', 'yellow')
    # 
    while True:
        
        data = mq_rx.receive()
        cprint('%s' %(datetime.now()), 'blue')
        cprint('MAC->PHY: %s' %data[0].encode('hex'), 'red')
        print (' ')
        
        


if __name__ == "__main__":
    main()
