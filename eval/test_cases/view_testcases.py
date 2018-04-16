
# coding: utf-8

# In[1]:


import json

simp2multitrad_test=json.load(open('./simp2multitrad_test.json', 'r'))
trad2multisimp_test=json.load(open('./trad2multisimp_test.json', 'r'))


# In[2]:


#store csv
import csv
with open ('simp2multitrad_test_raw.txt', 'w') as f_txt:
    with open('simp2multitrad_test.csv', 'w') as csvfile:
        fieldnames = ['orig_char', 'gold_char','char_index','orig','gold','orig_line_num']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for key in simp2multitrad_test:
            for line in simp2multitrad_test[key]:
                line['gold_char']=key
                writer.writerow(line)
                f_txt.write(line['orig']+'\n')

with open('trad2multisimp_test.csv', 'w') as csvfile:
    fieldnames = ['orig_char', 'gold_char','char_index','orig','gold','orig_line_num']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for key in trad2multisimp_test:
        for line in trad2multisimp_test[key]:
            line['gold_char']=key
            writer.writerow(line)
           


# In[6]:


import pandas as pd
df1 = pd.read_csv("./simp2multitrad_test.csv")
df1

