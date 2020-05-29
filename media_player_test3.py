import vlc
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from gpiozero import Button

reader = SimpleMFRC522()

instance = vlc.Instance('--aout=alsa')


playlist_list = {
    "Song1": ["1.mp3", "2.mp3"],
    "Song2": ["2.mp3", "1.mp3"],
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

        #Attempts to stop if anything is playing
        try:
            media.stop()
        except:
            print("Nothing playing right now")

        #Reads the RFID card and returns a playlist name
        playlist_name = read_card()

        #Each playlist name corresponds to a dictionary entry with all the file paths in order
        song_file_path_list = playlist_list[playlist_name]
        print(song_file_path_list)

        #This is the main playing function
        try:
            #Create a new playlist and add the songs from the list into it
            media_playlist = instance.media_list_new()
            for item in song_file_path_list:
                media_playlist.add_media(instance.media_new(item))
                print(f'Added {item}')

            #create new instance of the player & set the playlist
            media = instance.media_list_player_new()
            media.set_media_list(media_playlist)

            print("Playing Media")
            media.play()
            sleep(1)

            #While items are still playing it waits
            while str(media.get_state()) == "State.Playing":
                print(f'State = {media.get_state()}')
                sleep(0.5) #any higher and it seems to miss button presses
                print(f'MRL = {media.get_media_player().get_media().get_mrl()}')
                sleep(0.5)  # any higher and it seems to miss button presses
                # print(f'Meta = {media.get_media_player().get_media().get_meta()}')
                # sleep(0.5)  # any higher and it seems to miss button presses
                # print(f'Stats = {media.get_media_player().get_media().get_stats()}')
                # sleep(0.5)  # any higher and it seems to miss button presses
                print(f'Duration = {media.get_media_player().get_media().get_duration()}')
                sleep(0.5)  # any higher and it seems to miss button presses
                print(f'Tracks info = {media.get_media_player().get_media().get_tracks_info()}')
                sleep(0.5)  # any higher and it seems to miss button presses

                #This is where the function buttons are located (number TBC)
                button.when_pressed = media.next

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
