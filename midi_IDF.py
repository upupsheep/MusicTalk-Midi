from mido import MidiFile
from mido import Message
import time, os, sys, requests, random
import threading
import numpy as np
import pygame as pg
import DAN

# Uncomment the following part to use IoTTalk v1
# Note that DAN.py, csmapy.py need to be at the same directory
# """
ServerURL = 'http://garden.iottalk.tw'  #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None  #if None, Reg_addr = MAC address

DAN.profile['dm_name'] = 'Music'
DAN.profile['df_list'] = ['Note']
#DAN.profile['df_list'] = ['Sandy_I', 'Sandy_O']
DAN.profile['d_name'] = None  # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

# """


class ColorMapping:
    def __init__(self):
        """
        F#: (145, 25, 62) -> purple-red(?), 6
        G: (174, 0, 0) -> dark read, 7
        G#: (255, 0, 0) -> red, 8
        A: (255, 102, 0) -> orange-red, 9
        B-: (255, 239, 0) -> yello, 10
        B: (155, 255, 0) -> chartreuse, 11
        C: (40, 255, 0) -> lime, 0
        C#: (0, 255, 242) -> aqua, 1
        D: (0, 122, 255) -> sky blue, 2
        D#: (5, 0, 255) -> blue, 3
        E: (71, 0, 237) -> blue-indigo, 4
        F: (99, 0, 178) -> indigo, 5
        """
        note = []
        for i in range(128):
            note.append(i % 12)
        self.note_color_map = note.copy()
        self.color_map = [[40, 255, 0], [0, 255, 242], [0, 122, 255], [
            5, 0, 255
        ], [71, 0, 237], [99, 0, 178], [145, 25, 62], [174, 0, 0], [255, 0, 0],
                          [255, 102, 0], [255, 239, 0], [155, 255, 0]]

    def get_note_color(self, note):
        note_to_color = self.note_color_map[note]
        return self.color_map[note_to_color]


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
    note_color = ColorMapping()
    for msg in midi_file:
        # print(dir(msg))
        # exit()
        time.sleep(msg.time)
        if not msg.is_meta:
            # print(msg)
            str_msg = str(msg)
            mid = MidiMessage(str_msg)
            if mid.channel() == 0:
                # print(str_msg)
                # print('note:', mid.note())
                # print('velocity: ', mid.velocity())
                if mid.velocity() > 0:
                    color = note_color.get_note_color(mid.note())
                    print('color:', color)
                    # print(color[0])
                    # exit()
                    DAN.push('Note', color[0], color[1], color[2])


if __name__ == "__main__":
    music_file = "魔法公主主題曲-VW.mid"
    while (DAN.state != 'SET_DF_STATUS'):
        # wait for DAN ready
        time.sleep(0.1)
    """ play music """
    job_of_play_music(music_file)
    """ push feature data """
    job_of_music_feature(music_file)
