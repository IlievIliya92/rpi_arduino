#!/usr/bin/python3
from logger import *

# --- Constants
LIGHT_TRESHOLD = 70

# --- lights class

class modesLights:
    light1Enable = False
    light1State = 0
    light1StatePrev = 0

    light2Enable = False
    light2State = 0

    lightsThreshold = LIGHT_TRESHOLD

# --- Modes control

class modesContol:
    def __init__(self):
        self.lights = modesLights()

    def _evaluateLights(self, value):
        if value < self.lights.lightsThreshold:
            return 1
        elif value >= self.lights.lightsThreshold:
            return 0

    def modesEnableLights(self, light, state):
        if light == 0:
            self.lights.light1Enable = state
        elif light == 1:
            self.lights.light2Enable = state

    def manageLights(self, valuel1, ser):
        if self.lights.light1Enable:
            self.lights.light1State = self._evaluateLights(valuel1)
            if self.lights.light1State != self.lights.light1StatePrev:
                self.lights.light1StatePrev = self.lights.light1State
                ser.lightEnable(0, self.lights.light1State)
