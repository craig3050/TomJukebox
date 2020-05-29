import vlc
instance = vlc.Instance('--aout=alsa')
p = instance.media_player_new()
m = instance.media_new('1.mp3') 
p.set_media(m)

variable1 = input("Press A to play")

if variable1 == "A":
    p.play()
    while True:
        pass


