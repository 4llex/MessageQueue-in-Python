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

        # List of message queues
        self.mq_rx = posix_ipc.MessageQueue('/mqControlToPhy', posix_ipc.O_CREAT )
        self.mq_tx = posix_ipc.MessageQueue('/mqControlFromPhy', posix_ipc.O_CREAT )
        self.pdu_mq_rx = posix_ipc.MessageQueue("/mqPduToPhy", posix_ipc.O_CREAT )

        self.pack_msg = '' # mensagem concatenada
        self.flag_pdu = 0
        
        # Create and start thread for getting messages from control queue
        t1 = threading.Thread(target=self.read_L2_message)
        t1.start()

        # Create and start thread for getting messages from PDU queue
        t2 = threading.Thread(target=self.read_L2_pdu)
        t2.start()

    
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
            time.sleep(4.6e-3)

    def read_L2_message(self):
        while True:
            data = self.mq_rx.receive()
            #cprint('    MAC->PHY: %s (%s)' %(data[0], data[0].encode('hex')), 'red')            
            #cprint(type(data[0]), 'yellow')

            if data[0] == 'A':
                self.send_AA()
                t1 = threading.Thread(target=self.send_ff)
                t1.start()
            elif data[0] == 'B':
                self.send_BA()
            elif data[0] == 'E':
                #time.sleep(4.3e-3)
                while self.flag_pdu == 0: # Espera PDU ser concatenado
                    time.sleep(1e-3)    
                self.pack_msg = self.pack_msg + data[0].encode('hex') # concatena o 'E'      
                self.flag_pdu = 0
                #cprint(data[0].encode('hex'),'yellow')
                # ----> cprint(' Concatenado -->  %s' %self.pack_msg, 'green')
                print(len(self.pack_msg))
            else: # C
                self.pack_msg = data[0].encode('hex')
                #cprint(self.pack_msg,'blue')

    
    def read_L2_pdu(self):
        while True:
            if self.flag_pdu == 0:
                pdu_data = self.pdu_mq_rx.receive()
                #cprint(' MAC->PHY: %s' %pdu_data[0].encode('hex'), 'green')
                self.pack_msg = self.pack_msg + pdu_data[0].encode('hex')
                self.flag_pdu = 1       
                #cprint(' Concatenado -->  %s' %self.pack_msg, 'green')


if __name__ == "__main__":
   application = StubL1()

    