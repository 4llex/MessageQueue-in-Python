#! / usr / bin / env python
# 
# Message queue client side.
# 
# Reference: https://takuya-1st.hatenablog.jp/entry/2017/03/17/211530
# 

import json
import posix_ipc    # pip install posix_ipc
import time

mq = posix_ipc.MessageQueue("/my_q01")
mq.unlink()