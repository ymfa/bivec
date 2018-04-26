Extract ldc data and sentence segmentation 

	In the directory of ldc file, run 

	python process_ldc_file.py ./ ../corpora/trad_lines 

	Output to trad_lines 

Run opencc 

	Git clone https://github.com/BYVoid/OpenCC.git 

	opencc -i trad_lines -o ../corpora/simp_lines -c ./OpenCC/data/config/tw2s.json 

Check if two lines have different number of chars and output tra2simp and simp2tra dictionaries 
	python3 char_convert_stats.py ../corpora/trad_lines ../corpora/simp_lines 

extract testcases 

	Python extract_test_case.py ./simp2tra.json ./tra2simp.json ./data/trad_lines ./data/simp_lines 
