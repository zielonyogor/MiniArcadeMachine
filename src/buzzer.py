# melody: c5 e5 f5

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

def setup():
    global buzzer
    buzzer = TonalBuzzer(13)

def play_happy_melody():
    buzzer.play(Tone("C5"))
    sleep(0.1)
    buzzer.play(Tone("E5"))
    sleep(0.1)
    buzzer.play(Tone("F5"))
    sleep(0.5)
    buzzer.stop()
    return

def play_select_melody():
    buzzer.play(Tone("F4"))
    sleep(0.2)
    buzzer.stop()
    return

def play_sad_melody():
    buzzer.play(Tone("A3"))
    sleep(0.3)
    buzzer.play(Tone("C3"))
    sleep(0.3)
    buzzer.play(Tone("E3"))
    sleep(0.3)
    buzzer.stop()
    return

def play_up_melody():
    buzzer.play(Tone("C5"))
    sleep(0.1)
    buzzer.stop()
    return

def play_down_melody():
    buzzer.play(Tone("G4"))
    sleep(0.1)
    buzzer.stop()
    return

def play_left_melody():
    buzzer.play(Tone("A4"))
    sleep(0.1)
    buzzer.stop()
    return

def play_right_melody():
    buzzer.play(Tone("B4"))
    sleep(0.1)
    buzzer.stop()
    return