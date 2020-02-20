#!/usr/bin/python3

import sqlite3
import os
import time
import constructors as cstr

from constructors import TEMP_GRAPH_STYLE, LIGHT_GRAPH_STYLE
from remi import start, App
from modes import modesContol
from serialcom import SerialCom
from threading import Timer


from utils import *
from constants import *
from logger import *

# --- Smart Home app
class smARTHome(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'remi/res')
        super(smARTHome, self).__init__(*args, static_file_path={'resources':res_path})

    def idle(self):
        if self.ser.isConnected():
            self.modes.manageLights(self.light1.getLast(), self.lightSetPoint, self.ser)

        pass

    def main(self):
        # --- --- --- --- State  --- --- --- --- --- #
        self.ser = SerialCom(ARD_DEVICE_ID)
        self.modes = modesContol()
        self.lightSetPoint = 60
        self.serConnected = False
        self.stop_measure = False

        # --- --- --- --- --- --- --- --- --- --- --- #


        # --- --- --- --- BODY --- --- --- --- --- ---#
        self.page.children['head'].set_icon_file("/resources:favicon.ico")
        # --- --- --- --- --- --- --- --- --- --- --- #

        self.homeBtn = cstr.createButton("smART\nHOME", 'auto', 'auto',
                                         "gp_button", self.homeBtn_clicked)
        self.homeBtnCOnt = cstr.createContainer('100%', '4%', "outliner", "horizontal")
        self.homeBtnCOnt.append(self.homeBtn)


        self.connectBtn = cstr.createButton("Connect", 'auto', 'auto',
                                            "gp_button", self.connectBtn_clicked)
        self.connectStatus = cstr.createLabel("", 'auto', '40%', "gp_button")

        self.connectBtnCOnt = cstr.createContainer('100%', 'auto', "outliner", "vertical")
        self.connectBtnCOnt.append([self.connectBtn, self.connectStatus])
        cstr.modifyStyle(self.connectBtnCOnt, {'top':'30%'})


        # --- --- --- --- --- Home Container --- --- --- --- --- #
        self.homeContainer = cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralContainer = cstr.createContainer('90%', '50%', "menu_Container", "horizontal")
        self.menuBtn =cstr.createButton('O', '5%', 'auto', "menu_button", self.menuBtn_clicked)
        self.menuBtnEnb = 1
        self.slogan = cstr.createLabel('Looks Like Art\nFeels Like Home\n', '35%', 'auto', "slogan")
        gifContainer = cstr.createContainer('40%', '100%', "homegif", "vertical")
        centralContainer.append([self.menuBtn, self.slogan, gifContainer])
        self.homeContainer.append([self.homeBtnCOnt, centralContainer, self.connectBtnCOnt])

        # --- --- --- --- --- Menu Container Main --- --- --- --- --- #
        self.menuContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralmContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")
        self.modesBtn = cstr.createButton("Modes", '100px', '85%', "innermenu_button", self.modesBtn_clicked)
        self.ligthsBtn = cstr.createButton("Ligths", '100px', '85%', "innermenu_button", self.lightsBtn_clicked)
        self.tempBtn = cstr.createButton("Temperature", '100px', '85%', "innermenu_button", self.tempBtn_clicked)
        self.securityBtn = cstr.createButton("Security", '100px', '85%', "innermenu_button", self.securityBtn_clicked)
        centralmContainer.append([self.menuBtn, self.modesBtn, self.ligthsBtn, self.tempBtn, self.securityBtn])
        self.menuContainer.append([self.homeBtnCOnt, centralmContainer, self.connectBtnCOnt])


        # --- --- --- --- --- Menu Container Small --- --- --- --- --- #
        centralmVContainer= cstr.createContainer('80%', '10%', "menu_Container", "horizontal")
        centralmVContainer.append([self.modesBtn, self.ligthsBtn, self.tempBtn, self.securityBtn])
        cstr.modifyStyle(centralmVContainer, {'postion': 'relative', 'left': '10%', 'overflow': 'hidden',
                                              'white-space': 'pre-wrap'})

        # --- --- --- --- --- Modes Container --- --- --- --- --- #
        self.modesContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralmoContainer= cstr.createContainer('90%', '40%', "menu_Container", "horizontal")

        centralmoContainer.append([self.menuBtn])
        self.modesContainer.append([self.homeBtnCOnt, centralmoContainer, centralmVContainer,
                                    self.connectBtnCOnt])

        # --- --- --- --- --- Lights Container --- --- --- --- --- #
        self.lightsContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centrallContainer= cstr.createContainer('90%', '40%', "menu_Container", "horizontal")

        lightGraphContainer = cstr.createContainer('50%', '80%', "menu_Container", "horizontal")
        cstr.modifyStyle(lightGraphContainer, {'top':'0%', 'left': '0%',
                                              'text-align': 'left'})

        self.light1M = cstr.createDropDown('auto', 'auto', ("On", "Off"), "gp_button")
        cstr.modifyStyle(self.light1M, {'top':'0%', 'left': '0%',
                                        'text-align': 'left'})
        self.light1M.onchange.connect(self.light1ModeChange)

        self.light1 = cstr.RingBuffer(LIGHT_KEEP_VALS, 0)
        light1Container = cstr.createContainer('40%', 'auto', "menu_Container", "vertical")
        self.light1Curr = cstr.createLabel("Current: ", 'auto', 'auto', "gp_label")
        cstr.modifyStyle(self.light1Curr, {'color': 'aliceblue', 'white-space': 'pre-wrap'})
        self.light1SetP = cstr.createLabel("Desired: ", 'auto', 'auto', "gp_label")
        cstr.modifyStyle(self.light1SetP, {'color': 'aliceblue', 'white-space': 'pre-wrap'})
        self.light1Slider = cstr.SvgSlider(10, 0, 140, 1, 100, 10)
        self.light1Slider.onchange.connect(self.on_slider0_changed)

        self.light1S = cstr.createDropDown('auto', 'auto', ("On", "Off"), "gp_button")
        cstr.modifyStyle(self.light1S, {'top':'0%', 'left': '0%',
                                        'text-align': 'left'})
        self.light1S.onchange.connect(self.light1SChange)


        light1Container.append([self.light1M, self.light1Slider, self.light1Curr, self.light1SetP, self.light1S])
        cstr.modifyStyle(light1Container, {'top':'15%', 'left': '2%'})

        self.lightGraph = cstr.PyGal(width="100%", height="100%")
        self.lightGraph.create_graph("Light", LIGHT_GRAPH_STYLE)
        self.lightGraph.populate("", self.light1.get())
        self.lightGraph.render()

        lightGraphContainer.append([self.lightGraph])
        centrallContainer.append([self.menuBtn, lightGraphContainer, light1Container])

        self.lightsContainer.append([self.homeBtnCOnt, centrallContainer, centralmVContainer,
                                     self.connectBtnCOnt])

        # --- --- --- --- --- Temperature Container --- --- --- --- --- #
        self.tempContainer = cstr.createContainer('100%', '100%', "fadein", "vertical")
        centraltContainer = cstr.createContainer('90%', '40%', "menu_Container", "horizontal")

        tempGraphContainer = cstr.createContainer('50%', '80%', "menu_Container", "horizontal")
        cstr.modifyStyle(tempGraphContainer, {'top':'0%', 'left': '0%',
                                              'text-align': 'left'})

        self.temp1 = cstr.RingBuffer(ADC_KEEP_VALS, 0)
        temp1Container = cstr.createContainer('40%', 'auto', "menu_Container", "vertical")
        self.temp1Curr = cstr.createLabel("Current: ", 'auto', 'auto', "gp_label")
        cstr.modifyStyle(self.temp1Curr, {'color': 'aliceblue', 'white-space': 'pre-wrap'})
        self.temp1SetP = cstr.createLabel("Desired: ", 'auto', 'auto', "gp_label")
        cstr.modifyStyle(self.temp1SetP, {'color': 'aliceblue', 'white-space': 'pre-wrap'})
        self.temp1Slider = cstr.SvgSlider(10, 0, 50, 1, 100, 10)
        self.temp1Slider.onchange.connect(self.on_slider1_changed)
        temp1Container.append([self.temp1Slider, self.temp1Curr, self.temp1SetP])
        cstr.modifyStyle(temp1Container, {'top':'15%', 'left': '2%'})

        self.temp2 = cstr.RingBuffer(ADC_KEEP_VALS, 0)
        temp2Container = cstr.createContainer('40%', 'auto', "menu_Container", "vertical")
        self.temp2Curr = cstr.createLabel("Current: ", 'auto', 'auto', "gp_label")
        cstr.modifyStyle(self.temp2Curr, {'color': 'bisque', 'white-space': 'pre-wrap'})
        self.temp2SetP = cstr.createLabel("Desired: ", 'auto', 'auto', "gp_label")
        cstr.modifyStyle(self.temp2SetP, {'color': 'aliceblue', 'white-space': 'pre-wrap'})
        self.temp2Slider = cstr.SvgSlider(10, 0, 50, 1, 100, 10)
        self.temp2Slider.onchange.connect(self.on_slider2_changed)
        temp2Container.append([self.temp2Slider, self.temp2Curr, self.temp2SetP])
        cstr.modifyStyle(temp2Container, {'top':'20%', 'left': '2%'})

        self.tempGraph = cstr.PyGal(width="100%", height="100%")
        self.tempGraph.create_graph("Temperature", TEMP_GRAPH_STYLE)
        self.tempGraph.populate("", self.temp1.get())
        self.tempGraph.populate("", self.temp2.get())
        self.tempGraph.render()

        tempGraphContainer.append([self.tempGraph])
        centraltContainer.append([self.menuBtn, tempGraphContainer, temp1Container, temp2Container])
        self.tempContainer.append([self.homeBtnCOnt, centraltContainer, centralmVContainer,
                                   self.connectBtnCOnt])

        # --- --- --- --- --- Security Container --- --- --- --- --- #
        self.secContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralsContainer= cstr.createContainer('90%', '40%', "menu_Container", "horizontal")

        centralsContainer.append([self.menuBtn])
        self.secContainer.append([self.homeBtnCOnt, centralsContainer, centralmVContainer,
                                 self.connectBtnCOnt])


        # --- --- --- --- --- Groups --- --- --- --- --- #

        self.groupActive = [self.homeBtn ,self.connectBtn ,
                            self.connectStatus, self.menuBtn,
                            self.light1Curr, self.light1SetP, self.light1S,
                            self.temp1Curr, self.temp2Curr,
                            self.temp1SetP, self.temp2SetP,
                            self.modesBtn, self.ligthsBtn,
                            self.tempBtn, self.securityBtn,
                            self.slogan]

        self.groupContainers = [self.homeContainer, self.lightsContainer,
                                self.tempContainer,  self.menuContainer,
                                self.modesContainer, self.secContainer]

        # --- --- --- --- --- Initialization --- --- --- --- --- #

        # -- Enable auto lights mode for light 1
        self.modes.modesEnableLights(0, False)

        cstr.updateColorScheme("color", "#A6775B", self.groupActive)
        cstr.updateColorScheme("background-color", "white", self.groupContainers)
        self.measure()


        return self.homeContainer

    # listener functions
    def onload(self, emitter):
        logger.info("Application loaded succesfuly.")

    def onerror(self, emitter, message, source, line, col):
        logger.error("%s\n%s\n%s\n%s"%(message, source, line, col))
        self.execute_javascript('document.onkeydo')

    def menuBtn_clicked(self, widget):
        if self.menuBtnEnb == 1:
            self.menuBtn.set_text("X")
            self.set_root_widget(self.menuContainer)
            self.menuBtnEnb = 0
        elif self.menuBtnEnb == 0:
            self.menuBtn.set_text("O")
            self.set_root_widget(self.homeContainer)
            self.menuBtnEnb = 1

    def homeBtn_clicked(self, widget):
        self.menuBtn.set_text("O")
        self.set_root_widget(self.homeContainer)
        self.menuBtnEnb = 1

    def connectBtn_clicked(self, widget):
        if not self.serConnected:
            if self.ser.connect():
                if self.ser.isConnected():
                    self.serConnected = True
                    cstr.updateColorScheme("color", "#A6775B", self.groupActive)
                    cstr.updateColorScheme("background-color", "white", self.groupContainers)
                    cstr.updateBck("fadein", "fadeinConnected", self.groupContainers)
                    self.connectStatus.set_text("Device Authenticated")
                    logger.info("Serial communication established.")
                    self.connectBtn.set_text("Disconnect")

            else:
                self.serConnected = False
                self.connectStatus.set_text("Failed to Authenticate the Device")
        else:
            if self.ser.disconnect():
                self.connectStatus.set_text("")
                self.serConnected = False
                cstr.updateColorScheme("color", "#A6775B", self.groupActive)
                cstr.updateColorScheme("background-color", "white", self.groupContainers)
                cstr.updateBck("fadeinConnected", "fadein", self.groupContainers)
                self.connectBtn.set_text("Connect")

        self.execute_javascript("location.reload(true);")

    def modesBtn_clicked(self, widget):
        self.set_root_widget(self.modesContainer)

    def lightsBtn_clicked(self, widget):
        self.set_root_widget(self.lightsContainer)

    def tempBtn_clicked(self, widget):
        self.set_root_widget(self.tempContainer)

    def securityBtn_clicked(self, widget):
        self.set_root_widget(self.secContainer)

    def on_close(self):
        self.stop_measure = True

        if self.ser.isConnected():
            self.ser.disconnect()

        super(smARTHome, self).on_close()

    def measure(self):
        if self.ser.isConnected():
            temp1, temp2, light1, humidity, empty = self.ser.readAdcData()

            temp1 = utilsTempConverter(temp1)
            temp2 = utilsTempConverter(temp2)

            self.temp1.append(temp1)
            self.temp2.append(temp2)
            self.light1.append(light1)

            self.temp1Curr.set_text("Current: " + str(temp1))
            self.temp2Curr.set_text("Current: " + str(temp2))
            self.light1Curr.set_text("Current: " + str(light1))
            self.tempGraph.populate(str(temp1), self.temp1.get())
            self.tempGraph.populate(str(temp2), self.temp2.get())
            self.tempGraph.render()
            self.lightGraph.populate(str(light1), self.light1.get())
            self.lightGraph.render()

        if not self.stop_measure:
            Timer(ADC_READ_INTERVAL, self.measure).start()

    def light1SChange(self, widget, value):
        logger.debug("Disable light1 smart mode")
        self.modes.modesEnableLights(0, False)
        if value == "Off":
            logger.debug("Disable light1")
            self.ser.lightEnable(0, 0)
        elif value == "On":
            logger.debug("Enable light1")
            self.ser.lightEnable(0, 1)

    def light1ModeChange(self, widget, value):
        if value == "Off":
            logger.debug("Disable light1 smart mode")
            self.modes.modesEnableLights(0, False)
        elif value == "On":
            logger.debug("Enable light1 smart mode")
            self.modes.modesEnableLights(0, True)

    def on_slider0_changed(self, emitter, value):
        self.lightSetPoint = int(value)
        self.light1SetP.set_text("Desired: " + str(int(value)))

    def on_slider1_changed(self, emitter, value):
        self.temp1SetP.set_text("Desired: " + str(int(value)))

    def on_slider2_changed(self, emitter, value):
        self.temp2SetP.set_text("Desired: " + str(int(value)))



if __name__ == "__main__":
# starts the webserver
    start(smARTHome, debug=True, address='0.0.0.0',
                     port=8081, start_browser=True,
                     multiple_instance=False,
                     username='Iliya', password='admin')
