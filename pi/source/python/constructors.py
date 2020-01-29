#!/usr/bin/python3

import remi.gui as gui
from logger import *

# --- Constructors

def createButton(text, w, h, bclass, callback):
    btn = gui.Button(text, width=w, height=h)
    btn.add_class(bclass)
    btn.onclick.connect(callback)

    return btn

def createLabel(text, w, h, lclass):
    lbl = gui.Label(text, width=w, height=h)
    lbl.add_class(lclass)

    return lbl

def createContainer(w, h, cclass, orientation):
    if orientation == 'vertical':
        cont = gui.Container(width=w, height=h, layout_orientation=gui.Container.LAYOUT_VERTICAL)
    elif orientation == 'horizontal':
        cont = gui.Container(width=w, height=h, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
    cont.add_class(cclass)

    return cont

def createMenu(text, w, h, mclass, callback):
    menu = gui.MenuItem(text, width=w, height=h)
    menu.add_class(mclass)
    menu.onclick.connect(callback)

    return menu

def modifyStyle(widget, new_style):
    widget.style.update(new_style)

