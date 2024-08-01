# MASTER SCRIPT
#
#
# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

import os
import fnmatch
import random
import math

# mediaPath = 'C:\\Projects\\Ursuppe\\MediaFiles\\12fps_sortedAll_HAP'
mediaPath = '../../../../_MediaFiles/12fps_sortedAll_HAP'
genome = 'Genomes/Nanoarchaeum_Equitans/genomeRAW.txt' 

# for root, directories, files in os.walk(mediaPath, topdown=False):
# 	for name in files:


# null, 1. Szene (on), 2.Sz, 3.Sz, 4.Sz, MashUp Mutation, Full Distortion, Ende (off), Restart
# evolutionLeaps = [0, 1, 15, 30, 45, 60] #  60 => ca. 8:30 min.
evolutionLeaps = [0, 1, 10, 20, 30, 40, 55, 65, 75] #  60 => ca. 8:30 min.
# evolutionLeaps = [0, 1, 3,  5,  7,  9,  20, 22, 25] #  60 => ca. 8:30 min.
# evolutionLeaps = [0, 1, 2,  3,  4,  5,  25, 30, 35] #  60 => ca. 8:30 min.
# evolutionLeaps = [0, 1, 2,  3,  4,  5,  6, 10, 15] #  60 => ca. 8:30 min.


evolutionLevels = [0, 0, 0]
endDistortion = -1



layerScene = [1, 2, 3]
currentClip = [0, 0, 0]

# loopClip = [True, True, True]
loopClip = [False, False, False]
mutationMode = False
layerLoops = [0, 0, 0]
audioLoopPos = [0.0, 0.0, 0.0]
fullDistortion = False
loopLength = [60, 60, 60]



print('/////////// START //////////')


###### LOAD VIDEO FILES INTO ARRAY ######

videoFiles = []
fileSceneIndex = []
isNew = True

 
for (root, directories, filenames) in os.walk(mediaPath):
	directories.sort()
	for d in directories:

		allfiles = os.listdir(os.path.join(root, d))
		firstIndex = True

		for f in fnmatch.filter(allfiles, '*.mov'):

			videoFiles.append(os.path.join(d , f))

			if firstIndex:
				fileSceneIndex.append(len(videoFiles)-1)	# save at which index the new scene starts
				firstIndex = False
			
fileSceneIndex.append(len(videoFiles))	# add the total length of video files at the end


print("files: ")
print(videoFiles)

print("file Scene index: ")
print(fileSceneIndex)



with open(genome, 'r') as file:
    fullGenome = file.read().rstrip()


randomSeed = random.randint(0, math.floor(len(fullGenome) / 3) - 1 ) * 3
genomeIterator = randomSeed
foundGenomeStart = False
 
genomeCounter = 0
op('genomeCounter').par.value0 = 0


print('full genome length: ' + str(len(fullGenome)))
print('randomSeed: ' + str(randomSeed))
print('first triplet: ' + fullGenome[genomeIterator:genomeIterator+3])









def onStart():
	isNew = False



	return

def onCreate():
	return

def onExit():
	return

def onFrameStart(frame):

	# if (op('movie1').isLoopFrame):
	# 	op('constant1').par.value0 = 1
	# if (op('movie2').isLoopFrame):
	# 	op('constant1').par.value1 = 1
	# if (op('movie3').isLoopFrame):
	# 	op('constant1').par.value2 = 1

	findGenome()

	return

def onFrameEnd(frame):
	global loopLength

	if (op('movie1').isLastFrame):	
		loadClip(1)
		# op('constant1').par.value0 = 0	
		# op("oscout1").sendOSC('loop1', '5')
	elif mutationMode and op('movie1').index >= loopLength[0]:
		loadClip(1)


	if (op('movie2').isLastFrame):		
		loadClip(2)
		# op('constant1').par.value1 = 0
	elif mutationMode and op('movie2').index >= loopLength[1]:
		loadClip(2)


	if (op('movie3').isLastFrame):		
		loadClip(3)
		# op('constant1').par.value2 = 0
	elif mutationMode and op('movie3').index >= loopLength[2]:
		loadClip(3)

	return



def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
	return

def onProjectPostSave():
	return


def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y


###### LOAD A NEW CLIP INTO MOVIE PLAYER ######

def loadClip(lyrNum):
	global layerScene
	global layerLoops
	global mutationMode
	global audioLoopPos
	global loopLength

	global evolutionLeaps
	global genomeCounter

	# if not loopClip[lyrNum-1]:

	thisScene = layerScene[lyrNum-1]
	# mashUp = True if thisScene == 5 else False
	pick = currentClip[lyrNum-1]

	if not mutationMode:
		while (pick == currentClip[0] or pick == currentClip[1] or pick == currentClip[2]):		# avoid to pick the same clip again or the same that is playing on another layer
			pick = random.randint( fileSceneIndex[thisScene], fileSceneIndex[thisScene+1]-1 )	# pick in the range of the corresponding scene
	else:
		# mash-up loop mode
		if layerLoops[lyrNum-1] <= 0:	# if loop counter has ended
			mappedPosition = mapFromTo(genomeCounter, evolutionLeaps[5]*3, evolutionLeaps[6]*3, 1.0, 0.0)
			mappedPosition = max(0.0, min(mappedPosition, 1.0))

			# print('mapped Pos: ' + str(mappedPosition))

			minLoopTime = math.floor(1 + mappedPosition*36)
			maxLoopTime = math.floor(5 + mappedPosition*60)

			print('min time: ' + str(minLoopTime))


			maxLoops = math.floor((1.0-mappedPosition) * 5)

			layerLoops[lyrNum-1] = random.randint(0, maxLoops)		# set the loop iterations anew
			loopLength[lyrNum-1] = random.randint(minLoopTime, maxLoopTime)	#	 12, 36

			# layerLoops[lyrNum-1] = random.randint(0, 5)		# set the loop iterations anew
			# loopLength[lyrNum-1] = random.randint(36, 60)	#	 12, 36
			audioLoopPos[lyrNum-1] = round(random.random(), 3)

			# pick = currentClip[lyrNum-1]
			randScene = random.randint(1, 4)	# choose a random scene
			while (pick == currentClip[0] or pick == currentClip[1] or pick == currentClip[2]):		# avoid to pick the same clip again or the same that is playing on another layer
				pick = random.randint( fileSceneIndex[randScene], fileSceneIndex[randScene+1]-1 )						# pick one from the random scene
			layerScene[lyrNum-1] = randScene	# save in which scene we are now
			setAudioFile(lyrNum, randScene, audioLoopPos[lyrNum-1])	# set the audio accordingly
		else:	# else LOOP Video and Audio
			op('movie'+str(lyrNum)).par.cuepulse.pulse()	# restart or "loop" the video clip
			setAudioFile(lyrNum, thisScene, audioLoopPos[lyrNum-1])	# restart the audio
			layerLoops[lyrNum-1] -= 1	# diminish the loop counter
			print('Loops left: ' + str(layerLoops[lyrNum-1]))
			return		# BREAK FUNCTION HERE


	print( 'pick No: ' + str(pick))
	op('movie'+str(lyrNum)).par.file = os.path.join(mediaPath, videoFiles[pick])		# load the actual file
	print( 'new Clip - Layer ' + str(lyrNum) + ': ' + videoFiles[pick] )
	currentClip[lyrNum-1] = pick

	# flip the video horizontally by a 50:50 chance
	if random.randint(0, 1) == 1:
		op('flip'+str(lyrNum)).par.flipx = 1
	else:
		op('flip'+str(lyrNum)).par.flipx = 0

	# flip the video vertically by a 50:50 chance but ONLY if it has the token $ in its file name
	if random.randint(0, 1) == 1 and '$' in videoFiles[pick]:
		# if random.randint(0, 1) == 1:
		op('flip'+str(lyrNum)).par.flipy = 1
		# else:
		# 	op('flip'+str(lyrNum)).par.flipy = 0
	else:
		op('flip'+str(lyrNum)).par.flipy = 0
	
	return







###### SET SCENE OF THE LAYERS AND ACTIVATE / DEACTIVATE ######
 
def changeLayer(lyrNum, scene, startPos):
	global layerScene

	layerScene[lyrNum-1] = scene
	loadClip(lyrNum)
	setAudioFile(lyrNum, scene, startPos)



def activateLayer(lyrNum, active):

	op('active'+str(lyrNum)).par.value0 = active
	address = '/activateLayer'
	val = [lyrNum, active]	# must be a list [] to be accepted as osc message - a list of only one value is valid too
	op("oscout1").sendOSC(address, val)



def setAudioStem(lyrNum, stem):

	# op('active'+str(lyrNum)).par.value0 = active
	address = '/setStem'
	val = [lyrNum, stem]	# must be a list [] to be accepted as osc message - a list of only one value is valid too
	op("oscout1").sendOSC(address, val)

 

def setAudioDistortion(distAmount):
	
	for i in range(1,4):
		address = '/distortion'
		val = [i, distAmount]	# must be a list [] to be accepted as osc message - a list of only one value is valid too
		op("oscout1").sendOSC(address, val)


def setAudioFile(lyrNum, scene, startPos):

	address = '/setLayer'
	val = [lyrNum, scene, startPos]	# must be a list [] to be accepted as osc message - a list of only one value is valid too
	op("oscout1").sendOSC(address, val)


def toggleAudioIntermission(on):
	address = '/startInt'
	val = [on]	# must be a list [] to be accepted as osc message - a list of only one value is valid too
	op("oscout1").sendOSC(address, val)


def triggerAudioReset():
	address = '/Init'
	val = [1]	# must be a list [] to be accepted as osc message - a list of only one value is valid too
	op("oscout1").sendOSC(address, val)



def findGenome():
	global foundGenomeStart
	global fullGenome
	global genomeIterator
	global genomeCounter
	global endDistortion
	global fullDistortion
	global evolutionLeaps
	global mutationMode
 
	sample = fullGenome[genomeIterator:genomeIterator+3]

	if not foundGenomeStart and sample == 'ATG':
		foundGenomeStart = True
		genomeCounter += 1
		op('genomeCounter').par.value0 = genomeCounter		
		evolve()
	elif foundGenomeStart:
		if sample == 'TAA' or sample == 'TAG' or sample == 'TGA':
			foundGenomeStart = False
 	
	if sample == 'TGG' and endDistortion < genomeIterator and mutationMode:		# turn distortion on once that specific codon is found		and only if Mutation Mode is on
		# if random.randint(0, max((evolutionLeaps[6]*3 - genomeCounter), 0)) == 0:		# make the probalility low in the beginning and higher towards the end
		if genomeCounter >= ( evolutionLeaps[5]*3 + (evolutionLeaps[6]-evolutionLeaps[5])/2*3 ):		# start only from the middle of Mutation Mode
			op('distortionAmount').par.value0 = 1
			setAudioDistortion(1.0)
			# endDistortion = genomeIterator + (genomeCounter * 3)	# turn distortion off after the mount of frames as the number of genomeCounter	!! does not wrap like the Iterater !! source of error !!
			endDistortion = genomeIterator + (max((genomeCounter - evolutionLeaps[5]*3), 3) * 3)	# add the amount of frames as the genomeCounter increases - but start counting from Mutation Mode onwards!
			# print('genomeIteratr: ' + str(genomeIterator))
			# print('endDistortion: ' + str(endDistortion))

	if genomeIterator == endDistortion:
		if not fullDistortion:
			op('distortionAmount').par.value0 = 0
			setAudioDistortion(0.0)
			print('Distortion OFF')

	

	# WRAP THE GENOME ITERATOR once the full length has been passed
	if genomeIterator <= len(fullGenome)-3:
		genomeIterator = genomeIterator + 3
	else: 
		endDistortion = endDistortion - genomeIterator
		genomeIterator = 0

	# genomeIterator = genomeIterator + 3 if genomeIterator <= len(fullGenome)-3 else 0		# short wrap version


	# print(sample)

 
def evolve():
	global evolutionLevels
	global evolutionLeaps
	global mutationMode
	global fullDistortion

	layer = 0
	layerChosen = False

	# CHOOSE A LAYER - randomly - to step up in the evolution
	# but if a layer is about to step into the next evolutionary leap, check first if the others are also arrived a the fringe to the next leap - if not choose another layer
	# also if a layer has just entered a new evolutionaly stage, check if the others have done the step into this stage as well - if not choose one of them
	while not layerChosen:
		layer = random.randint(1, 3)
		thisLevel = evolutionLevels[layer-1]
		nextLevel = evolutionLevels[layer-1] + 1
		
		if nextLevel in evolutionLeaps:
			if evolutionLevels[0] >= thisLevel and evolutionLevels[1] >= thisLevel and evolutionLevels[2] >= thisLevel:
				layerChosen = True
		elif thisLevel in evolutionLeaps:
			if evolutionLevels[0] >= thisLevel and evolutionLevels[1] >= thisLevel and evolutionLevels[2] >= thisLevel:
				layerChosen = True
		else:
			layerChosen = True


	# if everthing's fine, step up the chosen layer in the evolution
	nextLevel = evolutionLevels[layer-1] + 1
	evolutionLevels[layer-1] = nextLevel
	op('evoLvl'+str(layer)).par.value0 = nextLevel	
 

	# if the next step happens to be a evolution leap, change the layer accordingly (change the scene)
	for i in range(0, len(evolutionLeaps)):
		if nextLevel == evolutionLeaps[len(evolutionLeaps)-2]:
			# in the special case that the next evolution leap is the second last one, don't change the scene but turn off the layer -> "evolution has come to an end"
			activateLayer(layer, 0)

			state1 = op('active1').par.value0
			state2 = op('active2').par.value0
			state3 = op('active3').par.value0
			if state1 == 0 and state2 == 0 and state3 == 0:
				toggleAudioIntermission(1)
			break
		elif nextLevel == evolutionLeaps[len(evolutionLeaps)-1]:
			# if its the last leap: RESTART THE WHOLE THING
			init()
			break
		elif nextLevel == 1:
			# if its the first, turn on the layer
			state1 = op('active1').par.value0
			state2 = op('active2').par.value0
			state3 = op('active3').par.value0
			if state1 == 0 and state2 == 0 and state3 == 0:
				toggleAudioIntermission(0)

			activateLayer(layer, 1)	
			break
		elif nextLevel == evolutionLeaps[5]:
			# if its step 5: change to Mutation Mode
			mutationMode = True
			loadClip(layer)
			break
		elif nextLevel == evolutionLeaps[6]:
			# if its step 6: change to Full Distortion
			fullDistortion = True
			op('distortionAmount').par.value0 = 1
			setAudioDistortion(1.0)
			break
		elif nextLevel == evolutionLeaps[i]:
			# if its on of the other evolution steps: change the scene number accordingly
			playPosition = round(random.random(), 3)
			# playPosition = 0.0
			changeLayer(layer, i, playPosition)
			# changeLayer(layer, i, playPosition)
			# activateLayer(layer, 1)			# to osc messages right after another fucks MAX up because its logic is totally crap
			break
		else:
			# if its a inner scene step turn randomly layers off
			activeState = op('active'+str(layer)).par.value0

			deactivateProbability = 4 if mutationMode else 1

			if nextLevel+1 not in evolutionLeaps:
				if activeState == 1 and not fullDistortion:

					if random.randint(0, deactivateProbability) == 0:
						activateLayer(layer, 0)

						state1 = op('active1').par.value0
						state2 = op('active2').par.value0
						state3 = op('active3').par.value0
						if state1 == 0 and state2 == 0 and state3 == 0:
							activateLayer(layer, 1)

				elif activeState == 0:
					if random.randint(0, 1) == 0 and not fullDistortion:
						activateLayer(layer, 1)
			elif not fullDistortion:
				activateLayer(layer, 1)


			# if random.randint(0, 1) == 0:
			# 	activeState = op('active'+str(layer)).par.value0
			# 	activeState = abs(activeState - 1)
			# 	activateLayer(layer, activeState)





 
 
 


def OSCreceived(oscMsg):
	# print(oscMsg)
	msg = oscMsg.split()
	if msg[0] == '/distortion':
		op('distortionAmount').par.value0 = float(msg[1])
	# else:
		# changeLayer(int(msg[1]), int(msg[2]), int(msg[3]))
		# changeLayer(int(msg[1]), int(msg[2]))
 

 

def init():
	global evolutionLevels
	global genomeCounter
	global foundGenomeStart
	global mutationMode
	global fullDistortion

	evolutionLevels = [0, 0, 0]
	layerLoops = [0, 0, 0]
	genomeCounter = 0
	op('genomeCounter').par.value0 = 0
	foundGenomeStart = False
	mutationMode = False
	fullDistortion = False
	setAudioDistortion(0.0)

	triggerAudioReset()

	for i in range(1,4):
		playPosition = round(random.random(), 3)
		# playPosition = 0.0
		activateLayer(i, 0)
		# setAudioStem(i, 1)
		setAudioStem(i, i)
		changeLayer(i, 1, playPosition)
		op('evoLvl'+str(i)).par.value0 = 0	
		op('distortionAmount').par.value0 = 0
 
init()
