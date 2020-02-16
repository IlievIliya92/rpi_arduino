#!/usr/bin/python3
from logger import *

# --- Constants

# --- lights class

class modesLights:
    light1Enable = False
    light1State = 0
    light1StatePrev = 0

    light2Enable = False
    light2State = 0
    light2StatePrev = 0

# --- Modes control

class modesContol:
    def __init__(self):
        self.lights = modesLights()

    def _evaluateLights(self, value, setpoint):
        if value < setpoint:
            return 1
        elif value >= setpoint:
            return 0

    def modesEnableLights(self, light, state):
        if light == 0:
            self.lights.light1Enable = state
        elif light == 1:
            self.lights.light2Enable = state

    def manageLights(self, valuel1, setpoint, ser):
        if self.lights.light1Enable:
            self.lights.light1State = self._evaluateLights(valuel1, setpoint)
            if self.lights.light1State != self.lights.light1StatePrev:
                self.lights.light1StatePrev = self.lights.light1State
                ser.lightEnable(0, self.lights.light1State)
