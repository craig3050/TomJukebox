import vlc
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from gpiozero import Button

reader = SimpleMFRC522()

instance = vlc.Instance('--aout=alsa')

file_list = {
    "Song1": "1.mp3",
    "Song2": "2.mp3",
}

button = Button(4)


def read_card():
    try:
        print("Present a card")
        id, text = reader.read()
        print(id)
        print(text)
    finally:
        GPIO.cleanup()

    text = str(text).strip()
    return text


def main():
    while True:

        try:
            media.stop()
        except:
            print("Nothing playing right now")

        song_name = read_card()
        song_file_path = file_list[song_name]

        try:
            media = instance.media_player_new(song_file_path)
            print("Playing Media")
            media.play()
            sleep(1)

        except:
            print("Not playing ball")
        # input("Press Enter to read a card to play music")
        button.when_pressed = media.stop
        #button.when_released = read_card
        while str(media.get_state()) == "State.Playing":
            print(media.get_state())
            sleep(1)


if __name__ == '__main__':
    main()
