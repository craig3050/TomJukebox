import vlc
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from gpiozero import Button
from datetime import datetime, timedelta
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

###########################################Stuff for Display ##################################################

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

###########################################Stuff for the card reader ##################################################
reader = SimpleMFRC522()

instance = vlc.Instance('--aout=alsa')


playlist_list = {
    "Song1": ["1.mp3", "2.mp3"],
    "Song2": ["2.mp3", "1.mp3"],
}

############################################Stuff for the buttons##################################################


button = Button(4)

####################################################The main programme#############################################

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
                media_state = media.get_state()
                media_file_path = media.get_media_player().get_media().get_mrl()
                media_duration = media.get_media_player().get_media().get_duration()
                media_parse = media.get_media_player().get_media().parse()
                media_track_info = media.get_media_player().get_media().get_tracks_info()
                media_artist_name = media.get_media_player().get_media().get_meta(vlc.Meta.Artist) or "Unknown Artist"
                media_album_name = media.get_media_player().get_media().get_meta(vlc.Meta.Album) or "Unknown Album"
                media_song_name = media.get_media_player().get_media().get_meta(vlc.Meta.Title) or "Unknown Song"

                media_duration = timedelta(milliseconds=media_duration)

                print(f'State = {media_state}')
                print(f'MRL = {media_file_path}')
                print(f'Duration = {media_duration}')
                print(f'Artist = {media_artist_name}')
                print(f'Album = {media_album_name}')
                print(f'Title = {media_song_name}')

                draw.text((x, top), f'Artist = {media_artist_name}', font=font, fill=255)
                draw.text((x, top + 8), f'Album = {media_album_name}', font=font, fill=255)
                draw.text((x, top + 16), f'Title = {media_song_name}', font=font, fill=255)
                draw.text((x, top + 25), f'Duration = {media_duration}', font=font, fill=255)

                # Display image.
                disp.image(image)
                disp.display()

                sleep(0.1)  # any higher and it seems to miss button presses

                #This is where the function buttons are located (number TBC)
                button.when_pressed = media.next

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
