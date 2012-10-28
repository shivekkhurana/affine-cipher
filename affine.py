#!/usr/bin/python
#coding=utf-8
import unicodedata as ucd
from fractions import gcd

class A:
  '''
  Object to hold a list of unicode equivalents of a string in any language
  in the form of a list()
  '''
  def __init__(self, string='hindi_alphabets.txt'):
    '''
    Converts content of a file or raw string into a list of Alphabet objects

    @param string 
      string is either raw text or a filename
      string defaults to input file
    '''
    try:
      string = file(string).read() #try reading a file
    except IOError as e:
      #raw input given
      #print e
      pass

    try:
      self.alphabets = string.decode('utf-8')#a list of all alphabets in required language
    except UnicodeEncodeError,e:
      #perhaps alreadt unicode (as sent by Affine.encrypt)
      self.alphabets = string
    alphabets_fixed = list()
    for a in self.alphabets:
      if(len(a) > 0):
        #take pain iff the element exists
        unicoded = ucd.name(a, 0) #default to 0
        if(unicoded != 0):
          #add alphabet to cluster only if it is recognized
          alphabets_fixed.append(unicoded)
    self.alphabets = alphabets_fixed
    return None

  def read(self):
    '''
    'A' object in traditional form
    @param None
    @return string
    '''
    read = ''
    for a in self.alphabets:
      read += ucd.lookup(a)
    return read

class Affine:
  '''
  All (en|de)crypt methods
  '''
  def __init__(self, string, language):
    self.string = A(string).alphabets #string is a list of alphabet objects to (en|de)crypt
    self.language = A(language).alphabets
    self.m = len(self.language)

  def frequencies(self, f_table, corpus=None):
    '''
    Frequencies are either predefined or estimated from a corpus.
    @param f_table
    	name of file or raw_string
    '''
    if(f_table != None):
      #f_table is a file or raw_text which contains two most occuring alphabets in a script in order of occurence
      #ex 'te' for english
      self.f_table = A(f_table)
    else:
      #get into corpus and generate an f_table and save it as a file f_table.json
      pass #for now !!!TODO!!!

  def frequencify(self):
    '''
    'A' object with alphabets of string arranged in decreasing order of occurence.
    If an element has same occurance, then the element with lower index in script
    i.e the one which comes first is placed first (ex a is placed before b)

    @param None
    @return A object
    '''
    frequencified = {}
    for alphabet in self.string:
      if(frequencified.has_key(alphabet)):
        frequencified[alphabet] += 1
      else:
        frequencified[alphabet] = 1
    #sorting fast as on http://stackoverflow.com/questions/613183
    s= ''

    for w in sorted(frequencified, frequencified.get):
      s += ucd.lookup(w)
    return A(s)

  def encrypt(self, a, b):
    '''
    Encrypt string on the basis of give a,b
    y = (ax + b)%(m)
    
    @param int a
    @param int b
    @return 'A' object
    '''
    crypt = ''
    m = self.m
    if(gcd(m, a) == 1):
    #check a, m are relatively prime
      for alphabet in self.string:
        if(alphabet == 'SPACE'):
          crypt+=' '
          continue
        x = self.language.index(alphabet)
        y = (a*x + b)%m 
        crypt += ucd.lookup(self.language[y])
      return A(crypt)
    else:
      raise ValueError("Expected co primes")

  def get_inverse(self,a):
    '''
    Inverse of 'a' for decryption
    
    @param int a
    @return int  
    '''
    for i in range(self.m):
      if((i*a)%self.m == 1):
        return i
    raise Exception, "the multiplicative %d has no inverse, try another"%a

  def decrypt(self, a, b):
    '''
    Decrypt string on the basis of given a,b
    y = a^(-1)(x-b)%m
    a^(-1) is z such that:
      az = 1%m
      
    @param int a
    @param int b
    @return 'A' object   
    '''
    m = self.m
    z = self.get_inverse(a)
    crypt = ''
    for alphabet in self.string:
      if(alphabet == 'SPACE'):
        crypt += ' '
        continue
      x = self.language.index(alphabet)
      y = z*(x-b)%m
      crypt += ucd.lookup(self.language[y])
    return A(crypt)

  def break_affine(self, f_table):
    most_occuring = A(f_table)
    ordered_string = self.frequencify() #an A object with alphabets arranged in decreasing order of occurance
