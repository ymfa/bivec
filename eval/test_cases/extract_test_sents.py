
# coding: utf-8

# In[5]:


import sys
import csv
import pandas as pd
from collections import defaultdict
import logging
import numpy as np

#logging.basicConfig(filename='eval.log',level=logging.DEBUG)
import logging
if sys.argv[0]=='/opt/conda/lib/python3.6/site-packages/ipykernel_launcher.py':
    prefix='sinica'
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('prefix is {0}'.format(prefix))
else:
    logging.basicConfig(filename='extract_test_case.log',level=logging.DEBUG)

    
    
    if len(sys.argv)<2:
        logging.warning('result and gold not specified. ')

    else:
        prefix=sys.argv[1]

gold=prefix+'_gold.csv'

gold_out=prefix+'_test'
logging.info ('gold csv is {0}'.format(gold))
logging.info ('out test file is {0}'.format(gold_out))



# In[18]:


gold_csv = pd.read_csv(gold)
lines=gold_csv['orig']
with open(gold_out, 'w') as f:
    for line in lines:
        f.write(line+'\n')

