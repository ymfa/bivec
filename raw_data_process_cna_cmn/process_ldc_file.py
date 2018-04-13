import os
import sys
import re

root=sys.argv[1]
outfile=sys.argv[2]
outf=open(outfile,'w')
line_out=''
for root, dirs, files in os.walk(root):
    
     
    for file in files:
     if file.startswith('cna_cmn_'):
       print (file)
       num=0
       try:
        with open(file) as f:
         for line in f:
            #print (num)
            line=line.strip()
            if line.startswith('<') and line.endswith('>'):
               
               if line_out!='':
                   
                    sents=re.findall(r'[^！。？!?\n]+(?:[！。？!?\n])*', line_out)
                    
                    outf.writelines("%s\n" % l for l in sents)
               line_out=''
               continue
            else:
                
                #print (line)
                line_out+=line
                
        
         num+=1
       except:
        print (file) 
        print (num)
outf.close()
