
# coding: utf-8

# In[2]:


import os
import sys
import re
from xml.etree import cElementTree as ET

import logging
if sys.argv[0]=='/opt/conda/lib/python3.6/site-packages/ipykernel_launcher.py':
    logging.basicConfig(level=logging.DEBUG)
    prefix='ldc'
    logging.debug('prefix is {0}'.format(prefix))
    root='./cna_cmn'
    trad_out='./{0}.tc'.format(prefix)
else:
    logging.basicConfig(filename='extract_test_case.log',level=logging.DEBUG)

    
if len(sys.argv)<3:
    logging.warning ('root outfile missing')
    root='./cna_cmn'
    trad_out='./ldc.tc'
    logging.warning ('switched to default. root={0}, trad_out={1}'.format(root,trad_out))

else:
    root=sys.argv[1]
    trad_out=sys.argv[2]+'.tc'


# In[18]:


def process_sent(sent,seg=False):
    sent_out=[]
    sent=sent.strip()
    
    sent=sent.replace('\n','')
    if seg==True:
        sent_list=re.findall(r'[^！。？!?\n]+(?:[！。？!?\n])*', sent)
    else:
        sent_list=[sent]
    sent_out=["%s\n" % l for l in sent_list]
    return sent_out

def parse_single_xml(xml_f,outf):
    seg=True
    tree = ET.parse(xml_f)
    root = tree.getroot()
    for DOC in root:

         if DOC.attrib['type'] in ['multi','story']:
            for child in DOC:
                if child.tag not in ['HEADLINE','TEXT']:
                    continue
                lines=[]
                if child.tag =='HEADLINE':
                    if child.text!='':
                        lines+=process_sent(child.text)
                elif child.tag=='TEXT':
                     TEXT=child
                     
                     if len(TEXT)>0:
                            for p in TEXT:
                                if p.text!='':
                                    lines+= process_sent(p.text,seg)
                     else:
                        if TEXT.text!='':
                            lines+=process_sent(TEXT.text,seg)
                if lines!=[]:
                    outf.writelines(lines)
        


# In[20]:



with open(trad_out,'w') as outf:
        for rt, dirs, files in os.walk(root):


            for file in files:
                 if file.startswith('cna_cmn'):
                    filepath=root+'/'+file
                    print (filepath)
                    parse_single_xml(filepath,outf)


# In[ ]:





# line_out=''
# for root, dirs, files in os.walk(root):
    
     
#     for file in files:
#      if file.startswith('cna_cmn_'):
#        print (file)
#        num=0
#        try:
#         with open(file) as f:
#          for line in f:
#             #print (num)
#             line=line.strip()
#             if line.startswith('<') and line.endswith('>'):
               
#                if line_out!='':
                   
#                     sents=re.findall(r'[^！。？!?\n]+(?:[！。？!?\n])*', line_out)
                    
#                     outf.writelines("%s\n" % l for l in sents)
#                line_out=''
#                continue
#             else:
                
#                 #print (line)
#                 line_out+=line
                
        
#          num+=1
#        except:
#         print (file) 
#         print (num)
# outf.close()

