# A script just to double check I'm right about the probability of randomly playing a grammatical order being 1/6

# Possible orders of 3 words, of which 1 noun (n), with 3 classes of adjective (1,2,3)
# n12 1n2 12n 
# n13 1n3 13n
# n21 2n1 21n
# n23 2n3 23n
# n31 3n1 31n
# n32 3n2 32n
# = 18
#
# Orders that are grammatical
# 12n 13n 23n
# = 3
#
# Probability of picking grammatical order at random = 3/18 = 1/6

# Alternatively, for a desired input, there are 3 words to enter, making 6 possible permutations
# only one of those is the correct order. Therefore probability is 1/6

import random

def is_grammatical(array):
    a = []
    adj1 = ["big", "small"]
    adj2 = ["empty", "filled"]
    adj3 = ["red", "blue", "green"]
    nouns = ["square","circle","triangle"]
    for word in array:
        if word in adj1:
            a.append(1)
        if word in adj2:
            a.append(2)
        if word in adj3:
            a.append(3)
        if word in nouns:
            a.append(4)
    return (a[0] < a[1] < a[2]) and has_noun(array)

def has_noun(array):
    nouns = ["square","circle","triangle"]
    for word in array:
        if word in nouns:
            return True
    return False

def generate():
    s = []
    a1, a2, a3, n = 0,0,0,0
    adj1 = ["big", "small"]
    adj2 = ["empty", "filled"]
    adj3 = ["red", "blue", "green"]
    nouns = ["square","circle","triangle"]
    while len(s) < 3:
        w = random.randint(0,3)
        if w == 0 and a1 < 1:
            s.append(adj1[random.randint(0,len(adj1)-1)])
            a1 += 1
        if w == 1 and a2 < 1:
            s.append(adj2[random.randint(0,len(adj2)-1)])
            a2 += 1
        if w == 2 and a3 < 1:
            s.append(adj3[random.randint(0,len(adj3)-1)])
            a3 += 1
        if w == 3 and n < 1:
            s.append(nouns[random.randint(0,len(nouns)-1)])
            n += 1
    if n == 1:
        return s
    return generate()
        
r = 1000000
g = 0
for i in range(r):
    s = generate()
    if is_grammatical(s):
        g += 1
print(g/r)