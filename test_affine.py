#!/usr/bin/python
#coding=utf-8
from affine import *
import unittest

#!/usr/bin/python
# -*- coding: utf-8 -*-

original = Affine("बिक्रम मेरो नाम हो",'devnagri.txt')

encrypt = original.encrypt(5,7)
print "encrypted :\n", encrypt.read()

print "break attempts :\n"
choice1=raw_input("Do you want to try frequency analysis based decryption yes/no?")
if choice1=='yes':
    print Affine(encrypt.read(),'devnagri.txt').break_affine_frequency("नज").read()
choice2=raw_input("Do you want to try brute force yes/no? ")
if choice2=='yes':
    print Affine(encrypt.read(), 'devnagri.txt').break_affine(2).read()

choice3=raw_input("Do you want to try all keys yes/no?")
if choice3=='yes':
    print Affine(encrypt.read(), 'devnagri.txt').break_affine_manually()
import os
os.remove("affine.pyc")
