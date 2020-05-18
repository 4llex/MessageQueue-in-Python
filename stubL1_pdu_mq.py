#! /usr/bin/env python
# 
# stubL1 for L1/L2 integration.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc    # pip install posix_ipc
import time

def main():
    mq_rx = posix_ipc.MessageQueue("/mqPduToPhy", posix_ipc.O_CREAT )
    # 
    while True:
        
        data = mq_rx.receive()
        print('MAC->PHY: %s' %data[0].encode('hex'))
        
        


if __name__ == "__main__":
    main()
