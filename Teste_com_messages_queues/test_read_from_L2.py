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



def main():

    mq_rx = posix_ipc.MessageQueue("/mqControlToPhy", posix_ipc.O_CREAT )
    mq_tx = posix_ipc.MessageQueue("/mqControlFromPhy", posix_ipc.O_CREAT )
    cprint(' ===> Reading L2 msg! ', 'yellow')
    cont = 0;

    while True:
        
        data = mq_rx.receive()        
        cprint('    MAC->PHY: %s (%s)' %(data[0], data[0].encode('hex')), 'red')
	cont = cont + 1;
        #if cont == 5:
	#	mq_tx.send('AA')
	if data[0] == 'A':
		mq_tx.send('AA')
	cprint('reading buffer', 'blue')

if __name__ == "__main__":
    main()
