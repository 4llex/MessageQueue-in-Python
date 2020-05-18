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
    mq_rx = posix_ipc.MessageQueue("/mqControlToPhy", posix_ipc.O_CREAT )
    mq_tx = posix_ipc.MessageQueue("/mqControlFromPhy", posix_ipc.O_CREAT )
    # 
    while True:
        
        data = mq_rx.receive()
        # print('MAC->PHY: %s' %data[0])
        # print('MAC->PHY: %s' %data[0].encode('hex'))
        print('MAC->PHY: %s (%s)' %(data[0], data[0].encode('hex')))
        
        if data[0] == 'A':
            mq_tx.send('AA')
            print('PHY->MAC: AA')

        mq_tx.send('F')
        print('PHY->MAC: F')
        time.sleep(4.6e-3)

        # while True:
        #     mq.send('F')
        #     print('PHY -> MAC: F')
        #     time.sleep(4.6e-3)


if __name__ == "__main__":
    main()
