from mido import MidiFile
from mido import Message
import time, os, sys, requests, random
import threading
import numpy as np
import pygame as pg


class MidiMessage:
    def __init__(self, msg_str):
        self.msg = msg_str.split()  #split string into a list
        # self.msg = msg_str

    def channel(self):
        """ Get channel attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[1]
            idx = target.find('=')
            # print(target[idx + 1:])
            return int(target[idx + 1:])

    def note(self):
        """ Get note attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[2]
            idx = target.find('=')
            # print(target[idx + 1:])
            return int(target[idx + 1:])

    def velocity(self):
        """ Get velocity attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[3]
            idx = target.find('=')
            # print(target[idx + 1:])
            return int(target[idx + 1:])

    def time(self):
        """ Get time attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[4]
            idx = target.find('=')
            # print(target[idx + 1:])
            return float(target[idx + 1:])


def play(music_file):
    # pick a midi or MP3 music file you have in the working folder
    # or give full pathname
    #music_file = "Drumtrack.mp3"
    '''
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get right sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    '''
    pg.mixer.init()

    # optional volume 0 to 1.0
    pg.mixer.music.set_volume(0.8)

    # play music
    print("Playing...")
    clock = pg.time.Clock()
    pg.mixer.music.load(music_file)
    pg.mixer.music.play()
    # check if playback has finished
    while pg.mixer.music.get_busy():
        clock.tick(30)


def job_of_play_music(music_file):
    """ create a thread to play music """

    def call():
        play(music_file)

    p = threading.Thread(target=call)
    p.setDaemon(True)
    p.start()


def job_of_music_feature(music_file):
    """ fetch message from music file and get music features """
    midi_file = MidiFile(music_file)
    for msg in midi_file:
        # print(dir(msg))
        # exit()
        time.sleep(msg.time)
        if not msg.is_meta:
            # print(msg)
            str_msg = str(msg)
            mid = MidiMessage(str_msg)
            if mid.channel() == 0:
                print(str_msg)
                print('note:', mid.note())
                print('velocity: ', mid.velocity())


if __name__ == "__main__":
    music_file = "魔法公主主題曲-VW.mid"
    """ play music """
    job_of_play_music(music_file)
    """ push feature data """
    job_of_music_feature(music_file)
