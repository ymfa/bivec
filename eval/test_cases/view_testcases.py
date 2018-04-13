
# coding: utf-8

# In[9]:


import json

simp_test=json.load(open('./simp_test.json', 'r'))
trad_test=json.load(open('./trad_test.json', 'r'))


# In[10]:


simp_test


# In[12]:


trad_test


# In[13]:


#store csv
import csv

with open('trad-test-cases.csv', 'w') as csvfile:
    fieldnames = ['orig_char', 'gold_char','char_index','line','gold','orig_line_num']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for key in trad_test:
        for line in trad_test[key]:
            line['orig_char']=key
            writer.writerow(line)

with open('simp-test-cases.csv', 'w') as csvfile:
    fieldnames = ['orig_char', 'gold_char','char_index','line','gold','orig_line_num']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for key in simp_test:
        for line in simp_test[key]:
            line['orig_char']=key
            writer.writerow(line)
           

