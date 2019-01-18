#!/usr/bin/python
import os
import sys
import string
from encodeMorse import start, morse, convertToMorse

encAlphabet = {}

def main():
	flag = True
	while(flag):
		keyPhrase = string.lower(raw_input("enter your key phrase: "))
		if(checkKey(keyPhrase)):
			print("key phrase cannot contain repeat characters")
		else:
			flag = False
	buildDic(keyPhrase)
	input = start()
	encInput = encrypt(input)
	print("encrypted message: "+encInput)
	print("converting to morse...")
	convertToMorse(encInput)
	print("...converted and stored.")

def checkKey(keyPhrase):
	i = 0
	j = len(keyPhrase)-1
	flag = False
	while(i < len(keyPhrase)):
		if(flag):
			break
		while(j > i):
			if(keyPhrase[i] == keyPhrase[j]):
				print(keyPhrase[i]+", "+keyPhrase[j])
				flag = True
				break
			j -= 1
		j = len(keyPhrase)-1
		i += 1
	return flag

def buildDic(keyPhrase):
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

def encrypt(input):
	encrypted = ""
	for char in input:
		try:
			encrypted += encAlphabet[char]
		except KeyError:
			print("unknown character: "+char)
	return encrypted

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
