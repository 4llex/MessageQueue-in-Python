#! / usr / bin / env python
# 
# Message queue server side.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc    # pip install posix_ipc
import time

# mq_send(mq, (char *) &i, sizeof(i), 0);

def  main():
    mq = posix_ipc.MessageQueue("/mqPduToPhy", posix_ipc.O_CREAT)
    # 
    cnt = 0 
    # 
    while  True:
        cnt = cnt + 1 
        obj = {"A":cnt}
        mq.send(json.dumps(obj))
	#mq_send(mq, (char *) &i, sizeof(i), 0);
	print(obj)	
        #print("pushed:% d" % cnt)
        time.sleep(1)


if __name__ == "__main__" :
    main ()
