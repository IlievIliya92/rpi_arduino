#!/usr/bin/python3

import remi.gui as gui
from logger import *

import os
import time

import pygal
from pygal.style import Style

# --- Styles ---#
TEMP_GRAPH_STYLE = Style(colors=('#F0F8FF', '#FFE4C4'),
                         background = 'transparent',
                         plot_background = 'transparent',
                         legend_font_size = 20,
                         transition = '250ms ease-in',
                         foreground ='white',
                         font_family='Palatino',
                         label_font_size = 20)

LIGHT_GRAPH_STYLE = Style(colors=('#F0F8FF', '#F0F8FF'),
                         background = 'transparent',
                         plot_background = 'transparent',
                         legend_font_size = 20,
                         transition = '250ms ease-in',
                         foreground ='white',
                         font_family='Palatino',
                         label_font_size = 20)

# --- Constructors objects

class RingBuffer:
    def __init__(self, size, initval):
        self.data = []
        for i in range(size):
            self.data.append(initval)

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

    def getLast(self):
        return self.data[-1]


class PyGal(gui.Svg):
    def render(self):
        self.data = self.graph.render()
        self.remove_child("line")
        self.add_child("line", self.data)

    def create_graph(self, title, gstyle):
        self.graph  = pygal.Line(style=gstyle, show_legend=False)
        self.graph.title = title

    def populate(self, label, content):
        self.graph.add(label, content, fill=True)

class SvgDraggablePoint(gui.SvgCircle):
    def __init__(self, x, y, radius, *args, **kwargs):
        super(SvgDraggablePoint, self).__init__(x, y, radius, *args, **kwargs)
        self.radius = radius
        self.active = False

    def start_drag(self, emitter, x, y):
        self.active = True

    @gui.decorate_event
    def stop_drag(self, emitter, x, y):
        self.active = False
        return ()

    def on_drag(self, emitter, x, y):
        if self.active:
            self.set_position(x, self.attributes['cy'])

class SvgSlider(gui.Svg):
    def __init__(self, value, _min, _max, step, width, height, *args, **kwargs):
        super(SvgSlider, self).__init__(width, height, *args, **kwargs)
        self.min = _min
        self.max = _max
        self.step = step
        self.width = int(self.attributes['width'])
        self.height = int(self.attributes['height'])

        self.horizontal_line = gui.SvgRectangle(self.height/2,self.height/2-2, self.width-self.height, 2)
        self.horizontal_line.set_fill('gray')
        self.horizontal_line.set_stroke(1, 'lighgray')

        self.pointer = SvgDraggablePoint(self.width/2, self.height/2, self.height/2)
        self.pointer.set_fill('lightblue')
        self.pointer.set_stroke(1, 'lightgray')
        self.onmousedown.connect(self.pointer.start_drag)
        self.onmouseup.connect(self.pointer.stop_drag)
        self.onmouseleave.connect(self.pointer.stop_drag, 0, 0)
        self.onmousemove.connect(self.pointer.on_drag)

        self.append([self.horizontal_line, self.pointer])
        self.pointer.stop_drag.connect(self.onchange)

        self.set_value(value)

    @gui.decorate_event
    def onchange(self, emitter):
        self.set_value( (float(self.pointer.attributes['cx'])-self.pointer.radius)*(self.max-self.min)/(self.width-self.pointer.radius*2) + self.min )
        return (self.value, )

    def set_value(self, value):
        self.value = max(self.min, value)
        self.value = min(self.max, self.value)
        self.pointer.attributes['cx'] = str(int((self.value-self.min)*(self.width-self.pointer.radius*2)/(self.max-self.min))+self.pointer.radius)

    def get_value(self):
        return self.value


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

def createSpinBox(minv, maxv, w, h, sclass, callback):
    spin = gui.SpinBox(0, minv, maxv, width=w, height=h)
    spin.onchange.do(callback)
    spin.add_class(sclass)

    return spin

def createDropDown(w, h, items, dclass):
    dropdown = gui.DropDown.new_from_list(items, width=w, height=h)
    dropdown.add_class(dclass)

    return dropdown


def modifyStyle(widget, new_style):
    widget.style.update(new_style)

def updateColorScheme(tp, color, widgets):
    for widget in widgets:
        modifyStyle(widget, {tp : color})

def updateBck(bckclass, bckclassNew, containers):
    for cont in containers:
        cont.remove_class(bckclass)

    for cont in containers:
        cont.add_class(bckclassNew)
