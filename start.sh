#run in docker: docker run -it --name simp2trad  -p 8888:8888 -v /home/ql261/simp2trad/:/home/simp2trad/ continuum/annoconda3 /bin/bash 
# add git config name
git config --global user.email "hey_flora@126.com"


# add packages and tensorflow eager in python startup
apt-get update
apt-get update && apt-get install procps
apt-get install vim
#export PYTHONSTARTUP='/home/context-embed/context-skipgram/PYTHONSTARTUP.py'





# run jupyter
cd /home/simp2trad/bivec
cp /home/simp2trad/bivec/jupyter_notebook_config.py /root/.jupyter/
for pid in $(ps -def | grep jupyter | awk '{print $2}'); do kill -9 $pid; done
export SHELL=/bin/bash
jupyter notebook --ip '*'  --port=8888 --allow-root &

