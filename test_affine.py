#!/usr/bin/python
#coding=utf-8
from affine import *

original = Affine("infile.txt",'devnagri.txt')
print "original :\n", original.string.read()

encrypt = original.encrypt(5,5)
print "encrypted :\n", encrypt.read()

print "break attempts :\n"
print Affine(encrypt.read(), 'devnagri.txt').break_affine().read()
import os
os.remove("affine.pyc")
