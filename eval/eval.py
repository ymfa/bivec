
# coding: utf-8

# In[1]:


import sys
import csv
import pandas as pd
from collections import defaultdict

if len(sys.argv)<5:
    print('result and gold not specified. Default is ./opencc/simp2multitrad_test_opencc_s2, gold is ./test_cases/simp2multitrad_test.csv')
    result='./opencc/simp2multitrad_test_opencc_s2tw'
    gold='./test_cases/simp2multitrad_test_gold.csv'
else:
    result=sys.argv[1]
    gold=sys.argv[2]
    print (result,gold)



# In[13]:


gold_csv = pd.read_csv(gold)
gold_dict=gold_csv.to_dict('records')
gold_dict[5520]


# In[3]:


multi_trad_official=set(list(gold_csv['gold_char']))
multi_trad_official


# In[12]:



trad2simp={}
line_num=0
num_incor=0
num_corr=0
accu_per_char=defaultdict(float)
num_per_char=defaultdict(float)
yitizi={'裡':'裏'}
print ('printing incorrect predictions')
print ('char_gold',':',"char_orig",":",'error_rate')
with open(result+'_error', 'w') as error_f:
    with open(result, 'r') as res_f:
        fieldnames = ['char_res','orig_char', 'gold_char','char_index','res','orig','gold','orig_line_num','line_num_in_gold']
        writer = csv.DictWriter(error_f, fieldnames=fieldnames)

        writer.writeheader()
        for line in res_f:
            line=line.strip()
            char_i=gold_csv['char_index'][line_num]
            char_gold=gold_csv['gold_char'][line_num]
            char_res=line[char_i]
            char_orig=gold_csv['orig_char'][line_num]
            trad2simp[char_gold]=char_orig
            num_per_char[char_gold]+=1


            if char_gold!=char_res:
                if char_res in yitizi:
                    if yitizi[char_res]==char_gold:
                        accu_per_char[char_gold]=accu_per_char[char_gold]
                else:
                    

                    gold_dict[line_num]['char_res']=char_res
                    gold_dict[line_num]['res']=line
                    gold_dict[line_num]['line_num_in_gold']=line_num
                    writer.writerow(gold_dict[line_num])
                    #print (char_gold,char_res,char_i,line_num,gold_csv['gold'][line_num])
                    num_incor+=1
                    accu_per_char[char_gold]+=1
            else:
                accu_per_char[char_gold]=accu_per_char[char_gold]
                num_corr+=1
            line_num+=1   
for key in accu_per_char:
    print (key, ': ', trad2simp[key],':',float(accu_per_char[key])/100)
print (num_incor, 'incorrect cases')
print(len(gold_csv))
print (float(num_incor/len(gold_csv)), 'incorrect. total 133000',)

