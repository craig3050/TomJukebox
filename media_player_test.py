import vlc
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def play_music():
    id = ""
    text = ""
    instance = vlc.Instance('--aout=alsa')
    try:
            id, text = reader.read()
            print(id)
            print(text)
    finally:
            GPIO.cleanup()

    text = str(text).strip()
    print(f'the card information is {text}')
    if text == 'Song1':
        print("playing song 1")
        media = instance.media_player_new('1.mp3')
        media.play()
    # if text == 'Song1':
    #     print("playing song 1")
    #     p = instance.media_player_new()
    #     m = instance.media_new('1.mp3')
    #     p.set_media(m)
    #     p.play()
    elif text == 'Song2':
        print("playing song 2")
        media = instance.media_player_new('2.mp3')
        media.play()
        # print("Playing song 2")
        # p = instance.media_player_new()
        # m = instance.media_new('2.mp3')
        # p.set_media(m)
        # p.play()
    else:
        print("Didn't work I see")
        print(text)

def main():
    while True:
        input("Press Enter to read a card to play music")
        play_music()






if __name__ == '__main__':
    main()