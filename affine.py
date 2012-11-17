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
    @return 'A' object
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

  def break_affine(self, f_table):
    '''
    Match two most occuring elements in langauage to two most occuring
    elements in the given string. Ask user if the return is apt. If not
    repeat it with next most occuring elements.

    @param raw_string or text file
    @return
    '''
    most_occuring = A(f_table)
    ordered_string = self.string.frequencify(self.language) #sorted list of alphabets arranged in decreasing order of occurance
    """
    print ordered_string
    x1 = self.language.alphabets.index(most_occuring.alphabets[0])
    x2 = self.language.alphabets.index(most_occuring.alphabets[1])
    for i in range( len(ordered_string) ):
#print self.language.alphabets.index(ordered_string[i])

      try:
        y1 = self.language.alphabets.index(ordered_string[i])
        y2 = self.language.alphabets.index(ordered_string[i+1])
      except IndexError:
        continue
      '''
      a = (y1-y2)/(x1-x2)
      b = ((x1*y2) - (x2*y1))/(x1-x2)
      print "x1 = %s | x2 = %s | y1 = %s | y2 = %s | a = %s | b = %s \n\n"%(x1,x2,y1,y2,a,b), '-'*60, '\n'
      try:
        print self.decrypt(a,b).read()
        print '-'*60, '\n'
      except:
        print "Inverse doesn't exist"
      '''
      nb.crack(x1,x2,y1,y2,self.m)
    """
    for i in range(self.m):
      for j in range(self.m):
        try:
          print self.decrypt(i,j).read()
        except:
          pass
