#! / usr / bin / env python
# 
# Message queue client side.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc    # pip install posix_ipc
import time

#mq = posix_ipc.MessageQueue("/my_q01")
#mq.unlink()

mq0 = posix_ipc.MessageQueue("/mqControlToPhy")
mq1 = posix_ipc.MessageQueue("/mqControlFromPhy")
mq2 = posix_ipc.MessageQueue("/mqPduToPhy")
mq3 = posix_ipc.MessageQueue("/mqControlFromPhy")
mq0.close()
mq1.close()
mq2.close()
mq3.close()

mq0.unlink()
mq1.unlink()
mq2.unlink()
mq3.unlink()
