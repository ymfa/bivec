
# coding: utf-8

# In[57]:


import sys
import csv
import pandas as pd
from collections import defaultdict
import logging

#logging.basicConfig(filename='eval.log',level=logging.DEBUG)

if len(sys.argv)<3:
#if len(sys.argv)<5:
    result='./opencc/sinica_test_opencc_s2tw'
    gold='./test_cases/sinica_gold.csv'
    logging.warning('result and gold not specified. Default is {0}, gold is {1}'.format(result,gold))

else:
    result=sys.argv[1]
    gold=sys.argv[2]
    print ('result {0} and gold {1}'.format( result,gold))



# In[58]:


gold_csv = pd.read_csv(gold)
gold_dict=gold_csv.to_dict('records')


# In[56]:


gold_csv['gold']


# In[59]:


multi_trad_official=set(list(gold_csv['gold_char']))
multi_trad_official


# In[68]:


yitizi={'裡':'裏','裏':'裡'}#,'衚':'胡', '胡':'衚'}


# In[69]:



trad2simp={}
line_num=0
num_incor=0
accu_per_char=defaultdict(float)
num_per_char=defaultdict(float)

with open(result+'_error', 'w') as error_f:
  with open(result+'_score','w') as score_f:
    fieldnames_score=['char_gold',"char_orig",'error_rate']
    writer_score=csv.DictWriter(score_f,fieldnames=fieldnames_score)
    writer_score.writeheader()
    with open(result, 'r') as res_f:
        fieldnames = ['char_res','orig_char', 'gold_char','char_index','res','orig','gold','orig_line_num','line_num_in_gold']
        writer = csv.DictWriter(error_f, fieldnames=fieldnames)

        writer.writeheader()
        for line in res_f:
            #line=line.strip()
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
                    if char_res not in multi_trad_official:
                        logging.warning('{0} for {1} not in multi_trad_official. Might be yitizi'.format(char_res,char_gold))
                    gold_dict[line_num]['char_res']=char_res
                    gold_dict[line_num]['res']=line
                    gold_dict[line_num]['line_num_in_gold']=line_num
                    writer.writerow(gold_dict[line_num])
                    #print (char_gold,char_res,char_i,line_num,gold_csv['gold'][line_num])
                    num_incor+=1
                    accu_per_char[char_gold]+=1
            else:
                accu_per_char[char_gold]=accu_per_char[char_gold]
            line_num+=1 
            
with open(result+'_score','w') as score_f:
    fieldnames_score=['char_gold',"char_orig",'error_rate']
    writer_score=csv.DictWriter(score_f,fieldnames=fieldnames_score)
    writer_score.writeheader()
    for key in accu_per_char:
        writer_score.writerow ({'char_gold':key, 'char_orig': trad2simp[key],'error_rate':float(accu_per_char[key])/100})
    writer_score.writerow ({'char_gold':'average', 'char_orig': 'average','error_rate':float(num_incor/len(gold_csv))})
print (num_incor, 'incorrect cases')
print('of total {0}'.format(len(gold_csv)))
print ('error rate {0}'.format(float(num_incor/len(gold_csv))))

