from mido import MidiFile
from mido import Message
import time


class MidiMessage:
    def __init__(self, msg_str):
        self.msg = msg_str.split()  #split string into a list
        # self.msg = msg_str

    def channel(self):
        if (self.msg[0] != 'program_change'):
            target = self.msg[1]
            idx = target.find('=')
            print(target[idx + 1:])
            return int(target[idx + 1:])

    def note(self):
        if (self.msg[0] != 'program_change'):
            target = self.msg[2]
            idx = target.find('=')
            print(target[idx + 1:])
            return int(target[idx + 1:])

    def velocity(self):
        if (self.msg[0] != 'program_change'):
            target = self.msg[3]
            idx = target.find('=')
            print(target[idx + 1:])
            return int(target[idx + 1:])

    def time(self):
        if (self.msg[0] != 'program_change'):
            target = self.msg[4]
            idx = target.find('=')
            print(target[idx + 1:])
            return float(target[idx + 1:])


if __name__ == "__main__":
    midi_file = MidiFile('BEYER003-VK.mid')
    '''
    for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(str(msg))
    '''
    for msg in midi_file:
        time.sleep(msg.time)
        if not msg.is_meta:
            # print(dir(msg))
            str_msg = str(msg)
            mid = MidiMessage(str_msg)
            if mid.channel() == 0:
                print(str_msg)
                mid.note()

            # exit()
