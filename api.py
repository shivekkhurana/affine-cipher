# -*- coding: utf-8 -*-
#coding=utf-8
from affine import *

def g_encrypt(string,a,b):
	return Affine(string, "devnagri.txt").encrypt(a,b)

def g_decrypt(string,a,b):
	return Affine(string, "devnagri.txt").decrypt(a,b)

def g_break(string,accuracy=2):
	return Affine(string, "devnagri.txt").break_affine(accuracy)
def g_break_f(string):
        return Affine(string, "devnagri.txt").break_affine_frequency("अक")
