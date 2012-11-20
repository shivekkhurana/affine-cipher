#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8

import unicodedata as ucd

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
      pass
    string = string.lower() #fix english, safe otherwise
    try:
      self.alphabets = string.decode('utf-8')#a list of all alphabets in required language
    except UnicodeEncodeError,e:
      #perhaps already unicode (as sent by Affine.encrypt)
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

  def frequencify(self, language):
    '''
    List of alphabets of string arranged in decreasing order of occurence.
    If an element has same occurance, then the element with lower index in script
    i.e the one which comes first is placed first (ex a is placed before b)

    @param 'A' object for language to which the string needs to be mapped
    @return list
    '''
    frequencified = {} #a dict to store occurences of a alphabet in unicode equivalent
    for alphabet in self.alphabets:
      if(frequencified.has_key(alphabet)):
        frequencified[alphabet] += 1 #if already occured +1 to occurence
      else:
        frequencified[alphabet] = 1 #never occured before
    s = list()

    for w in sorted(frequencified, key=lambda x:frequencified[x], reverse=True):
      if(w != 'SPACE' and (w not in s)):
        s.append(w)
    return s

class Affine:
  '''
  All (en|de)crypt methods
  '''
  def __init__(self, string, language):
    self.string = A(string) #alphabet object to (en|de)crypt
    self.language = A(language) #alphabet object of the script of language being encoded or decoded (in alphabetic order)
    self.m = len(self.language.alphabets)

  def gcd(self,a, b):
    '''
    Calculate greatest common dvisior of a,b. Eucledian Algorithm.
    @param : a,b
    @return : GCD of a,b
    '''
    while(b!=0):
       t= b
       b= a%b
       a=t
    return a

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
    if(self.gcd(m, a) == 1):
    #check a, m are relatively prime
      for alphabet in self.string.alphabets:
        if(alphabet == 'SPACE'):
          crypt+=' '
          continue
        x = self.language.alphabets.index(alphabet)
        y = (a*x + b)%m 
        crypt += ucd.lookup(self.language.alphabets[y])
      return A(crypt)
    else:
      raise ValueError("Expected co primes")
    
  def get_inverse(self,b,a): ##programme for calculating modular inverse of a in [ax=1 mod b]
    r=[a,b]
    t=[0,1]
    s=[1,0]
    q=[0]
    m= 1
  
    while(r[m]!=0):
        
        mm1=m-1
        mp1=m+1
        q.append(r[mm1]/r[m])

        r.append(r[mm1]-(q[m]*r[m]))
        t.append(t[mm1]-(q[m]*t[m]))
        s.append(s[mm1]-(q[m]*s[m]))
        m= m+1
    m=m-1
    return s[m]

  def decrypt(self, a, b):
    '''
    Decrypt string on the basis of given a,b
    y = a^(-1)(x-b)%m
    a^(-1) is z such that:
      az = 1%m

    @param int a
    @param int b
    @return 'A' object or None if inverse doesn't exist
    '''
    m = self.m
    try:
      z = self.get_inverse(m,a)
    except:
      return None
    crypt = ''
    for alphabet in self.string.alphabets:
      if(alphabet == 'SPACE'):
        crypt += ' '
        continue
      x = self.language.alphabets.index(alphabet)
      y = z*(x-b)%m
      crypt += ucd.lookup(self.language.alphabets[y])
    return A(crypt)

  def crack(self,p,q,r,s,m):##computes key's B and displacys the key set(a,b) for given p,q,r,s,m such than [ap+b=r (mod m)],[aq+b=s (mod m)]
    D=p-q
    D1=r-s
    if(self.gcd(D,m)==1):## equation are subtracted and converted to Da=D1 (mod m)
        k_a=(self.get_inverse(m,D)*D1)%m
    else:
        d=self.gcd(D,m)
        D=D/d
        D1=D1/d
        m=m/d
        k_a=(self.get_inverse(m,D)*D1)%m
    k_b=(r-p*k_a)%m
    return k_a,k_b
    
  def possible_keys(self):
    '''
    Generate all possible keys depending on the value of m for
    brute force cryptanalysis.
    '''
    m = self.m
    possible_keys=list()
    for i in range(1,m+1):
      if(self.gcd(i,m)==1):
        possible_keys.append(i)
    return possible_keys

  def validate(self,observation,accuracy,corpus="hindi_corpus.txt"):
    '''
    Validate brutely cryptanalised A object against a corpus.

    @param observation : A object to analyse
    @param corpus : text file to analyse against
    @return bool:
      True if one word matches.
      False otherwise
    '''
    corpus = file(corpus).read().split('\n')
    o_list = observation.read().split(' ')[0:10] #take only first ten observations if a big input.
    matches=0

    for word in corpus:
      word = word.decode('utf-8')
      for word_o in o_list:
        if len(word_o) == 0: continue
        if word_o == word:
          matches += 1
        if matches > accuracy:
          return observation
    return None
  
  def break_affine_frequency(self, f_table):
    '''
    Match two most occuring elements in langauage to two most occuring
    elements in the given string. Ask user if the return is apt. If not
    repeat it with next most occuring elements.

    @param raw_string or text file
    @return
    '''
    most_occuring = A(f_table)
    ordered_string = self.string.frequencify(self.language) #sorted list of alphabets arranged in decreasing order of occurance
    p = self.language.alphabets.index(most_occuring.alphabets[0])
    q = self.language.alphabets.index(most_occuring.alphabets[1])
    r = self.language.alphabets.index(ordered_string[0])
    s = self.language.alphabets.index(ordered_string[1])
    a,b=self.crack(p,q,r,s,self.m)
    decrypt = self.decrypt(a,b)
    return decrypt
      
  def break_affine(self,accuracy=2):
    '''
    Match two most occuring elements in langauage to two most occuring
    elements in the given string. Ask user if the return is apt. If not
    repeat it with next most occuring elements.

    @param raw_string or text file
    @return A(object) or None
    '''
    if len(self.string.read().split(' ')) < 3:accuracy = 1
    for i in self.possible_keys():
      print "Breaking at multiplier %s"%i
      for j in range(self.m):
        decrypt = self.decrypt(i,j)
        if decrypt != None:
          if self.validate(decrypt,accuracy) != None:
            print i,j," done"
            return decrypt,i,j
      print "Fail"
    return None
  
  def break_affine_manually(self):
    '''
    Try all keys.
    '''
    for i in self.possible_keys():
      for j in range(self.m):
        print self.decrypt(i,j).read()
        print i,j
