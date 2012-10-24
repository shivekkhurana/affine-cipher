from affine import *
a = Alphabets("hindi_alphabets.txt")
b= a.alphabets
for i in b:
  print i.value
import os
os.remove("affine.pyc")
