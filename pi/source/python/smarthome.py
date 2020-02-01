#!/usr/bin/python3

import sqlite3
import os
import time
import constructors as cstr

from remi import start, App
from serialcom import SerialCom
from threading import Timer

from constants import *

#!/usr/bin/python3
from logger import *

# --- Smart Home app
class smARTHome(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'remi/res')
        super(smARTHome, self).__init__(*args, static_file_path={'resources':res_path})

    def idle(self):
        pass

    def main(self):
        # --- --- --- --- State  --- --- --- --- --- #
        self.ser = SerialCom(ARD_DEVICE_ID)
        self.serConnected = False
        self.stop_measure = False

        # --- --- --- --- --- --- --- --- --- --- --- #


        # --- --- --- --- BODY --- --- --- --- --- ---#
        self.page.children['head'].set_icon_file("/resources:favicon.ico")
        # --- --- --- --- --- --- --- --- --- --- --- #

        self.homeBtn = cstr.createButton("smART\nHOME", 'auto', 'auto',
                                         "gp_button", self.homeBtn_clicked)

        self.connectBtn = cstr.createButton("Connect", 'auto', 'auto',
                                            "gp_button", self.connectBtn_clicked)
        cstr.modifyStyle(self.connectBtn, {'top':'20%'})
        self.connectStatus = cstr.createLabel("", 'auto', 'auto', "gp_button")
        cstr.modifyStyle(self.connectStatus, {'top':'22%'})

        # --- --- --- --- --- Home Container --- --- --- --- --- #
        self.homeContainer = cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralContainer = cstr.createContainer('90%', '50%', "menu_Container", "horizontal")
        self.menuBtn =cstr.createButton('O', '5%', 'auto', "menu_button", self.menuBtn_clicked)
        self.menuBtnEnb = 1
        slogan = cstr.createLabel('Looks Like Art\nFeels Like Home\n', '35%', 'auto', "slogan")
        gifContainer = cstr.createContainer('30%', '100%', "homegif", "vertical")
        centralContainer.append([self.menuBtn, slogan, gifContainer])
        self.homeContainer.append([self.homeBtn, centralContainer, self.connectBtn, self.connectStatus])

        # --- --- --- --- --- Menu Container --- --- --- --- --- #
        self.menuContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralmContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")
        modesBtn = cstr.createButton("Modes", '100px', '85%', "innermenu_button", self.modesBtn_clicked)
        ligthsBtn = cstr.createButton("Ligths", '100px', '85%', "innermenu_button", self.lightsBtn_clicked)
        tempBtn = cstr.createButton("Temperature", '100px', '85%', "innermenu_button", self.tempBtn_clicked)
        securityBtn = cstr.createButton("Security", '100px', '85%', "innermenu_button", self.securityBtn_clicked)
        centralmContainer.append([self.menuBtn, modesBtn, ligthsBtn, tempBtn, securityBtn])
        self.menuContainer.append([self.homeBtn, centralmContainer, self.connectBtn, self.connectStatus])

        # --- --- --- --- --- Modes Container --- --- --- --- --- #
        self.modesContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralmoContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centralmoContainer.append([self.menuBtn])
        self.modesContainer.append([self.homeBtn, centralmoContainer, self.connectBtn, self.connectStatus])

        # --- --- --- --- --- Lights Container --- --- --- --- --- #
        self.lightsContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centrallContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centrallContainer.append([self.menuBtn])
        self.lightsContainer.append([self.homeBtn, centralmoContainer, self.connectBtn, self.connectStatus])

        # --- --- --- --- --- Temperature Container --- --- --- --- --- #
        self.tempContainer = cstr.createContainer('100%', '100%', "fadein", "vertical")
        centraltContainer = cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        tempGraphContainer = cstr.createContainer('50%', '80%', "menu_Container", "horizontal")
        cstr.modifyStyle(tempGraphContainer, {'top':'0%', 'left': '5%',
                                              'text-align': 'left'})

        self.tempGraph = cstr.PyGal(width="100%", height="100%")
        self.temp1 = cstr.RingBuffer(ADC_KEEP_VALS, 0)
        self.temp1Curr = cstr.createLabel("", 'auto', 'auto', "gp_button")
        cstr.modifyStyle(self.temp1Curr, {'color': 'aliceblue', 'left': '5%', 'top': '5%'})


        self.temp1SetP = cstr.createLabel("", 'auto', 'auto', "gp_button")
        cstr.modifyStyle(self.temp1SetP, {'color': 'aliceblue', 'left': '5%', 'top': '5%'})
        self.temp1Slider = cstr.SvgSlider(10, -10, 18, 1, 100, 10)
        self.temp1Slider.onchange.connect(self.on_slider1_changed)
        self.temp1SetP.append(self.temp1Slider)

        self.temp2 = cstr.RingBuffer(ADC_KEEP_VALS, 0)
        self.tempGraph.create_graph("Temperature")
        self.temp2Curr = cstr.createLabel("", 'auto', 'auto', "gp_button")
        cstr.modifyStyle(self.temp2Curr, {'color': 'bisque', 'left': '10%', 'top': '5%'})


        self.tempGraph.populate("", self.temp1.get())
        self.tempGraph.populate("", self.temp2.get())
        self.tempGraph.render()

        tempGraphContainer.append([self.tempGraph])
        centraltContainer.append([self.menuBtn, tempGraphContainer,  self.temp1SetP, self.temp1Curr, self.temp2Curr])
        self.tempContainer.append([self.homeBtn, centraltContainer, self.connectBtn, self.connectStatus])

        # --- --- --- --- --- Security Container --- --- --- --- --- #
        self.secContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralsContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centralsContainer.append([self.menuBtn])
        self.secContainer.append([self.homeBtn, centralsContainer, self.connectBtn, self.connectStatus])

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
            #print("measure")
            temp1, temp2, light, humidity, empty = self.ser.readAdcData()
            self.temp1.append(temp1)
            self.temp2.append(temp2)
            self.temp1Curr.set_text("\tCurrent: " + str(temp1))
            self.temp2Curr.set_text("\tCurrent: " + str(temp2))
            self.tempGraph.populate(str(temp1), self.temp1.get())
            self.tempGraph.populate(str(temp2), self.temp2.get())
            self.tempGraph.render()

        if not self.stop_measure:
            Timer(ADC_READ_INTERVAL, self.measure).start()


    def on_slider1_changed(self, emitter, value):
        self.temp1SetP.set_text("Desired: " + str(int(value)))



# starts the webserver
if __name__ == "__main__":
# starts the webserver
#    import ssl
    start(smARTHome, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True, username='Iliya', password='admin')
