import sys
import time
import os

import pwd
import threading

from logger import *
from mgr_socket import *
from mgr_serial import *

# --- Modules ---


# ---------- Global Vars -----------

# ---------- MGR -----------

# -------------


# -------------

def _initialize():
    mgrSocketOpen()
    initSerial()
    print("Mgr Initialized.")
    sendData("Con\r\n")
    
def mgr():
    timeout_in_seconds = 1

    _initialize()

    deadline = time.time()

    while True:
        deadline += timeout_in_seconds
        mgrSocketService(deadline)

if __name__ == "__main__":
    mgr()
