#!/usr/bin/python
#coding=utf-8
from affine import *
a = A("devnagri.txt")
s = A("infile.txt")
#print a.alphabets
#print s.alphabets

c = Affine('ttttttweee', 'english.txt')
k = c.frequencify().read()
print k
#print Affine(k,'devnagri.txt').decrypt(5,7).read()

import os
os.remove("affine.pyc")
