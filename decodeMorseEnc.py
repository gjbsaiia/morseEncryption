#!/usr/bin/python
import os
import sys
import string
from encodeMorse import morse
from decodeMorse import run

decAlphabet = {}

def main():
	keyPhrase = string.lower(raw_input("enter key phrase: "))
	buildDic(keyPhrase)
	print("decoding morse message...")
	msg = run()
	print("...morse decoded.")
	print("encrypted output: "+msg)
	print("decrypting with "+'"'+keyPhrase+'"...')
	decMsg = decryptMsg(msg)
	print("...attempted decryption complete")
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
		print
		print 'oops... interrupted \_[o.O]_/'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
