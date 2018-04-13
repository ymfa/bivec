

import sys
import pickle
from collections import defaultdict
import json



trad_f=open(sys.argv[1])
sim_f=open(sys.argv[2])
#tra2simp_f=open('./tra2simp.json', 'w')
#simp2tra_f=open('./simp2tra.json','w')
tra2simp_f=open('./tra2simp', 'w')
simp2tra_f=open('./simp2tra','w')

tra2simp=defaultdict(lambda: defaultdict(int))
simp2tra=defaultdict(lambda: defaultdict(int))


current_tra_line=0
num=0
while current_tra_line!='':
    if num%1000000 ==0:
        print (num)
        print (tra2simp['的'])
        
    num+=1
    
    current_tra_line=trad_f.readline()
    current_simp_line=sim_f.readline()
    if len(current_tra_line)!=len(current_simp_line):
        print (current_tra_line)
        print (current_simp_line)
        continue
    else:
        for char_i in range(len(current_simp_line)):

            tra2simp[current_tra_line[char_i]][current_simp_line[char_i]]+=1
            simp2tra[current_simp_line[char_i]][current_tra_line[char_i]]+=1

pickle.dump(dict(tra2simp), tra2simp_f)
pickle.dump(dict(simp2tra), simp2tra_f)
#with open(dict(tra2simp), 'w') as outfile:
print (tra2simp['的'])

json.dump(dict(tra2simp), tra2simp_f)
json.dump(dict(simp2tra), simp2tra_f)

                         
tra2simp_f.close()
simp2tra_f.close()
trad_f.close()
sim_f.close()

                        
