# this code cracks the affine cipher
import re
from ngram_score import ngram_score
fitness = ngram_score('quadgrams.txt') # load our quadgram statistics

# helper function, converts an integer 0-25 into a character
def i2a(i): return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i%26]

# decipher a piece of text using the affine cipher and a certain key    
def affine_decipher(text,a,b):
    inva = -1
    # determine the multiplicative inverse of a (mod 26)
    for i in range(1,26,2): 
        if (a*i) % 26 == 1: inva = i
    ret = ''
    for c in text:
        if c.isalpha(): ret += i2a(inva*(ord(c.upper()) - ord('A') - b))
        else: ret += c
    return ret

def break_affine(ctext):
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^A-Z]','',ctext.upper())
    # try all posiible keys, return the one with the highest fitness
    scores = []
    for i in [1,3,5,7,9,11,15,17,19,21,23,25]:
        scores.extend([(fitness.score(affine_decipher(ctext,i,j)),(i,j)) for j in range(0,25)])
    return max(scores)
    
# example ciphertext
ctext = 'QUVNLAUVILZKVZZZVNHIVQUFSFZHWZQLQHQLJSNLAUVI'
max_score, max_key = break_affine(ctext)

print 'best candidate with key (a,b) = '+str(max_key)+':'
print affine_decipher(ctext,*max_key)
