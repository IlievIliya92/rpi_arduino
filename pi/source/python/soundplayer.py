#!/usr/bin/python3

from playsound import playsound
import vlc
from os import listdir
from os.path import isfile, join

from constants import *
from logger import *

def buttonClick(sound):
    try:
        if sound == 0:
            playsound(APPSOUNDS + 'ButtonClick.wav')
        elif sound == 1:
            playsound(APPSOUNDS + 'ButtonClick1.wav')
    except Exception as e:
        pass

class Player:
    def __init__(self, volume):
        try:
            self.volume = volume
            self.index = 0
            self.playlist = [f for f in listdir(AUDIODIR) if isfile(join(AUDIODIR, f))]
            self.player = vlc.MediaPlayer(AUDIODIR + self.playlist[self.index])
            self.songs = len(self.playlist)
            self.playing = False
        except Exception as e:
            pass


    def stop(self):
        self.player.stop()
        self.playing = False

    def play(self):
        self.player.stop()
        self.player.play()
        self.playing = True

    def next (self):
        self.stop()
        self.index += 1
        if self.index >= self.songs:
            self.index = 0
        self.player = vlc.MediaPlayer(AUDIODIR + self.playlist[self.index])
        self.play()

    def previous (self):
        self.stop()
        self.index -= 1
        if self.index < 0:
            self.index = len(self.playlist) - 1
        self.player = vlc.MediaPlayer(AUDIODIR + self.playlist[self.index])
        self.play()

    def getTitle(self):
        return self.playlist[self.index]

    def pause(self):
        self.player.pause()
        self.playing = False

    def setVol(self, value):
        self.player.audio_set_volume(int(value))

    def volUp(self):
        self.volume += 10
        self.player.audio_set_volume(self.volume)

    def volDown(self):
        self.volume -= 10
        self.player.audio_set_volume(self.volume)

    def isPlaying(self):
        return self.playing
