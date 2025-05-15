from gtts import gTTS
import pygame
import os

class AudioSystem:
    def __init__(self):
        pygame.mixer.init()
    
    def play_message(self, text):
        # Generate speech
        tts = gTTS(text=text, lang='en')
        tts.save("alert.mp3")
        
        # Play audio
        pygame.mixer.music.load("alert.mp3")
        pygame.mixer.music.play()
        
        # Keep program running while playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
