import pygame
import numpy as np
import base64


def play():
    
    filename = open("count.txt","r")
    file = filename.read()
    filename.close()

    freq = 44100
    bitsize = 16
    channels = 2
    buffer = 1024
    pygame.mixer.init(freq, bitsize, channels, buffer)

    pygame.mixer.music.set_volume(0.8)

    clock = pygame.time.Clock()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()


def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()