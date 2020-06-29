#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import string
import numpy
from gnuradio import gr
import pmt
import threading
import posix_ipc    # pip install posix_ipc
import time


class l1l2_integration(gr.basic_block):
    """
    l1l2_integration block
    """
    def __init__(self, msq_queue_01, msq_queue_02, msq_queue_03, msq_queue_04):
        gr.basic_block.__init__(self,
                                name="l1l2_integration",
                                in_sig=None,
                                out_sig=None)

        # Message Passing API, Ports declaration
        self.message_port_register_out(pmt.intern('pdus'))
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

        # List of message queues
        self.mq_control_rx = posix_ipc.MessageQueue('/' + msq_queue_01, posix_ipc.O_CREAT )
        self.mq_control_tx = posix_ipc.MessageQueue('/' + msq_queue_02, posix_ipc.O_CREAT )
        self.mq_pdu_rx = posix_ipc.MessageQueue('/' + msq_queue_03, posix_ipc.O_CREAT )
        self.mq_pdu_tx = posix_ipc.MessageQueue('/' + msq_queue_04, posix_ipc.O_CREAT )

        # mensagem concatenada
        self.pack_msg = '' 

        # Create and start thread for getting messages from control queue
        t1 = threading.Thread(target=self.read_L2_message)
        t1.start()

        print('    ')
        print(' Esse eh um print teste top:  L1-L2 Integration Block')
        print('    ')

    def send_AA(self):
        self.mq_control_tx.send('AA')

    def send_BA(self):
        self.mq_control_tx.send('BA')

    def send_ff(self):
        while True:
            self.mq_control_tx.send('F')
            time.sleep(4.6e-3)

    def read_L2_message(self):
        while True:
            
            data = self.mq_control_rx.receive()

            if data[0] == 'A':
                self.send_AA()
                t2 = threading.Thread(target=self.send_ff)            # Thread to send FF(TX indication) to L2 layer
                t2.start()
                self.pack_msg = ''
            elif data[0] == 'B':
                self.send_BA()
            elif data[0][0] == 'C':
                self.pack_msg = data[0]                               # Concatena 'C' - SubFrameTXStart
                pdu = self.mq_pdu_rx.receive()                        # Read PDU queue from L2      
                self.pack_msg = self.pack_msg + pdu[0]                # Concateda 'PDU'(MAC Ct + MAC PDUs)
            elif data[0] == 'E':
                self.pack_msg = self.pack_msg + data[0]               # Concatena o 'E' - SubFrameTXEnd      
                send_str = pdu[0] #self.pack_msg            
                send_pmt = pmt.make_u8vector(len(send_str), ord(' ')) # Create an empty PMT (contains only spaces):            
                for i in range(len(send_str)):                        # Copy all characters to the u8vector:
                    pmt.u8vector_set(send_pmt, i, ord(send_str[i]))
                self.handle_pdu_from_l2(send_pmt)
    
    def handle_pdu_from_l2(self, pdu):
        self.message_port_pub(pmt.intern('pdus'), pmt.cons(pmt.PMT_NIL, pdu)) # Publica mensagem (SubframeStart + PDUs + SubframeEnd) no output do bloco.

    
    # Implementação da parte de subida do PDU: L1->L2
    def send_C(self): # "C + RXMetrics struct" to L2
        self.mq_control_tx.send('C')
        print('Sent C to L2')
    
    def send_E(self):
        self.mq_control_tx.send('E')
        print('Sent E to L2')

    def send_pdu_to_l2(self, pdu): # Envia pdu recebido como Message Passing na entrada para L2.
        self.mq_pdu_tx.send(pdu)

    def handle_msg(self, msg_pmt):
        time.sleep(5e-3)
        print('Esta mensagem foi recebida!!!')

        # Collect message, convert to Python format:
        msg = pmt.cdr(msg_pmt)
        # Convert to string:
        msg_str = "".join([chr(x) for x in pmt.u8vector_elements(msg)])
        print(msg_str.encode('hex'))

        self.send_C()
        self.send_pdu_to_l2(msg_str)
        self.send_E()