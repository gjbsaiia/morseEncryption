#!/usr/bin/python
import os
import sys
import wave
from scipy.io import wavfile
import struct

morse = {
	"._":"a",
	"_...":"b",
	"_._.":"c",
	"_..":"d",
	".":"e",
	".._.":"f",
	"__.":"g",
	"....":"h",
	"..":"i",
	".___":"j",
	"_._":"k",
	"._..":"l",
	"__":"m",
	"_.":"n",
	"___":"o",
	".__.":"p",
	"__._":"q",
	"._.":"r",
	"...":"s",
	"_":"t",
	".._":"u",
	"..._":"v",
	".__":"w",
	"_.._":"x",
	"_.__":"y",
	"__..":"z",
	".____":"1",
	"..___":"2",
	"...__":"3",
	"...._":"4",
	".....":"5",
	"_....":"6",
	"__...":"7",
	"___..":"8",
	"____.":"9",
	"_____":"0",
	"._...":"&",
	".____.":"'",
	".__._.":"@",
	"_.__._":")",
	"_.__._":"]",
	"_.__.":"(",
	"_.__.":"[",
	"___...":":",
	"__..__":",",
	"_.._":"=",
	"_._.__":"!",
	"._._._":".",
	"_...._":"-",
	"._._.":"+",
	"._.._.":'"',
	"..__..":"?",
	"_.._.":"/",
	" ":" "
}

def main():
	msg = run()
	print(msg)

def run():
	path = raw_input("enter morse as .wav file: ")
	data = getData(path)
	dit, dash, spacer, nextChar, nextWord = findDitSize(data)
	morseMsg = parseMorse(dit, dash, spacer, nextChar, nextWord, data)
	msg = decodeMorse(morseMsg)
	return msg

def getData(path):
	wav = wave.open(path, "rb")
	dwidth = wav.getsampwidth()
	nframes = wav.getnframes()
	if(dwidth == 1):
		fmt = "%iB" % nframes
	elif(dwidth == 2):
		fmt = "%ih" % nframes
	else:
		print("error, with file format")
		raise KeyboardInterrupt
	packedData = wav.readframes(nframes)
	wav.close()
	data = struct.unpack(fmt, packedData)
	return data

def findDitSize(data):
	i = 0
	count = 0
	dit = 0
	dash = 0
	spacer = 0
	nextChar = 0
	nextWord = 0
	while(data[i] != 0 or data[i+1] != 0):
		count += 1
		i += 1
	i, space = getSpace(data, i)
	while(dit == 0):
		ditDiv = space/7.0
		if(ditDiv == count):
			dit = count
			dash = 3*count
			nextWord = space
			nextChar = dash
		elif(ditDiv*3.0 == count):
			dash = count
			dit = count/3.0
			nextWord = space
			nextChar = dash
		elif(space == count):
			dash = count
			dit = count/3.0
			nextChar = space
			nextWord = 7*dit
		elif(space/3.0 == count):
			dit = count
			dash = 3*count
			nextChar = space
			nextWord = 7*dit
		else:
			i, dc = nonZero(data, i)
			i, space = getSpace(data, i)
	i = 0
	i, dc = nonZero(data, i)
	spacer = getSpacer(data, i, nextChar)
	return (dit, dash, spacer, nextChar, nextWord)

def getSpacer(data, i, nextChar):
	space = 0
	while(data[i] == 0 and data[i+1] == 0):
		space += 1
		i += 1
	if(space >= nextChar):
		i, dc = nonZero(data, i)
		return getSpacer(data,i,nextChar)
	else:
		return space

def getSpace(data, i):
	space = 0
	while(data[i] == 0 and data[i+1] == 0):
		space += 1
		i += 1
	return (i, space)

def nonZero(data, i):
	counter = 0
	while(data[i] != 0 or data[i+1] != 0):
		i += 1
		counter += 1
	return (i, counter)

def parseMorse(dit, dash, spacer, nextChar, nextWord, data):
 	characters = []
	current = ""
	i = 0
	while i < len(data):
		try:
			if(data[i] != 0 or data[i+1] != 0):
				i, value = nonZero(data, i)
				if(dit <= value < dash):
					current += "."
				elif(value <= dash):
					current += "_"
				else:
					characters.append(current)
					print("ERROR: i="+str(i)+", value="+str(val))
					print(characters)
			elif(data[i] == 0 and data[i+1] == 0):
				i, space = getSpace(data, i)
				if(nextWord <= space):
					characters.append(current)
					current = ""
					characters.append(" ")
				elif(spacer < space <= nextChar):
					characters.append(current)
					current = ""
		except IndexError:
			characters.append(current)
			break;
	printMorse(characters)
	return characters

def decodeMorse(mm):
	msg = ""
	try:
		for each in mm:
			if(each != ''):
				msg += morse[each]
		return msg
	except KeyError:
		print(msg)
		print("ERROR: unknown key "+each)
		raise KeyboardInterrupt

def printMorse(char):
	morse = '"'
	for each in char:
		morse+=each
	morse+='"'
	print(morse)

#Execute the wrapper
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print 'oops... interrupted \_[o.O]_/'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
