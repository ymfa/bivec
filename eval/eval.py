
# coding: utf-8

# In[2]:


import sys
import csv
import pandas as pd
from collections import defaultdict
import logging

simp2trad_official='../raw_data_process_cna_cmn/simp2multitrad_official.txt'
if sys.argv[0]=='/opt/conda/lib/python3.6/site-packages/ipykernel_launcher.py':
    result='./opencc/sinica_test_opencc_s2tw'
    gold='./test_cases/sinica_gold.csv'
    logging.basicConfig(level=logging.DEBUG)
    logging.info ('result {0} and gold {1}'.format( result,gold))
else:
    logging.basicConfig(filename='extract_test_case.log',level=logging.DEBUG)

    
    if len(sys.argv)<3:
        #result='./opencc/sinica_test_opencc_s2tw'
        #gold='./test_cases/sinica_gold.csv'
        logging.warning('result and gold not specified!')
        raise
    else:
        result=sys.argv[1]
        gold=sys.argv[2]
        print ('result {0} and gold {1}'.format( result,gold))



# In[2]:


gold_csv = pd.read_csv(gold)
gold_dict=gold_csv.to_dict('records')


# In[3]:


multi_trad_official=[]
with open(simp2trad_official) as f:
    for line in f:
        line=line.strip()
        line=line.split('\t')
        simp_char=line[0]
        trad_chars=list(line[2].replace('～',line[0]))
        multi_trad_official+=trad_chars


# In[4]:


yitizi={'裡':'裏','裏':'裡','衚':'胡', '胡':'衚'}


# In[5]:



trad2simp={}
line_num=0
num_incor=0
error_per_char=defaultdict(int)
num_per_char=defaultdict(int)

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
            line=line.rstrip()
            char_i=gold_csv['char_index'][line_num]
            char_gold=gold_csv['gold_char'][line_num]
            char_res=line[char_i]
            char_orig=gold_csv['orig_char'][line_num]
            trad2simp[char_gold]=char_orig
            num_per_char[char_gold]+=1


            if char_gold!=char_res:
                
                if char_res in yitizi:
                    
                    if yitizi[char_res]==char_gold:
                        
                        error_per_char[char_gold]=error_per_char[char_gold]
                
                else:
                    if char_res not in multi_trad_official:
                        logging.warning('{0} for {1} not in multi_trad_official. Might be yitizi'.format(char_res,char_gold))
                    gold_dict[line_num]['char_res']=char_res
                    gold_dict[line_num]['res']=line
                    gold_dict[line_num]['line_num_in_gold']=line_num
                    writer.writerow(gold_dict[line_num])
                    num_incor+=1
                    error_per_char[char_gold]+=1
            else:
                error_per_char[char_gold]=error_per_char[char_gold]
            line_num+=1 
            
with open(result+'_score','w') as score_f:
    fieldnames_score=['char_gold',"char_orig",'error_num','total']
    writer_score=csv.DictWriter(score_f,fieldnames=fieldnames_score)
    writer_score.writeheader()
    for key in error_per_char:
        writer_score.writerow ({'char_gold':key, 'char_orig': trad2simp[key],'error_num':int(error_per_char[key]), 'total':num_per_char[key]})
    writer_score.writerow ({'char_gold':'total', 'char_orig': 'total','error_num':num_incor, 'total':len(gold_dict)})

print (num_incor, 'incorrect cases')
print('of total {0}'.format(len(gold_csv)))
print ('error rate {0}'.format(float(num_incor/len(gold_dict))))

