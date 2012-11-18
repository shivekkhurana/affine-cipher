#!/usr/bin/python
#coding=utf-8
import unicodedata as ucd
from fractions import gcd
import nitinbreaker as nb

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
    string = string.lower() #fix english, safe otherwise
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
    return sorted(s, key=lambda x:language.alphabets.index(x))

class Affine:
  '''
  All (en|de)crypt methods
  '''
  def __init__(self, string, language):
    self.string = A(string) #alphabet object to (en|de)crypt
    self.language = A(language) #alphabet object of the script of language being encoded or decoded (in alphabetic order)
    self.m = len(self.language.alphabets)

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
    @return 'A' object or None if inverse doesn't exist
    '''
    m = self.m
    try:
      z = self.get_inverse(a)
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

  def possible_keys(self):
    '''
    Generate all possible keys depending on the value of m for
    brute force cryptanalysis.
    '''
    m = self.m
    possible_keys=list()
    for i in range(1,m+1):
      if(gcd(i,m)==1):
        possible_keys.append(i)
    return possible_keys

  def validate(self,observation,corpus="hindi_corpus.txt"):
    '''
    Validate brutely cryptanalised A object against a corpus.

    @param observation : A object to analyse
    @param corpus : text file to analyse against
    @return bool:
      True if one word matches.
      False otherwise
    '''
    corpus = file(corpus)
    flag =  True
    matches = 0
    while flag:
      case = A(corpus.readline()).alphabets
      if len(case) == 0: continue
      for test in observation.read().split(' '):
        test = A(test).alphabets
        if len(test) == 0: continue
        if(test == case):
          print test,case
          if matches > 4:
            flag = False
            break
          else:
            matches +=1
            continue
    if not flag:
      return observation
    return None

  def break_affine(self):
    '''
    Match two most occuring elements in langauage to two most occuring
    elements in the given string. Ask user if the return is apt. If not
    repeat it with next most occuring elements.

    @param raw_string or text file
    @return A(object) or None
    '''

    for i in self.possible_keys():
      for j in range(self.m):
        decrypt = self.decrypt(i,j)
        if decrypt != None:
          if self.validate(decrypt) != None:
            return decrypt
    return None
