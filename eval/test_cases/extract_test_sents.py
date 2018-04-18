
# coding: utf-8

# In[15]:


import sys
import csv
import pandas as pd
from collections import defaultdict
import logging
import numpy as np

#logging.basicConfig(filename='eval.log',level=logging.DEBUG)

if len(sys.argv)<2:
#if len(sys.argv)<5:
    gold_pre='./sinica'
    logging.warning('result and gold not specified')

else:
    gold_pre=sys.argv[1]

gold=gold_pre+'_gold.csv'

gold_out=gold_pre+'_test'
print ('gold csv is {0}'.format(gold))
print ('out test file is {0}'.format(gold_out))



# In[18]:


gold_csv = pd.read_csv(gold)
lines=gold_csv['orig']
with open(gold_out, 'w') as f:
    for line in lines:
        f.write(line+'\n')

