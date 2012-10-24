import unicodedata as ucd

class Alphabet:
  def __init__(self, value):
    value = ucd.name( unichr(value), 0 )
    self.value = value#ucd.name( unicode(value) ) #the alphabet itself in unicode.
    return None

class Alphabets:
  def __init__(self, a_file=None):
    '''
    a_file is a file contaning all alphabets in sequence
    ex:
      abcdef...z
    in any script
    '''
    a_file = a_file if a_file else "alphabets.txt"
    self.alphabets = file(a_file).read().split('\n')#a list of all alphabets in required language
    alphabets_fixed = list()
    for i in range(len(self.alphabets)):
      if(len(self.alphabets[i]) > 0):
        #take pain iff the element exists
        try:
          a_object = Alphabet( int(self.alphabets[i]) )
        except ValueError,e:
          a_object = Alphabet( int(self.alphabets[i], 16) )
        if(a_object.value != 0):
          alphabets_fixed.append(a_object)
    self.alphabets = alphabets_fixed
    return None

class Affine:
  def __init__(self, string, alphabets_object, f_table_file=None):
    self.string = string #string is a list of alphabet objects to (en|de)crypt
#f_table_file = f_table_file if f_table_file else "f_table.json"
#self.f_table = json.loads( file(f_table_file).read() )

  def frequencies(self, corpus=None, alphabets=None):
    '''
    Frequencies are either predefined or estimated from a corpus.
    '''
    if(self.f_table != None):
      return self.f_table
    else:
      #get into corpus and generate an f_table and save it as a file f_table.json
      pass #for now !!!TODO!!!

  def encrypt(self, a, b):
    '''
    Encrypt string on the basis of give a,b,m
    y = (ax + b)%(m)
    '''
    a = alp_map()
    crypt = list()
    m = len(a)
    for alphabet in self.string:
      old = a.index(alphabet) + 1
      new = a(old)
      crypt.append(new)
    return crypt
