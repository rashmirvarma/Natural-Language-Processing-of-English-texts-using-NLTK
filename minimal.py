##Author: Rashmi Varma
##Created: November 16, 2017

from music import *
import collections
import math

filename = "ny.csv"

dataset = open(filename, "r")

header_line = dataset.readline()
print(header_line)

tempByMonth = {}
avgTemperatures = []
data = dataset.readlines() 
for record in data:
   record = record.split(',')
   x = float(record[11])
   avgTemperatures.append(x)
   tempByMonth.update({record[6]:x})
    
minVelocity = min(avgTemperatures)
maxVelocity = max(avgTemperatures)
print "Month:Temp",tempByMonth
print "Average Temperatures:",avgTemperatures
tempPitches = []
tempDurations = []
od = collections.OrderedDict(sorted(tempByMonth.items()))
print(od)
keyList = od.keys()
for key in keyList:
    pitch = mapScale(int(od[key]), 0, 127, C1, C6, CHROMATIC_SCALE)
    tempPitches.append( pitch )
    tempDurations.append( EN )
 
# create the planet melodies
melody1 = Phrase(0.0)      # starts at beginning
#melody2 = Phrase(10.0)     # starts 10 beats into the piece
#melody3 = Phrase(20.0)     # starts 20 beats into the piece
 
# create melody 1 (theme)
melody1.addNoteList(tempPitches, tempDurations)
 
# melody 2 starts 10 beats into the piece and
# is elongated by a factor of 2
#melody2 = melody1.copy()
#melody2.setStartTime(10.0)
#Mod.elongate(melody2, 2.0)
 
# melody 3 starts 20 beats into the piece and
# is elongated by a factor of 4
#melody3 = melody1.copy()
#melody3.setStartTime(20.0)
#Mod.elongate(melody3, 4.0)
 
# repeat melodies appropriate times, so they will end together
#Mod.repeat(melody1, 8)
#Mod.repeat(melody2, 3)
 
# create parts with different instruments and add melodies
part1 = Part("Eighth Notes", PIANO, 2)
#part2 = Part("Half Notes", DRUM, 5)
#part3 = Part("Half Notes", GUITAR, 2)
part1.addPhrase(melody1)
#part2.addPhrase(melody2)
#part3.addPhrase(melody3)
 
# finally, create, view, and write the score
score = Score("Temperatures")
score.addPart(part1)
#score.addPart(part2)
#score.addPart(part3)
Metronome(100,4/4)
View.sketch(score)
Play.midi(score)
