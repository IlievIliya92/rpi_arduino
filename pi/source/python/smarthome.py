#!/usr/bin/python3

import sqlite3
import os
import time
import constructors as cstr

from remi import start, App
from serialcom import SerialCom
from threading import Timer

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
        self.ser = SerialCom()
        self.serConnected = False

        # --- --- --- --- --- --- --- --- --- --- --- #


        # --- --- --- --- BODY --- --- --- --- --- ---#
        self.page.children['head'].set_icon_file("/resources:favicon.ico")
        # --- --- --- --- --- --- --- --- --- --- --- #

        self.homeBtn = cstr.createButton("smART\nHOME", 'auto', 'auto',
                                         "home_button", self.homeBtn_clicked)

        self.connectBtn = cstr.createButton("Connect", 'auto', 'auto',
                                            "home_button", self.connectBtn_clicked)
        cstr.modifyStyle(self.connectBtn, {'top':'20%'})

        # --- --- --- --- --- Home Container --- --- --- --- --- #
        self.homeContainer = cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralContainer = cstr.createContainer('90%', '50%', "menu_Container", "horizontal")
        self.menuBtn =cstr.createButton('O', '5%', 'auto', "menu_button", self.menuBtn_clicked)
        self.menuBtnEnb = 1
        slogan = cstr.createLabel('Looks Like Art\nFeels Like Home\n', '35%', 'auto', "slogan")
        gifContainer = cstr.createContainer('30%', '100%', "homegif", "vertical")
        centralContainer.append([self.menuBtn, slogan, gifContainer])
        self.homeContainer.append([self.homeBtn, centralContainer, self.connectBtn])

        # --- --- --- --- --- Menu Container --- --- --- --- --- #
        self.menuContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralmContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")
        modesBtn = cstr.createButton("Modes", '100px', '85%', "innermenu_button", self.modesBtn_clicked)
        ligthsBtn = cstr.createButton("Ligths", '100px', '85%', "innermenu_button", self.lightsBtn_clicked)
        tempBtn = cstr.createButton("Temperature", '100px', '85%', "innermenu_button", self.tempBtn_clicked)
        securityBtn = cstr.createButton("Security", '100px', '85%', "innermenu_button", self.securityBtn_clicked)
        centralmContainer.append([self.menuBtn, modesBtn, ligthsBtn, tempBtn, securityBtn])
        self.menuContainer.append([self.homeBtn, centralmContainer, self.connectBtn])

        # --- --- --- --- --- Modes Container --- --- --- --- --- #
        self.modesContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralmoContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centralmoContainer.append([self.menuBtn])
        self.modesContainer.append([self.homeBtn, centralmoContainer, self.connectBtn])

        # --- --- --- --- --- Lights Container --- --- --- --- --- #
        self.lightsContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centrallContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centrallContainer.append([self.menuBtn])
        self.lightsContainer.append([self.homeBtn, centralmoContainer, self.connectBtn])

        # --- --- --- --- --- Lights Container --- --- --- --- --- #
        self.tempContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centraltContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centraltContainer.append([self.menuBtn])
        self.tempContainer.append([self.homeBtn, centralmoContainer, self.connectBtn])

        # --- --- --- --- --- Security Container --- --- --- --- --- #
        self.secContainer =cstr.createContainer('100%', '100%', "fadein", "vertical")
        centralsContainer= cstr.createContainer('90%', '50%', "menu_Container", "horizontal")

        centralsContainer.append([self.menuBtn])
        self.secContainer.append([self.homeBtn, centralmoContainer, self.connectBtn])


        return self.homeContainer

    # listener functions
    def onload(self, emitter):
        logger.info("Application loaded succesfuly.")

    def onerror(self, emitter, message, source, line, col):
        logger.error("%s\n%s\n%s\n%s"%(message, source, line, col))
        self.execute_javascript('document.onkeydo')

    def menuBtn_clicked(self, widget):
        if self.menuBtnEnb == 1:
            self.set_root_widget(self.menuContainer)
            self.menuBtn.set_text("X")
            self.menuBtnEnb = 0
        elif self.menuBtnEnb == 0:
            self.set_root_widget(self.homeContainer)
            self.menuBtn.set_text("O")
            self.menuBtnEnb = 1

    def homeBtn_clicked(self, widget):
        self.set_root_widget(self.homeContainer)

    def connectBtn_clicked(self, widget):
        if not self.serConnected:
            if self.ser.connect():
                self.serConnected = True
                logger.info("Serial communication established.")
                self.connectBtn.set_text("Disconnect")
        else:
            if self.ser.disconnect():
                logger.info("Failed to connect to the serial device.")
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
        super(smARTHome, self).on_close()

# starts the webserver
if __name__ == "__main__":
# starts the webserver
#    import ssl
    start(smARTHome, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True, username='Iliya', password='admin')
