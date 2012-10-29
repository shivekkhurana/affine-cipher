#!/usr/bin/python
#coding=utf-8
from affine import *
a = A("devnagri.txt")
s = A("infile.txt")
#print a.alphabets
#print A("afsfsaascxvs").frequencify(A("english.txt"))

c = Affine('to infinity and beyond', 'english.txt')
k = c.encrypt(5,5).read()
#k = c.frequencify().read()

print k
#print Affine(k,'devnagri.txt').decrypt(5,7).read()

import os
os.remove("affine.pyc")
