#coding:utf-8

'''return secret pass'''
def encodePassword(password,key):
	return ''.join(["%04x"%(ord(char)^ord(key[offset % len(key)])) for offset,char in enumerate(password)])
	
'''return src pass'''
def decodePassword(password, key):
	passw=[int(password[i:i+4], 16) for i in xrange(0, len(password), 4)]
	return ''.join([unichr(char^ord(key[offset % len(key)])) for offset,char in enumerate(passw)])