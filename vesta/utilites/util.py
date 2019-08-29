import math
import os

PATH = os.getcwd()

def clearConsole():
    clear = lambda: os.system('cls')
    clear()

def cos(angle):
    x = math.radians(angle)
    return math.cos(x)

def sin(angle):
    x = math.radians(angle)
    return math.sin(x)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

# Numbers = enum('ZERO','ONE','TWO',THREE = 'three')
# print(Numbers.ONE)
# OUTPUT: 1
# print(Numbers.reverse_mapping['three'])
# OUTPUT THREE
