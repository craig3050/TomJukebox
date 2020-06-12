from gpiozero import Button
from signal import pause

def button_4():
    print("button 4")

def button_17():
    print("button 17")

def button_27():
    print("button 27")

button4 = Button(4)
button17 = Button(17)
button27 = Button(27)

button4.when_pressed = button_4
button17.when_pressed = button_17
button27.when_pressed = button_27



pause()