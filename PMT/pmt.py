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
import pmt

def main():
    
	P = pmt.from_long(23)
	print(type(P))
	print(P)
        
	P2 = pmt.from_complex(9j)
	print(type(P2))
	print(P2)

	print(pmt.is_complex(P2))
       	print(pmt.is_complex(P))


if __name__ == "__main__":
    main()
