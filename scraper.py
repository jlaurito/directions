'''Directional Complexity Scraper
    
    created as part of a project on directional complexity

    1. makes requests, with time delay of 35s in-between
    2. parses json results
'''



import urllib2
import json
import time
import csv


'load zips'
zips = []
with open('rand_zip_seq.csv') as zipfile:
    reader = csv.reader(zipfile, delimiter=',')
    for row in reader:
        zips.append(row)

zips = zips[0]



'find starting point & create request combos'
base = 'http://maps.googleapis.com/maps/api/directions/json'
trail= '&sensor=false&mode=driving&region=US' 

for i, z in enumerate(zips):
    if i > 0:
        if i % 10 == 0:
            start= []
            end  = []
            dist = []
            sloc = []
            eloc = []
            instr= []
            inputs = tuple(zips[i-10:i])
            param= '?origin=%s&waypoints=%s|%s|%s|%s|%s|%s|%s|%s&destination=%s' % inputs

            url = base + param + trail
            print url

            try:
                val = urllib2.urlopen(url).read()
            except urllib2.HTTPError:
                fr = open('failed_runs.csv','a')
                wr = csv.writer(fr)
                wr.writerow(list(inputs))
                fr.close()

            directions = json.loads(val)
            if directions['routes'] == []:
                fr = open('failed_runs.csv','a')
                wr = csv.writer(fr)
                wr.writerow(list(inputs))
                fr.close()
            else:


                for j in xrange(0,9):
                    step = directions['routes'][0]['legs'][j]

                    start.append(step['start_address'])
                    end.append(step['end_address'])
                    dist.append(step['distance']['value'])
                    sloc.append((step['start_location']['lat'],
                                 step['start_location']['lng']))
                    eloc.append((step['end_location']['lat'],
                                 step['end_location']['lng']))

                    cnt = 0
                    for turn in xrange(0,1000):
                        try: 
                            step['steps'][turn]
                            cnt +=1
                        except IndexError:
                            instr.append(cnt)
                            break

                for k in xrange(0,9):
                    out = [inputs[k], start[k], inputs[k+1], end[k], 
                           dist[k], sloc[k][0], sloc[k][1], eloc[k][0], 
                           eloc[k][1], instr[k]]
                    sr = open('success_runs.csv','a')
                    wr = csv.writer(sr)
                    wr.writerow(out)
                    sr.close()


            time.sleep(34)


