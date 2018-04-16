
# coding: utf-8

# In[116]:


import sys
import csv
import pandas as pd

if len(sys.argv)<5:
    print('result and gold not specified. Default is ./opencc/simp2multitrad_test_opencc_s2, gold is ./test_cases/simp2multitrad_test.csv')
    result='./opencc/simp2multitrad_test_opencc_s2t'
    gold='./test_cases/simp2multitrad_test_gold.csv'
else:
    result=sys.argv[1]
    gold=sys.argv[2]
    print (result,gold)



# In[117]:


gold_csv = pd.read_csv(gold)


# In[118]:




line_num=0
num_incor=0
num_corr=0
print ('printing incorrect predictions')
print ('char_gold','char_res')
with open(result, 'r') as res_f:
    
    for line in res_f:
        char_i=gold_csv['char_index'][line_num]
        char_gold=gold_csv['gold_char'][line_num]
        char_res=line[char_i]
        

        if char_gold!=char_res:
            print (char_gold,char_res,char_i,line_num,gold_csv['gold'][line_num])
            num_incor+=1
        else:
            num_corr+=1
        line_num+=1   
print (num_incor)
print (float(num_incor/len(gold_csv)), 'incorrect. total 133000',)

