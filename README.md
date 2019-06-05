# MusicTalk-Midi

**MusicTalk-Midi** is used to map midi file notes to color, and then use **IoTTalk** to push these color information to other output device.

### 1. Usage:

Make sure you install all the python dependency.

This project uses `mido`. To install `mido`, use the following command:

```b
pip install mido
```



To easily install all dependencies, run the following command:

```bash
sudo pip install -r requirements.txt
```



Also, make sure you have `DAN.py`, `csmapy.py` in the same directory with `midi_IDF.py`.

Change the `music_file` in the code ( in main ) to the midi file you want.

For example: (in main function)

```py
music_file = "BEYER003-VK.mid"
```



Finally, run the program using the following command:

```py
python midi_IDF.py
```

