!/bin/bash
ssh root@114.115.130.106 "cd /data ; python gettopics.py" <<eeooff
exit
eeooff
# ~~~~~~~~~~~~
# >>> conda init >>>
__conda_setup="$(CONDA_REPORT_ERRORS=false '$HOME/anaconda3/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then    
	\eval "$__conda_setup"
else    
	if [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then        
		. "$HOME/anaconda3/etc/profile.d/conda.sh"        
		CONDA_CHANGEPS1=false conda activate base    
	else        
		\export PATH="$PATH:$HOME/anaconda3/bin"    
		fi
		fi
		unset __conda_setup
		# <<< conda init <<<
		# ~~~~~~~~~~~~

source activate tensorflow
echo "yep"
python get_file.py

ssh root@114.115.130.106 "cd /data ; python renew.py ; python similar.py" <<eeooff
exit
eeooff
