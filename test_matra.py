#/usr/bin/python 
# -*- coding: utf-8 -*- 
from affine import *
import os
encrypt = Affine("ग़ऐढ़सग़ ग़ऐथसूऋोू ॣऋग़नऋफ","devnagri.txt").break_affine_matra()
print encrypt.read()
os.remove("affine.pyc")
