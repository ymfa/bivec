

import sys
import pickle
from collections import defaultdict
import json
import logging

logging.basicConfig(filename='char_convert_stats.log',level=logging.DEBUG)


trad_f=open(sys.argv[1])
sim_f=open(sys.argv[2])
#tra2simp_f=open('./tra2simp.json', 'w')
#simp2tra_f=open('./simp2tra.json','w')
tra2simp_f=open('./tra2simp.json', 'w')
simp2tra_f=open('./simp2tra.json','w')

tra2simp=defaultdict(lambda: defaultdict(int))
simp2tra=defaultdict(lambda: defaultdict(int))


current_tra_line=0
num=0
while current_tra_line!='':
    if num%1000000 ==0:
        logging.debug ('processing {0}'.format(num))
        logging.debug (str(tra2simp['的']))
        
    num+=1
    
    current_tra_line=trad_f.readline()
    current_simp_line=sim_f.readline()
    if len(current_tra_line)!=len(current_simp_line):
        logging.warning ('uneual length of trad and simp lines. Line number', num)
        
        logging.warning (current_tra_line)
        logging.warning (current_simp_line)
        continue
    else:
        for char_i in range(len(current_simp_line)):

            tra2simp[current_tra_line[char_i]][current_simp_line[char_i]]+=1
            simp2tra[current_simp_line[char_i]][current_tra_line[char_i]]+=1

#with open(dict(tra2simp), 'w') as outfile:
logging.debug (tra2simp['的'])

json.dump(dict(tra2simp), tra2simp_f)
json.dump(dict(simp2tra), simp2tra_f)

                         
tra2simp_f.close()
simp2tra_f.close()
trad_f.close()
sim_f.close()

                        
