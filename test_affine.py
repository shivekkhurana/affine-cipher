#!/usr/bin/python
#coding=utf-8
from affine import *
a = A("devnagri.txt")
s = A("infile.txt")
#print a.alphabets
#print A("afsfsaascxvs").frequencify(A("english.txt"))

c = Affine('infile.txt', 'devnagri.txt')
print "original string : \n",c.string.read(), "\n"
k = c.encrypt(5,5).read()
#k = c.frequencify("devnagri.txt").read()

print "encrypted string : \n", k, "\n"


print "break attempts : \n\n", '*'*60, "\n"
Affine(k,'devnagri.txt').break_affine("ाक")
#print k
#print Affine(k,'devnagri.txt').decrypt(5,7).read()

import os
os.remove("affine.pyc")
