
# coding: utf-8

# In[95]:



from collections import defaultdict
import json
import sys
import random

# simp2trad=sys.argv[1]
# tra2simp=sys.argv[2]
# trad_inf=sys.argv[3]
# simp_inf=sys.argv[4]
simp2trad='./simp2tra.json'
trad2simp='./tra2simp.json'
trad_inf='./data/trad_lines'
simp_inf='./data/simp_lines'
#import simplejson as json


# In[ ]:


simp2trad=json.load(open(simp2trad, 'r'))
tra2simp=json.load(open(trad2simp, 'r'))


# In[92]:


#only keep keys with multiple entries with each entry's count >1000
simp2multitrad={}
trad2multisimp={}
for key in simp2trad:
    if len(simp2trad[key].keys())>1: 
        temp_dict={}
        for tra_key in simp2trad[key]:
            if int(simp2trad[key][tra_key])>=1000:
                temp_dict[tra_key]=simp2trad[key][tra_key]
        if len(temp_dict)>1:
            simp2multitrad[key]=dict(temp_dict)
for key in tra2simp:
    if len(tra2simp[key].keys())>1:
        temp_dict={}
        for simp_key in tra2simp[key]:
            if int(tra2simp[key][simp_key])>=1000:
                temp_dict[simp_key]=tra2simp[key][simp_key]
        if len(temp_dict)>1:
            trad2multisimp[key]=dict(temp_dict)
        
#num of simplified characters with multiple traditional
print (len(simp2multitrad), 'simplified character types with multiple traditional chars aligned')
#num of tra characters with multiple simplified
print (len(trad2multisimp),'tra character types with multiple simplified chars aligned')

#compile multitrad tra characters
multitrad={}
multisimp={}
for chars in simp2multitrad.values():
    multitrad.update(chars)
for chars in trad2multisimp.values():
    multisimp.update(chars)

print (len(multisimp), 'ambigous simplified characters')
print (len(multitrad), 'ambigous traditional characters')


# In[62]:


# process files to extract test cases, max 20 sentences per ambiguous charactesr



trad_lines=open(trad_inf).readlines()
simp_lines=open(simp_inf).readlines()




# In[131]:


max_per_char=10000
simp_max=0
for key in multisimp:
    simp_max+=int(multisimp[key]/max_per_char)
    
trad_max=0
for key in multitrad:
    trad_max+=int(multitrad[key]/max_per_char)
print('{0} ambiguous trad char test cases'.format(trad_max), '{0} ambigous simp char test cases'.format(simp_max))


# In[ ]:


#generate a random list
ran_is=list(range(len(trad_lines)))
random.shuffle(ran_is)
print ('generate a random list')


# In[127]:


trad_testcases=0
simp_testcases=0
test_multitrad=defaultdict(list)
test_multisimp=defaultdict(list)

for ran_i in ran_is:
        
        if  trad_testcases>=trad_max and simp_testcases>=simp_max:
            break
        if trad_testcases<trad_max:
            

            #read traditional lines
            line=trad_lines[ran_i]

            for char_i in range(len(line)):
                char=line[char_i]
                if char not in multitrad:
                    continue
                else: 

                    if len(test_multitrad[char])< int(multitrad[char]/max_per_char):
                        test_multitrad[char].append({'char_index':char_i,'orig_line_num':ran_i,'line':line,'gold':simp_lines[line_num]})
                        trad_testcases+=1
        

        if simp_testcases<simp_max:
            #read simplified lines
            line=simp_lines[ran_i]

            for char_i in range(len(line)):
                char=line[char_i]
                if char not in multisimp:
                    continue
                else:
                    if len(test_multisimp[char])< int(multisimp[char]/max_per_char):
                        test_multisimp[char].append({'char_index':char_i,'orig_line_num':ran_i,'line':line,'gold':trad_lines[line_num]})
                        simp_testcases+=1

        


# In[129]:




for key in list(test_multisimp.keys()):
    if test_multisimp[key]==[]:
        test_multisimp.pop(key)
for key in list(test_multitrad.keys()):
    if test_multitrad[key]==[]:
        test_multitrad.pop(key)
print (len(test_multitrad), 'ambigous trad char types in the test cases')
print (len(test_multisimp), 'ambigous simp char types in the test cases')


# In[15]:


#store test cases

with open('trad_test.json','w') as f:
    json.dump(test_multitrad,f)
    
with open('simp_test.json', 'w') as f:
    json.dump(test_multisimp, f)


# In[13]:


#delete the test sentences from the corpus to form training dataset
line_nums=sorted(set(lines_num_trad+lines_num_simp),reverse=True)

with open('./data/trad_train', 'w') as f:
    for line_num in line_nums:
        del trad_lines[line_num]
    f.writelines(trad_lines)

with open('./data/simp_train', 'w') as f:
    for line_num in line_nums:
        del simp_lines[line_num]
    f.writelines(simp_lines)


# In[77]:


a=[1,2,3]
random.shuffle(a)
a


# In[85]:


a=random.shuffle(list(range(10)))
a

