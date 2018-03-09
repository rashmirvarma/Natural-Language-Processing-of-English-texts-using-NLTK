##Author: Rashmi Varma
##Created: November 16, 2017
## Sonification of text
 
from music import *
from image import *
from random import *
 
soundscapeScore = Score("Greyscale Soundscape", 60)
soundscapePart  = Part(HARMONICA, 0) 
minPitch = 0        
maxPitch = 127 
minDuration = 0.8   
maxDuration = 6.0
minVolume = 0       
maxVolume = 127

 
image = Image("Img_Son.jpg")
 
pixelRows = [0, 53, 106, 159, 212]
width = image.getWidth()     
height = image.getHeight()   

def sonifyPixel(pixel):
   red, green, blue = pixel  
   luminosity = (red + green + blue) / 3  
   pitch = mapScale(luminosity, 0, 255, minPitch, maxPitch, scale)
   duration = mapValue(red, 0, 255, minDuration, maxDuration)
   dynamic = mapValue(blue, 0, 255, minVolume, maxVolume)
   note = Note(pitch, duration, dynamic)   
    return note
 
 
for row in pixelRows:   
   for col in range(width):  
      pixel = image.getPixel(col, row)
      note = sonifyPixel(pixel)
      startTime = float(col)   
      startTime = startTime + choice( timeDisplacement )
 
      phrase = Phrase(startTime)  
      phrase.addNote(note)         
 
      soundscapePart.addPhrase(phrase)
 
soundscapeScore.addPart(soundscapePart)
View.sketch(soundscapeScore)
Play.midi(soundscapeScore)
