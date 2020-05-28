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


class StubL1:
    
    def __init__(self):

        cprint(' ===> Waiting for L2 layer command! ', 'yellow')

        #self.flag = 0
        # List of message queues
        self.mq_rx = posix_ipc.MessageQueue('/mqControlToPhy', posix_ipc.O_CREAT )
        self.mq_tx = posix_ipc.MessageQueue('/mqControlFromPhy', posix_ipc.O_CREAT )
        
        # Create and start thread for getting messages from control queue
        t1 = threading.Thread(target=self.read_L2_message)
        t1.start()

        # Create and start thread for getting messages from PDU queue
        #t2 = threading.Thread(target=self.get_mq_pdu_to_phy)
        #t2.start()


    def send_AA(self):
        self.mq_tx.send('AA')
        print('PHY->MAC: AA')

    def send_BA(self):
        self.mq_tx.send('BA')
        print('PHY->MAC: BA')

    def send_ff(self):
        print('PHY -> MAC: F')
        while True:
            self.mq_tx.send('F')
            #print('PHY -> MAC: F')
            time.sleep(4.6e-3)
            #time.sleep(1)

    def read_L2_message(self):
        while True:
            data = self.mq_rx.receive()
            cprint('    %s' %(datetime.now()), 'blue')
            cprint('    MAC->PHY: %s (%s)' %(data[0], data[0].encode('hex')), 'red')
            if data[0] == 'A':
                self.send_AA()
                t1 = threading.Thread(target=self.send_ff)
                t1.start()
                # if flag==0:
                #     flag = 1
                #     t1 = threading.Thread(target=send_ff)
                #     t1.start()
            if data[0] == 'B':
                self.send_BA()
      

if __name__ == "__main__":
   application = StubL1()

    