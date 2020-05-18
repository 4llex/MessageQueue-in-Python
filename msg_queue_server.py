#! / usr / bin / env python
# 
# Message queue server side.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc    # pip install posix_ipc
import time

def  main():
    mq = posix_ipc.MessageQueue("/my_q01", posix_ipc.O_CREAT)
    # 
    cnt = 0 
    # 
    while  True:
        cnt = cnt + 1 
        obj = {"counter": cnt}
        mq.send(json.dumps(obj))
        print("pushed:% d" % cnt)
        time.sleep(1)


if __name__ == "__main__" :
    main ()