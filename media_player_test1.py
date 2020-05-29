import vlc
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def read_card():
    id = ""
    text = ""
    try:
            id, text = reader.read()
            print(id)
            print(text)
    finally:
            GPIO.cleanup()

    text = str(text).strip()
    return text



def main():
    instance = vlc.Instance('--aout=alsa')
    while True:
        #input("Press Enter to read a card to play music")
        Album_name = read_card()


        if Album_name == 'Song1':
            print("playing song 1")
            media = instance.media_player_new('1.mp3')
            media.play()
            input("Press Enter to stop")
            media.stop()

        elif Album_name == 'Song2':
            print("playing song 2")
            media = instance.media_player_new('2.mp3')
            media.play()
            input("Press Enter to stop")
            media.stop()

        else:
            print("Didn't work I see")
            print(Album_name)




if __name__ == '__main__':
    main()