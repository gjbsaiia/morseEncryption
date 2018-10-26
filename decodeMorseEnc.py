#!/usr/bin/python
import os
import sys
import string
from encodeMorse import morse
from decodeMorse import run

decAlphabet = {}

def main():
	keyPhrase = string.lower(raw_input("Enter keyPhrase: "))
	buildDic(keyPhrase)
	msg = run()
	decMsg = decryptMsg(msg)
	print(decMsg)

def buildDic(keyPhrase):
	encAlphabet = {}
	alphabet = []
	for key in morse:
		encAlphabet[key]=key
		alphabet.append(key)
	i = 0
	for char in keyPhrase:
		encAlphabet[alphabet[i]] = char
		i += 1
	for each in alphabet:
		if(not(each in keyPhrase)):
			encAlphabet[alphabet[i]] = each
			i += 1
	for key in morse:
		decAlphabet[encAlphabet[key]] = key

def decryptMsg(msg):
	decMsg = ""
	for char in msg:
		decMsg += decAlphabet[char]
	return decMsg

#Execute the wrapper
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print 'Interrupted'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
