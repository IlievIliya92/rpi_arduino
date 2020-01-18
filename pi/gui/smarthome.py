#!/usr/bin/python3

import json
import os
import sys
import remi.gui as gui
from remi import start, App
from threading import Timer

from constants import *
from soundplayer import *
from serialcom import *
from logger import *
from modes import *
from styles import *

_usernNames = {'0':'Test User', '1':'Test User', '2':'Test User'}

class smartHome(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        # static_file_path can be an array of strings allowing to define
        #  multiple resource path in where the resources will be placed
        super(smartHome, self).__init__(*args, static_file_path=res_path)

    def idle(self):
        pass
        self.temperature0.set_text('Living Room: ' + str(self.temp0)  + DEGREES)
        self.progress0.set_value(self.temp0)
        self.temperature1.set_text('Bedroom: ' + str(self.temp1)  + DEGREES)
        self.progress1.set_value(self.temp1)
        self.lightvalue0.set_text('Light: ' + str(self.light)  + ' %')
        self.progress2.set_value(self.light)

    def bodyUpdate(self, color, opa, favicon):
        self.page.children['body'].style['background-color'] = color
        self.page.children['body'].style['opacity'] = opa
        self.page.children['head'].set_icon_file("/res:" + favicon)

        self.execute_javascript("location.reload(true);")

    def main(self):
        # --- Serial comm Object --- #
        try:
            self.ser = SerialCom()
        except Exception as e:
            print(e)
            sys.exit()


        # --- --- ---  --- BODY Properties --- --- --- --- --- --- ---  #
        self.bodyUpdate(DARK, '0.8', FAVICON_DIS)
#        self.page.children['body'].style['white-space'] = 'pre-wrap'
        # --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---   #

        #--- --- --- --- ---  Menu panel --- --- --- --- --- #
        menu = gui.Menu(width='99%', height=22, style=MENU)
        self.home = gui.MenuItem(HOME, width='10%', height=22, style=HOMESTYLE)
        self.home.onclick.connect(self.home_clicked)
        self.connectStatus = gui.MenuItem('Connect', width='120%', height=22, style=CONNECT)
        self.connectStatus.onclick.connect(self.connect_clicked)
        self.home.append([self.connectStatus])

        modes = gui.MenuItem(MODESSYMBOL, width='10%',
                                          height=22,
                                          style={'border': '2px solid azure', 'background-color': BTN_BCK,
                                                 'color': BTN_CLR, 'border-radius': BTN_RAD})
        modes.onclick.connect(self.modes_clicked)

        modeslbl = gui.MenuItem("Modes", width='200%', height=22, style=MENU_LV1)
        modes.append(modeslbl)

        security = gui.MenuItem(KEY, width='10%', height=22, style=MENU_LV1)
        security.onclick.connect(self.security_clicked)
        securitylbl = gui.MenuItem("Security configuration", width='200%', height=22, style=MENU_LV1)
        security.append(securitylbl)

        entertainment = gui.MenuItem(MUSIC, width='10%', height=22, style=MENU_LV1)
        entertainment.onclick.connect(self.entertainment_clicked)
        entertainmentlbl = gui.MenuItem("Entertainment", width='200%', height=22, style=MENU_LV1)
        entertainment.append(entertainmentlbl)

        lights = gui.MenuItem(SUN, width='10%', height=22, style=MENU_LV1)
        lights.onclick.connect(self.lights_clicked)
        lightslbl = gui.MenuItem("Lights Configuration", width='200%', height=22, style=MENU_LV1)
        lights.append(lightslbl)

        heater = gui.MenuItem(TERMOMETER, width='10%', height=22, style=MENU_LV1)
        heater.onclick.connect(self.heater_clicked)
        heaterlbl = gui.MenuItem("Heaters Configuration", width='200%', height=22, style=MENU_LV1)
        heater.append(heaterlbl)

        menu.append([self.home, modes, security, lights, heater, entertainment])
        menubar = gui.MenuBar(width='100%', height='22px')
        menubar.append(menu)
        # --- --- --- --- --- --- --- --- --- --- #



        # --- --- --- --- --- Header Container --- --- --- --- --- #
        headerCont = gui.Widget(width='98%', height=46, margin='5px', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, style=CONTAINER)

        self.title = gui.Label('HOME', width='55%', height=24, margin='4px',
                                       style=TITLE)
        headerCont.append([self.title])
        # --- --- --- --- --- --- --- --- --- --- --- --- --- --- #

        # --- --- --- --- HOME --- --- --- --- ---  #
        self.homeContainer = gui.Widget(width='90%', height='70%', margin='5px auto', style=CONTAINER)

        # --- --- --- Left panel --- --- --- #
        subContainerLeft = gui.Widget(width='50%', margin='8px, 0px, 0px, 0px', style=CONTAINER)

        # --- --- Presence Monitor --- --- #
        self.presenseCont = gui.Widget(width='80%', height='50%', margin='4%', style=CONTAINER)
        self.presenseLabel = gui.Label('Presence Monitor', width='96%', height=20, margin='8px', style=TEXT)

        self.user0 = gui.Label(_usernNames['0'] + MISSING, width='100%', height=20, margin='0px', style=USER_LBL)
        self.user1 = gui.Label(_usernNames['1'] + CHECKED, width='100%', height=20, margin='0px', style=USER_LBL)
        self.user2 = gui.Label(_usernNames['2'] + CHECKED, width='100%', height=20, margin='0px', style=USER_LBL)

        self.presenseCont.append([self.presenseLabel, self.user0, self.user1, self.user2])
        subContainerLeft.append([self.presenseCont])
        # --- --- --- --- --- --- --- --- --- --- #

        # --- --- ---  Right panel  --- --- --- #
        subContainerRight = gui.Widget(width='50%', style=CONTAINER)

        # ---Temp display --- #
        self.tempCont = gui.Widget(width='90%', height='90%',  margin='4%', style=CONTAINER)

        self.tempLabel = gui.Label('Temperatute Monitor', width='96%', height=20, margin='4px', style=TEXT)

        self.temp0 = 0
        self.progress0 = gui.Progress(0, 1000, width='100%', height=4, margin='0px', color='red', style=PROGRESSBAR)
        self.temperature0 = gui.Label('', width='100%', height=20, margin='0px', style=TEXT)

        self.temp1 = 0
        self.progress1 = gui.Progress(0, 1000, width='100%', height=4, margin='0px', color='red', style=PROGRESSBAR)
        self.temperature1 = gui.Label('', width='100%', height=20, margin='0px',style=TEXT)

        self.tempCont.append([self.tempLabel, self.progress0, self.temperature0, self.progress1, self.temperature1])

        self.lightCont = gui.Widget(width='90%', height='90%', margin='4%', style=CONTAINER)
        self.lightLabel = gui.Label('Light Monitor', width='96%', height=20, margin='4px', style=TEXT)

        self.light = 0
        self.progress2 = gui.Progress(0, 1000, width='100%', height=4, margin='0px', color='red', style=PROGRESSBAR)
        self.lightvalue0 = gui.Label('', width='100%', height=20, margin='0px', style=TEXT)

        self.lightCont.append([self.lightLabel, self.progress2, self.lightvalue0])


        subContainerRight.append([self.tempCont, self.lightCont])
        # --- --- --- --- --- --- --- --- --- --- #

        # --- --- --- Horizontal panel --- --- --- #
        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px', style=CONTAINER)

        horizontalContainer.append([subContainerLeft, subContainerRight])
        # --- --- --- --- --- --- --- --- --- --- #

        self.homeContainer.append([menubar, headerCont, horizontalContainer])
        # --- --- --- --- HOME END --- --- --- --- ---  #

        # --- --- --- --- ENTERTAINMENT  --- --- --- --- #
        self.entertainmentContainer = gui.Widget(width='90%', height='100%', margin='5px auto', style=CONTAINER)

        self.musicLabel = gui.Label('Music', width='30%', height=22, margin='4px', style=TEXT)
        # --- Music Player object --- #
        self.musicPlayer = Player(150)

        musicPlayerCont = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px', height= 30, style=CONTAINER)

        self.playBtn = gui.Button(START, width='10%', height=22, margin='4px', style=BTN)
        self.playBtn.onclick.connect(self.playBtn_clicked)

        self.nextBtn = gui.Button(NEXT, width='10%', height=22, margin='4px', style=BTN)
        self.nextBtn.onclick.connect(self.nextBtn_clicked)

        self.prevBtn = gui.Button(PREVIOUS, width='10%', height=22, margin='4px', style=BTN)
        self.prevBtn.onclick.connect(self.prevBtn_clicked)

        self.sliderVol = gui.Slider(10, 0, 100, 5, width='30%', height=22, margin='4px', style=SLIDER)
        self.sliderVol.onchange.connect(self.sliderVol_changed)

        self.songTitle = gui.Label(' ', width='30%', height=24, margin='2px', style=TEXT)

        self.img0 = gui.Image('/res:tashSultanaCover.jpg', width=240, height=240, margin='10px')
        self.img1 = gui.Image('/res:keranaLogo.jpg', width=240, height=240, margin='10px')
        self.img2 = gui.Image('/res:andersonLogo.jpg', width=240, height=240, margin='10px')
        self.img3 = gui.Image('/res:nirvanalogo.jpg', width=240, height=240, margin='10px')

        self.playBtn.onclick.connect(self.playBtn_clicked)

        musicPlayerCont.append([self.prevBtn, self.playBtn, self.nextBtn, self.sliderVol, self.songTitle])

        self.entertainmentContainer.append([menubar, headerCont, self.musicLabel, musicPlayerCont, self.img0, self.img1, self.img2, self.img3])
        # --- --- --- --- ENTERTAINMENT END --- --- --- --- #

        # --- --- --- --- MODES  --- --- --- ---#
        self.modesContainer = gui.Widget(width='90%', height='70%', margin='5px auto', style=CONTAINER)

        self.modesCont = gui.Widget(width='80%', height='50%', style=CONTAINER)

        self.smartLight = gui.CheckBoxLabel(SUN, False, width='30%', height='10%', margin='10px', style=CB)
        self.smartLightTresh = gui.TextInput(width='30%', height='10%', margin='10px', style=TEXT_INPUT)
        self.smartLightTresh.set_text('25 %')

        self.smartHeater = gui.CheckBoxLabel(TERMOMETER, False, width='30%', height='10%', margin='10px', style=CB)
        self.smarHeaterTresh = gui.TextInput(width='30%', height='10%', margin='10px', style=TEXT_INPUT)
        self.smarHeaterTresh.set_text('25 ' + DEGREES)

        '''
        self.description0 = gui.Label(SUN + ' - SmartLights mode controls your lights automaticaly depending on light level', width='80%', height=50, margin='4px',
                                    style={'display': 'block', 'text-align': 'left',
                                           'overflow': 'visible', #'border': '1px solid bisque',
                                           'background-color': BCK, 'color': TEXT_COL,
                                           'font-size': '100%'})

        self.description1 = gui.Label(TERMOMETER + ' - Smart Heater mode controls your heater automaticaly depending on temperature level', width='80%', height=50, margin='4px',
                                     style={'display': 'block', 'text-align': 'left',
                                           'overflow': 'visible', #'border': '1px solid bisque',
                                           'background-color': BCK, 'color': TEXT_COL,
                                           'font-size': '100%'})
        '''
        self.smartLight.onchange.connect(self.on_check_smartL)
        self.modesCont.append([self.smartLight, self.smartLightTresh, self.smartHeater, self.smarHeaterTresh])

        self.modesContainer.append([menubar, headerCont, self.modesCont])
        # --- --- --- --- MODES END --- --- --- ---#

        # --- --- --- --- LIGHTS --- --- --- ---#
        self.lightsContainer = gui.Widget(width='90%', height='70%', margin='5px auto', style=CONTAINER)
        self.lightsContainer.append([menubar, headerCont])
        # --- --- --- --- LIGHTS END --- --- --- ---#


        # --- --- --- --- HEATER --- --- --- ---#
        self.heaterContainer = gui.Widget(width='90%', height='70%', margin='5px auto', style=CONTAINER)

        self.heaterContainer.append([menubar, headerCont])
        # --- --- --- --- HEATER END --- --- --- ---#

        # --- --- --- --- SECURITY --- --- --- ---#
        self.securityContainer  = gui.Widget(width='90%', height='70%', margin='5px auto', style=CONTAINER)

        self.securityContainer.append([menubar, headerCont, subContainerLeft])
        # --- --- --- --- SECURITY END --- --- --- ---#

        # this flag will be used to stop the measure Timer
        self.stop_measure = False

        # this flag will be used to stop the modes Timer
        self.stop_modes = False

        # --- Start Functions --- #
        self.measure()
        self.modes()

        # returning the root widget
        return self.homeContainer

    def measure(self):
        if self.ser.isConnected():
            self.temp0, self.temp1, self.light, humidity, empty = self.ser.readAdcData()

        if not self.stop_measure:
            Timer(10, self.measure).start()

    def modes(self):
        if self.ser.isConnected() and self.smartLight.get_value():
            try:
                if smartLight(self.light, LIGHT_TRESHOLD):
                    self.ser.lightEnable(1, 1)
                else:
                    self.ser.lightEnable(1, 0)
            except Exception as e:
                pass

        if not self.stop_modes:
            Timer(50, self.modes).start()

    # listener functions
    def onload(self, emitter):
        print(">>>>>>>>> ON PAGE LOADED")

    def onerror(self, emitter, message, source, line, col):
        print(">>>>>>>>> ON ERROR: %s\n%s\n%s\n%s"%(message, source, line, col))
        self.execute_javascript('document.onkeydo')

    def home_clicked(self, widget):
        buttonClick(0)
        self.set_root_widget(self.homeContainer)
        self.title.set_text('HOME')
        print('home')

    def modes_clicked(self, widget):
        buttonClick(0)
        self.set_root_widget(self.modesContainer)
        self.title.set_text('MODES')
        print('modes')

    def entertainment_clicked(self, widget):
        buttonClick(0)
        self.set_root_widget(self.entertainmentContainer)
        self.title.set_text('ENTERTAINMENT')
        print('entertainment')

    def security_clicked(self, widget):
        buttonClick(0)
        self.set_root_widget(self.securityContainer)
        self.title.set_text('SECURITY CONFIGURATION')
        print('security')

    def lights_clicked(self, widget):
        buttonClick(1)
        self.set_root_widget(self.lightsContainer)
        self.title.set_text('LIGHTS CONFIGURATION')
        print('lights')

    def heater_clicked(self, widget):
        buttonClick(1)
        self.set_root_widget(self.heaterContainer)
        self.title.set_text('HEATERS CONFIGURATION')
        print('heater')

    def connectSym_clicked(self):
        print('Connect')

    def connect_clicked(self, widget):
        if self.ser.isConnected():
            if self.ser.disconnect():
                self.connectStatus.set_text('Connect')
                self.bodyUpdate(DARK, '0.8', FAVICON_DIS)
                self.home.set_text(HOME)
        else:
            if self.ser.connect():
                self.connectStatus.set_text('Disconnect')
                self.bodyUpdate(DARK, '1', FAVICON_ENB)
                self.home.set_text(HOMEON)

    def on_check_smartL(self, widget, newValue):
        if newValue == True:
            print('smartLight mode')
        elif newValue == False:
            print('smartLight mode stop')

    # --- Music Player --- #
    def playBtn_clicked(self, widget):
        if self.musicPlayer.isPlaying():
            self.musicPlayer.pause()
            self.songTitle.set_text(' ')
        else:
            self.musicPlayer.play()
            song = self.musicPlayer.getTitle()
            self.songTitle.set_text('Playing: ' + song.strip('.mp3').replace('-', ' Track: '))

    def nextBtn_clicked(self, widget):
        self.musicPlayer.next()
        song = self.musicPlayer.getTitle()
        self.songTitle.set_text('Playing: ' + song.strip('.mp3').replace('-', ' Track: '))

    def prevBtn_clicked(self, widget):
        self.musicPlayer.previous()
        song = self.musicPlayer.getTitle()
        self.songTitle.set_text('Playing: ' + song.strip('.mp3').replace('-', ' Track: '))

    def sliderVol_changed(self, widget, value):
        result = self.sliderVol.get_value()
        self.musicPlayer.setVol(result)

    def on_close(self):
        """ Overloading App.on_close event to stop the Timer.
        """
        self.stop_measure = True
        self.stop_modes = True

        if self.musicPlayer.isPlaying():
            self.musicPlayer.stop()

        if self.ser.isConnected():
            self.ser.disconnect()

        super(smartHome, self).on_close()

# starts the webserver
if __name__ == "__main__":
# starts the webserver
#    import ssl
    start(smartHome, debug=True, address='0.0.0.0', port=8081, start_browser=False, multiple_instance=True) #username='Iliya', password='admin'
