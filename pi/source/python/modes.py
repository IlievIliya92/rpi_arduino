#!/usr/bin/python3

import json
import os

from constants import *
from logger import *

def smartLight(lightValue, treshold):
    if (lightValue < treshold):
        return True
    return False



