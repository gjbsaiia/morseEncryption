#!/usr/bin/python
import os
import sys
import string
from encodeMorse import inputStart, morse, convertToMorse

encAlphabet = {}

def main():
	flag = True
	while(flag):
		keyPhrase = string.lower(raw_input("Enter your key phrase: "))
		if(checkKey(keyPhrase)):
			print("key phrase cannot contain repeat characters")
		else:
			flag = False
	buildDic(keyPhrase)
	input = inputStart()
	encInput = encrypt(input)
	print(encInput)
	convertToMorse(encInput)

def checkKey(keyPhrase):
	actual = (len(keyPhrase)*1.0)/2
	intAct = len(keyPhrase)/2
	if(actual == intAct):
		pivot = intAct
	else:
		pivot = intAct+1
	i = 0
	j = pivot
	flag = False
	while(i < pivot):
		if(flag):
			break
		j = pivot
		while(j < len(keyPhrase)):
			if(keyPhrase[i] == keyPhrase[j]):
				print(keyPhrase[i]+", "+keyPhrase[j])
				flag = True
				break
			j += 1
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
		print 'Interrupted'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
