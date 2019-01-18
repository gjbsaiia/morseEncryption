#!/usr/bin/python
import os
import sys
import math
import wave
import struct
import string

srate = 8000.0
vol = 0.75
freq = 450.0
ditDur = 150
dashDur = 3 * ditDur
btwDur = ditDur/10.0

def main():
	input = start()
	print("converting to morse...")
	convertToMorse(input)
	print("...msg converted")


def start():
	global ditDur
	global btwDur
	ditDur = int(raw_input("enter dit duration: "))
	if(ditDur < 2):
		print("message cannot be decoded at a speed less than 2 micros per dit.")
		ditDur = 2
	recalculateDependents()
	if(btwDur < 1):
		btwDur = 1
	line = raw_input("type or use file?(t/f) ")
	if(line == "t"):
		input = string.lower(raw_input("enter Message: "))
	else:
		filen = raw_input("file path: ")
		input = string.lower(readText(filen))
	return input

def inputStart():
	global ditDur
	global btwDur
	ditDur = 2
	recalculateDependents()
	btwDur = 1
	line = raw_input("type or use file?(t/f) ")
	if(line == "t"):
		input = string.lower(raw_input("enter message: "))
	else:
		filen = raw_input("file path: ")
		input = string.lower(readText(filen))
	return input

def readText(filen):
	lines = []
	with open(filen, "r+") as file:
		lines = file.readlines()
	file.close()
	text = ""
	for line in lines:
		splitt = line.split()
		nwline = ' '.join(splitt)
		text += nwline+" "
	return text

def recalculateDependents():
	global ditDur
	global dashDur
	global btwDur
	dashDur = 3 * ditDur
	btwDur = ditDur/10.0

def dit():
	audio = appendComboSinwave(ditDur)
	return audio

def dash():
	audio = appendComboSinwave(dashDur)
	return audio

def betweenWords():
	audio = appendSilence((ditDur * 7) - btwDur)
	return audio

def betweenLetters():
	audio = appendSilence(dashDur-btwDur)
	return audio

def betweenSigs():
	audio = appendSilence(btwDur)
	return audio

morse = {
	"a":[dit, dash],
	"b":[dash,dit,dit,dit],
	"c":[dash,dit,dash,dit],
	"d":[dash,dit,dit],
	"e":[dit],
	"f":[dit,dit,dash,dit],
	"g":[dash,dash,dit],
	"h":[dit,dit,dit,dit],
	"i":[dit,dit],
	"j":[dit,dash,dash,dash],
	"k":[dash,dit,dash],
	"l":[dit,dash,dit,dit],
	"m":[dash,dash],
	"n":[dash,dit],
	"o":[dash,dash,dash],
	"p":[dit,dash,dash,dit],
	"q":[dash,dash,dit,dash],
	"r":[dit,dash,dit],
	"s":[dit,dit,dit],
	"t":[dash],
	"u":[dit,dit,dash],
	"v":[dit,dit,dit,dash],
	"w":[dit,dash,dash],
	"x":[dash,dit,dit,dash],
	"y":[dash,dit,dash,dash],
	"z":[dash,dash,dit,dit],
	"1":[dit,dash,dash,dash,dash],
	"2":[dit,dit,dash,dash,dash],
	"3":[dit,dit,dit,dash,dash],
	"4":[dit,dit,dit,dit,dash],
	"5":[dit,dit,dit,dit,dit],
	"6":[dash,dit,dit,dit,dit],
	"7":[dash,dash,dit,dit,dit],
	"8":[dash,dash,dash,dit,dit],
	"9":[dash,dash,dash,dash,dit],
	"0":[dash,dash,dash,dash,dash],
	"&":[dit,dash,dit,dit,dit],
	"'":[dit,dash,dash,dash,dash,dit],
	"@":[dit,dash,dash,dit,dash,dit],
	")":[dash,dit,dash,dash,dit,dash],
	"]":[dash,dit,dash,dash,dit,dash],
	"(":[dash,dit,dash,dash,dit],
	"[":[dash,dit,dash,dash,dit],
	":":[dash,dash,dash,dit,dit,dit],
	",":[dash,dash,dit,dit,dash,dash],
	"=":[dash,dit,dit,dash],
	"!":[dash,dit,dash,dit,dash,dash],
	".":[dit,dash,dit,dash,dit,dash],
	"-":[dash,dit,dit,dit,dit,dash],
	"+":[dit,dash,dit,dash,dit],
	'"':[dit,dash,dit,dit,dash,dit],
	"?":[dit,dit,dash,dash,dit,dit],
	"/":[dash,dit,dit,dash,dit],
	" ":[betweenWords]
}

def convertToMorse(msg):
	audio = []
	i = 0
	msg = msg.strip("\n")
	flag= False
	for each in msg:
		try:
			if(each == " "):
				flag =False
			else:
				flag = True
			decode = morse[each]
			for n in decode:
				out = n()
				audio += out
				spacer = betweenSigs()
				audio += spacer
			if(flag):
				b = betweenLetters()
				audio += b
		except KeyError:
			print("unknown character: "+each)
		except IndexError:
			break
	saveWav(audio, "message.wav")

def appendComboSinwave(dur):
	audio = []
	numSamples = dur * (srate / 1000.0)
	for x in range(int(numSamples)):
		y1 = sinFunc(srate, vol, freq, x)
		y2 = sinFunc(srate, vol, 2*freq, x)
		y3 = sinFunc(srate, vol, 2.5*freq, x)
		y4 = sinFunc(srate, vol, 1.5*freq, x)
		yF = (y1 + y2 + y3 + y4)/3
		audio.append(yF)
	return audio

def sinFunc(srate, vol, freq, x):
	y = vol * math.sin(2 * math.pi * freq * ( x / srate ))
	return y

def appendSilence(dur):
	audio = []
	numSamples = dur * (srate / 1000.0)
	for x in range(int(numSamples)):
	    audio.append(0.0)
	return audio

def saveWav(audio, name):
	wav_file=wave.open(name,"w")
	nchannels = 1
	sampwidth = 2
	nframes = len(audio)
	comptype = "NONE"
	compname = "not compressed"
	wav_file.setparams((nchannels, sampwidth, srate, nframes, comptype, compname))
	for sample in audio:
		wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))
	wav_file.close()
	return

#Execute the wrapper
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print
		print('oops... interrupted \_[o.O]_/')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
