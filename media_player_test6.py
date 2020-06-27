import vlc
from time import sleep
from datetime import datetime, timedelta
import random

###########################################Stuff for Display ##################################################
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
jukebox_display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Load default font.
font = ImageFont.load_default()

# Clear display.
jukebox_display.fill(0)
jukebox_display.show()

###########################################Stuff for the card reader ##################################################
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

instance = vlc.Instance('--aout=alsa')

import ast


# playlist_list = {
#     "Song1": ["1.mp3", "2.mp3", "3.mp3", "4.mp3", "5.mp3"],
#     "Song2": ["5.mp3", "4.mp3", "3.mp3", "2.mp3", "1.mp3"],
# }

############################################Stuff for the buttons##################################################
from gpiozero import Button
import RPi.GPIO as GPIO
skip_button = Button(17)
play_button = Button(4, hold_time=1)
shuffle_button = Button(27)

####################################################Flags##########################################################
shuffle_flag = 0
card_currently_read = ""

####################################################The main programme#############################################
def welcome_message():
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (jukebox_display.width, jukebox_display.height))

    # Get drawing object to draw on image.
    jukebox_draw = ImageDraw.Draw(image)

    jukebox_draw.text((50, 0), "Jukebox", font=font, fill=255)
    jukebox_draw.text((0, 20), "Please wait, ", font=font, fill=255)
    jukebox_draw.text((0, 30), "loading data", font=font, fill=255)
    jukebox_draw.text((0, 45), "This may take a while", font=font, fill=255)
    jukebox_display.image(image)
    jukebox_display.show()

    sleep(1)


def read_card():
    # Clear display.
    jukebox_display.fill(0)
    jukebox_display.show()
    image = Image.new('1', (jukebox_display.width, jukebox_display.height))

    # Get drawing object to draw on image.
    jukebox_draw = ImageDraw.Draw(image)

    # Display image
    jukebox_draw.text((45, 0), "Jukebox", font=font, fill=255)
    jukebox_draw.text((20, 30), "Present a card", font=font, fill=255)
    jukebox_display.image(image)
    jukebox_display.show()

    try:
        print("Present a card")
        id, text = reader.read()
        print(id)
        print(text)
    finally:
        print("Card has been read")

    text = str(text).strip()
    return text


def card_read_to_return_file_list(text):
    with open(f'/song_lists/{text}.txt') as f:
        playlist_list = ast.literal_eval(f.read())
        return_list = []
        for item in playlist_list:
            return_list.append(item)
        return return_list


def display_info(media_artist_name, media_album_name, media_song_name, media_duration):
    # Clear display.
    jukebox_display.fill(0)
    jukebox_display.show()
    image = Image.new('1', (jukebox_display.width, jukebox_display.height))

    # Get drawing object to draw on image.
    jukebox_draw = ImageDraw.Draw(image)

    # Display image
    print("Displaying information Start")
    jukebox_draw.text((0, 0), f'Artist = {media_artist_name}', font=font, fill=255)
    jukebox_draw.text((0, 15), f'Album = {media_album_name}', font=font, fill=255)
    jukebox_draw.text((0, 30), f'Title = {media_song_name}', font=font, fill=255)
    jukebox_draw.text((0, 45), f'Duration = {media_duration}', font=font, fill=255)

    # Display image.
    jukebox_display.image(image)
    jukebox_display.show()
    print("Displaying information End")


def change_shuffle_flag():
    global shuffle_flag
    shuffle_flag = 1


def main():

    global shuffle_flag
    global card_currently_read

    while True:
        welcome_message()
        #Attempts to stop if anything is playing
        try:
            media.stop()
        except:
            print("Nothing playing right now")

        ##Checks if the shuffle button has been pressed first
        if shuffle_flag == 0:
            # Reads the RFID card and returns a playlist name
            playlist_name = read_card()
            # Each playlist name corresponds to a dictionary entry with all the file paths in order
            song_file_path_list = card_read_to_return_file_list(playlist_name)
            print(song_file_path_list)
        else:
            song_file_path_list = random.sample(song_file_path_list, len(song_file_path_list))
            print(song_file_path_list)
            shuffle_flag = 0

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
            sleep(1) #This is required otherwise the item doesn't start playing before the loop breaks
            media_song_name_previous = "Default"

            #While items are still playing, paused or still opening next track it waits
            while str(media.get_state()) in {"State.Playing", "State.Paused", "State.Opening"}:

                # Get information about the track playing
                media_song_name = media.get_media_player().get_media().get_meta(vlc.Meta.Title) or "Unknown Song"

                if media_song_name != media_song_name_previous:
                    media_state = media.get_state()
                    media_file_path = media.get_media_player().get_media().get_mrl()
                    media_duration = media.get_media_player().get_media().get_duration()
                    # media_parse = media.get_media_player().get_media().parse()
                    # media_track_info = media.get_media_player().get_media().get_tracks_info()
                    media_artist_name = media.get_media_player().get_media().get_meta(
                        vlc.Meta.Artist) or "Unknown Artist"
                    media_album_name = media.get_media_player().get_media().get_meta(vlc.Meta.Album) or "Unknown Album"
                    media_duration = timedelta(milliseconds=media_duration)

                    print(f'State = {media_state}')
                    print(f'MRL = {media_file_path}')
                    print(f'Duration = {media_duration}')
                    print(f'Artist = {media_artist_name}')
                    print(f'Album = {media_album_name}')
                    print(f'Title = {media_song_name}')

                    media_song_name_previous = media_song_name
                    display_info(media_artist_name, media_album_name, media_song_name, media_duration)

                sleep(0.1)  # any higher and it seems to miss button presses

                play_button.when_pressed = media.pause
                play_button.when_held = media.stop
                skip_button.when_pressed = media.next
                shuffle_button.when_pressed = change_shuffle_flag
                shuffle_button.when_released = media.stop

            print(media.get_state())

        except Exception as e:
            print(e)

    GPIO.cleanup()


if __name__ == '__main__':
    main()
