
# coding: utf-8

# In[1]:


import sys
sys.path.append("../../")
import logging
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity as cosine
import string
import pandas as pd
import re

# IO
logging.basicConfig(level=logging.DEBUG)

if sys.argv[0]=='/opt/conda/lib/python3.6/site-packages/ipykernel_launcher.py':
    tc_model='../../embeddings/out-5-50.3.de'
    outvec=1
    win_flag=1
    test_case_f='../test_cases/ldc_simp2trad_gold.csv'
    filter_nonhanzi=1

else:
    

    
    if len(sys.argv)<5:
        logging.warning('result and gold not specified!')
        logging.warning('python [tc_model] [outvec](0 or 1) [win_flag](0 or 1) [test_case_gold_f]')
        raise
    else:
        tc_model=sys.argv[1]
        outvec=sys.argv[2]
        win_flag=sys.argv[3]
        test_case_f=sys.argv[4]
        fiter_nonhanzi=sys.argv[5]
        
if int(outvec)==0:
    sc_model=tc_model[:-2]+'en'

elif int(outvec)==1:
    sc_model=tc_model[:-2]+'outvec.en'

model_base=sc_model.split('/')[-1]
winsize=int(model_base.split('.')[0].split('-')[1])
if int(filter_nonhanzi)==1:
    test_case_f_out='filter-{0}_{1}'.format(test_case_f.split('/')[-1].split('.')[0],model_base)
    def filter_char(s):
      non_hz = re.compile(r'[^\u3400-\u4DBF\u4E00-\u9FFF\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F\U0002B820-\U0002CEAF\U0002CEB0-\U0002EBEF\uF900-\uFAFF\U0002F800-\U0002FA1F]+')
      s=non_hz.sub('',s)
      return s
else:
    
    from make_data import filter_char

    test_case_f_out='{0}_{1}'.format(test_case_f.split('/')[-1].split('.')[0],model_base)

logging.info ('tc_we fname {0}, sc_we sc fname {1} and win flag is {2}'.format( tc_model,sc_model,win_flag))



# In[2]:


# process the we files

sc_vectors = KeyedVectors.load_word2vec_format(sc_model, binary=False)
tc_vectors = KeyedVectors.load_word2vec_format(tc_model, binary=False)





# In[12]:




def predict(win_size,win_flag,input_sent,position,tc_vectors,sc_vectors,candidates):
    before=filter_char(input_sent[0:position])
    after=filter_char(input_sent[position+1:len(input_sent)])
    input_sent=before+input_sent[position]+after
    position=len(before)

    if int(win_flag)==0: # use the whole sentence as context
        context=list(range(len(input_sent)))
    
    else:
        start=position-win_size
        end=position+win_size+1
        if start<=0:
            start=0
        if end>len(input_sent):
            end=len(input_sent)
        context=list(range(start,position))+list(range(position+1, end))
    
    score_dict={}
    #print (context)
    for candi in candidates:
        #print (candi)
        score_total=0
        num_contextw=0
        for context_i in context:
            
                context_w=input_sent[context_i]
                #print (context_w)
                try:
                    score=cosine([sc_vectors[context_w]],[tc_vectors[candi]])[0][0]
                    #print (score)
                except KeyError as e:
                        logging.warning (e)
                        
                        continue
                score_total+=score
                
                num_contextw+=1
        #print ('total',score_total,'num_contextw',num_contextw)
        try:
            score_dict[candi]=score_total/num_contextw
        except ZeroDivisionError as e:
            logging.warning(e)
            continue
    sort_key=sorted(score_dict.items(),key=lambda x:x[1], reverse=True)
    return '-'.join([str(res[0])+':'+str(res[1]) for res in sort_key])
#     res=sort_key[0][0]
#     #out_sent=input_sent[:position]+res+input_sent[position:len(input_sent)]
#     return sort_key
    
        
        


# In[4]:


#read in candidates
simp2trad_official='../../raw_data_process_cna_cmn/simp2multitrad_official.txt'

multi_trad_official={}
with open(simp2trad_official) as f:
    for line in f:
        line=line.strip()
        line=line.split('\t')
        simp_char=line[0]
        multi_trad_official[simp_char]=list(line[2].replace('～',line[0]))


# In[5]:


input_sent='aaa头发'
position=4
candidates=multi_trad_official[input_sent[position]]
predict(winsize,win_flag,input_sent,position,tc_vectors,sc_vectors,candidates)


# In[13]:


# output predictions

gold_csv = pd.read_csv(test_case_f)
gold_dict=gold_csv.to_dict('records')


# In[25]:


a=[(1,2),(3,4)]
'-'.join([str(res[0])+':'+str(res[1]) for res in a])


# In[14]:





with open(test_case_f_out, 'w') as f_o:
            #input_sent=filter_char(line.strip())
            for line in gold_dict:
                 
                 position=line['char_index']
                 candidates=multi_trad_official[line['orig_char']]
                 input_sent=line['orig']
                 res_char=predict(winsize,win_flag,input_sent,position,tc_vectors,sc_vectors,candidates)
                 
                 f_o.write(res_char+'\n')

