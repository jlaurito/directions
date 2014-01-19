'''Directional Complexity Scraper
    
    created as part of a project on directional complexity

    1. loads zip list
    2. outputs several random sequences

'''



import urllib2
import json
from pandas import read_csv
import random
import csv


def add_leading_zero(v, length=5):
    '''adds leading zeros to make the output 'length' char long'''
    val = str(v)
    if len(val) >= length:
        return str(val)
    else:
        return add_leading_zero('0'+val, length)



'load zips'
zips = read_csv('../../data/standard_zips_lower_48.csv')



'creates requests based on several random sequences go through 5 times'
zips_random = []
for i in xrange(0,5):
    zips_random.extend(random.sample(zips['zip'], len(zips['zip'])))

for i, z in enumerate(zips_random):
    zips_random[i] = add_leading_zero(z)

outFile = open('../../data/rand_zip_seq.csv', 'wb')
w = csv.writer(outFile, dialect='excel')
w.writerow(zips_random)
