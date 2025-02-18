
# coding: utf-8

# In[13]:


from collections import defaultdict
import json
import sys
import random
import copy
import csv


import logging
if sys.argv[0]=='/opt/conda/lib/python3.6/site-packages/ipykernel_launcher.py':
    prefix='ldc'
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('prefix is {0}'.format(prefix))
else:
    logging.basicConfig(filename='extract_test_case.log',level=logging.DEBUG)

    
    
    if len(sys.argv)==2:
    #if len(sys.argv)==12:
        prefix=sys.argv[1]
    else: 
        print ('no argument or more arguments passed. Back to default prefix train')
        prefix='ldc'

        logging.warning('no arguments passed. Back to default prefix {0}'.format(prefix))
    
simp_ouf='../corpora/{0}.sc'.format(prefix)
simp2trad='./simp2tra.json'
trad2simp='./tra2simp.json'
trad_inf='./data/{0}.tc'.format(prefix)
simp_inf='./data/{0}.sc'.format(prefix)
trad_ouf='../corpora/{0}.tc'.format(prefix)
simp_ouf='../corpora/{0}.sc'.format(prefix)

#import simplejson as json


# In[11]:


simp2trad=json.load(open(simp2trad, 'r'))
tra2simp=json.load(open(trad2simp, 'r'))


# In[12]:


logging.info('reading in simp2trad and trad2simp. Only keep ambigous chars')
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
logging.debug ('{0} simplified character types with multiple traditional chars aligned'.format(len(simp2multitrad)))

#num of tra characters with multiple simplified
print (len(trad2multisimp),'tra character types with multiple simplified chars aligned')
logging.debug ('{0} tra character types with multiple simplified chars aligned'.format(len(trad2multisimp)))

#compile multitrad tra characters
multitrad={}
multisimp={}
for chars in simp2multitrad.values():
    multitrad.update(chars)
for chars in trad2multisimp.values():
    multisimp.update(chars)


print(len(multisimp), 'ambigous simplified character types')
print (len(multitrad), 'ambigous traditional character types')
logging.debug( '{0} ambigous simplified character types'.format(len(multisimp)))
logging.debug ( '{0} ambigous traditional character types'.format(len(multitrad)))


# In[18]:


#filter and extract test case characters
simp2trad_official_final=defaultdict(str)
multitrad_final=[]

logging.debug ('filtering the following chars which are <1000..')

print ('filtering the following chars...')
with open('./simp2multitrad_official.txt') as f:
    for line in f:
        line=line.strip()
        line=line.split('\t')
        simp_char=line[0]
        trad_chars=line[2].replace('～',line[0])
        #filter according to fre and outut
        trad_char_per_simp=''
        for trad_char in trad_chars:
            try:
                freq = simp2trad[simp_char][trad_char]
                if freq < 1000:
                    print(simp_char, trad_char)
                    logging.debug('{0} {1}'.format(simp_char, trad_char))
                else:
                    trad_char_per_simp += trad_char
            except KeyError:
                print(simp_char, trad_char, 'e')
                logging.warning('{0} {1} {2}'.format(simp_char, trad_char, 'e'))

        if len(trad_char_per_simp) > 1:
                simp2trad_official_final[simp_char]=trad_char_per_simp
                multitrad_final+=list(trad_char_per_simp)
print (len(simp2trad_official_final),'simp2trad_official_final test case simp char types')
logging.info ('{0} simp2trad_official_final test case simp char types'.format(len(simp2trad_official_final)))

if len(multitrad_final)!=len(set(multitrad_final)):
    print ('warning! the same traditional character can be mapped onto different simplified characters ')
    logging.warning('warning! the same traditional character can be mapped onto different simplified characters ')

    


# In[19]:


# show differences between simp2trad_offical and the corpus
logging.info('show differences between simp2trad_offical and the corpus')
for sim_char in simp2trad_official_final:
    
   simp2trad_lst= sorted(list(simp2multitrad[sim_char].keys()))
   simp2trad_official_lst=sorted(list(simp2trad_official_final[sim_char]))
   if simp2trad_official_lst!=simp2trad_lst:
        print(simp2multitrad[sim_char],simp2trad_official_final[sim_char])
        logging.debug('{0} {1} '.format(simp2multitrad[sim_char],simp2trad_official_final[sim_char]))


# In[20]:


# process files to extract test cases according to prob (1/10000 cases per char)

logging.info('read tradlines and simplines...')

trad_lines=open(trad_inf).readlines()
simp_lines=open(simp_inf).readlines()




# In[21]:


####extract a fixed number of chars
max_per_char=100
trad_max=max_per_char*len(multitrad_final)
simp_max=0
###extract according to probability
#max_per_char=10000
# simp_max=0
# for key in multisimp:
#     #simp_max+=int(multisimp[key]/max_per_char)
    
# trad_max=0
# for key in multitrad:
#     trad_max+=int(multitrad[key]/max_per_char)
print('aim to find {0} ambiguous trad char test cases'.format(trad_max), '{0} ambigous simp char test cases'.format(simp_max))
logging.info('{0},{1}'.format('aim to find {0} ambiguous trad char test cases'.format(trad_max), '{0} ambigous simp char test cases'.format(simp_max)))




# In[22]:


#generate a random list
ran_is=list(range(len(trad_lines)))
random.Random(1).shuffle(ran_is)

print ('generate a random list')
logging.info ('generate a random list')


# In[9]:


simp2trad_official_final


# In[23]:


logging.info('extracting test cases')

trad_testcases=[]
simp_testcases=[]
test_multitrad=defaultdict(list)
test_multisimp=defaultdict(list)
tra_line_matched=False

for ran_i in ran_is:
        
        if  len(trad_testcases)>=trad_max and len(simp_testcases)>=simp_max:
            print ('max reached')
            logging.info('max reached')
            break
        if len(trad_testcases)<trad_max:
            

            #read traditional lines
            line=trad_lines[ran_i]
            line=line.strip()
            for char_i in range(len(line)):
                char=line[char_i]
                if char not in multitrad_final:
                    continue
                else: 

                    #if len(test_multitrad[char])< int(multitrad[char]/max_per_char): 
                    if len(test_multitrad[char])<max_per_char:
                        test_char=simp_lines[ran_i].strip()[char_i]
                        if test_char not in simp2trad_official_final:
                            print ('test_char {0} (simp) for {1} (trad) not in simp2trad_official_final'.format(test_char, char))
                            logging.warning ('test_char {0} (simp) for {1} (trad) not in simp2trad_official_final'.format(test_char, char))

                        else:
                            test_multitrad[char].append({'char_index':char_i,'orig_line_num':ran_i,'gold':line, 'orig_char':test_char,'orig':simp_lines[ran_i].strip()})
                            trad_testcases.append(ran_i)
                            tra_line_matched=True
                            break #diversify the test cases. Once a sentence is matched, continue searching for later sents

        
        if tra_line_matched==True: #mdiversify the test cases
            tra_line_matched=False
            continue
            
            
        elif len(simp_testcases)<simp_max:
            #read simplified lines
            line=simp_lines[ran_i]

            for char_i in range(len(line)):
                char=line[char_i]
                if char not in multisimp:
                    continue
                else:
                    if len(test_multisimp[char])< int(multisimp[char]/max_per_char):
                        test_multisimp[char].append({'char_index':char_i,'orig_line_num':ran_i,'gold':line,'orig_char':trad_lines[ran_i][char_i],'orig':trad_lines[ran_i].strip()})
                        simp_testcases.append(ran_i)
                        break
        


# In[27]:




for key in list(test_multisimp.keys()):
    if test_multisimp[key]==[]:
        test_multisimp.pop(key)
for key in list(test_multitrad.keys()):
    if test_multitrad[key]==[]:
        test_multitrad.pop(key)
print (len(test_multitrad), 'ambigous trad char types in the test cases')
logging.info ( '{0} ambigous trad char types in the test cases'.format(len(test_multitrad)))

print (len(test_multisimp), 'ambigous simp char types in the test cases')
logging.info ( '{0} ambigous simp char types in the test cases'.format(len(test_multisimp),))


# In[36]:


#store test cases as csv and json
logging.info('storing the test cases')
with open ('../eval/test_cases/ldc_simp2trad_test', 'w') as f_txt:

    with open('../eval/test_cases/ldc_simp2trad_gold.csv', 'w') as csvfile:
        fieldnames = ['orig_char', 'gold_char','char_index','orig','gold','orig_line_num']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for key in test_multitrad:
            for line in test_multitrad[key]:
                line['gold_char']=key
                writer.writerow(line)
                f_txt.write(line['orig']+'\n')
# with open('trad2multisimp_test.csv', 'w') as csvfile:
#     fieldnames = ['orig_char', 'gold_char','char_index','orig','gold','orig_line_num']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
    
#     for key in trad2multisimp_test:
#         for line in trad2multisimp_test[key]:
#             line['gold_char']=key
#             writer.writerow(line)
# with open('../eval/test_cases/simp2multitrad_test.json','w') as f:
#     json.dump(test_multitrad,f)
    
# with open('../eval/test_cases/trad2multisimp_test.json', 'w') as f:
#     json.dump(test_multisimp, f)


# In[37]:


#delete the test sentences from the corpus to form training dataset
logging.info('deleting the test cases')
line_nums=set(trad_testcases+simp_testcases)
logging.debug ('{0} {1} {2} {3}'.format('trad lines orig',len(trad_lines),'simp_lines orig',len(simp_lines)))

line_no=0
with open(trad_ouf, 'w') as trad_f:
    with open (simp_ouf,'w') as simp_f:
        for line_num in range(len(trad_lines)):
            if line_num not in line_nums:
                trad_f.write(trad_lines[line_num])
                simp_f.write(simp_lines[line_num])
                line_no+=1
            else:
                
                pass
logging.debug ('{0} {1} {2} {3}'.format('trad lines',line_no,'simp_lines',line_no)) 

 

