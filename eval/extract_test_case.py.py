
# coding: utf-8

# In[ ]:


import pickle
from collections import defaultdict
import json
#import simplejson as json


# In[ ]:


simp2trad=json.load(open('./simp2tra.json', 'r'))
tra2simp=json.load(open('./tra2simp.json', 'r'))


# In[ ]:


#only keep keys with multiple entries with each entry's count >100
simp2multitrad={}
trad2multisimp={}
for key in simp2trad:
    if len(simp2trad[key].keys())>1:
        temp_dict={}
        for tra_key in simp2trad[key]:
            if int(simp2trad[key][tra_key])>1000:
                temp_dict[tra_key]=simp2trad[key][tra_key]
        if len(temp_dict)>1:
            simp2multitrad[key]=dict(temp_dict)
for key in tra2simp:
    if len(tra2simp[key].keys())>1:
        temp_dict={}
        for simp_key in tra2simp[key]:
            if int(tra2simp[key][simp_key])>1000:
                temp_dict[simp_key]=tra2simp[key][simp_key]
        if len(temp_dict)>1:
            trad2multisimp[key]=dict(temp_dict)
        
#num of simplified characters with multiple traditional
print (len(simp2multitrad))
#num of tra characters with multiple simplified
print (len(trad2multisimp))

#compile multitrad tra characters
multitrad={}
multisimp={}
for chars in simp2multitrad.values():
    multitrad.update(chars)
for chars in trad2multisimp.values():
    multisimp.update(chars)




# In[ ]:


# process files to extract test cases, max 20 sentences per ambiguous charactesr


test_multitrad=defaultdict(list)
test_multisimp=defaultdict(list)
trad_lines=open('../corpora/trad_lines').readlines()
simp_lines=open('../corpora/simp_lines').readlines()
lines_num_trad=[]
lines_num_simp=[]


# In[16]:




line_num=0

for line in trad_lines:
        if len(lines_num_trad)==1470:
            break
            
        
        for char_i in range(len(line)):
            char=line[char_i]
            if char not in multitrad:
                continue
            else:
                if len(test_multitrad[char])<20:
                    test_multitrad[char].append({'char_index':char_i,'orig_line_num':line_num,'line':line,'gold':simp_lines[line_num]})
                    lines_num_trad.append(line_num)
        line_num+=1
        

    
line_num=0
for line in simp_lines:
        if len(lines_num_simp)==120:
            break
        for char_i in range(len(line)):
            char=line[char_i]
            if char not in multisimp:
                continue
            else:
                if len(test_multisimp[char])<20:
                    test_multisimp[char].append({'char_index':char_i,'orig_line_num':line_num,'line':line,'gold':trad_lines[line_num]})
                    lines_num_simp.append(line_num)
                    #print (char, line_num,line)
        line_num+=1



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

