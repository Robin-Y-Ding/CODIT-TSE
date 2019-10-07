import csv
import glob
import os


def PreSplit(result_file):
	'''
	This function is for scanning the csv file to find the split locations
	:return: lineno_split: This is a list containing the split locations
	'''
	r_file = open(result_file, 'r')
	lines = r_file.readlines()

	flag = ''
	lineno_split = list()
	for index, line in enumerate(lines):
		bug_id = line.split(',')[0]
		if bug_id != flag:
			flag = bug_id
			lineno_split.append(index)

	lineno_split.append(len(lines))
	return lineno_split


def SplitCsv(result_file, split_no):
	r_file = open(result_file, 'r')
	lines = r_file.readlines()


	for i in range(0, len(split_no) - 1):
		w_file_p = 'split_result/' + lines[split_no[i]].split(',')[0] + '_result.txt'
		w_file = open(w_file_p, 'w')
		for line in lines[split_no[i]:split_no[i + 1]]:
			w_file.write(line)
		w_file.close()



def OrderByProb(unordered_file):
	
	ordered_file = unordered_file.split('/')[-1].replace('result', 'ordered')
	ordered_file = 'split_result/' + ordered_file

	r_file = open(unordered_file, 'r')

	csvreader = csv.reader(r_file, delimiter=',')
	
	csv_w_file = open(ordered_file, 'w', newline='')
	
	#csv_writer = csv.writer(csv_w_file, delimiter=',')
	sorted_list = sorted(csvreader, key=lambda row: float(row[3])*float(row[4]), reverse=True)
	
	for l in sorted_list:
		csv_w_file.write(','.join(l) + "\n")
		
	csv_w_file.close()
	r_file.close()

	os.remove(unordered_file)


def OrderResults(pre_fix):
	text_files = pre_fix + '*.txt'
	fn_list = glob.glob(text_files)
	for fn in fn_list:
		file_path = fn.replace("\\", '/') #windows stuff, no worries for linux
		OrderByProb(file_path)


def ExtractPatchToken(pre_fix):
	text_files = pre_fix + '*.txt'
	fn_list = glob.glob(text_files)

	for fn in fn_list:
		result_file = fn.replace("\\", '/')
		
		patch_file = result_file.split('/')[-1].replace('ordered', 'patches')
		patch_file = 'tokenized_patches/' + patch_file
		r_f = open(result_file, 'r')
		w_f = open(patch_file, 'w')
		result_lines = r_f.readlines()
		
		for rl in result_lines:
			patch = rl[rl.find('<s>')+3:rl.find('</s>')].strip().replace('\t',' ')
			w_f.write(patch + '\n')
			
		r_f.close()
		w_f.close()


def ExtractPatchForEnsemble(pre_fix):
	text_files = pre_fix + '*.txt'
	fn_list = glob.glob(text_files)

	for fn in fn_list:
		result_file = fn.replace("\\", '/')
		
		patch_file = result_file.split('/')[-1].replace('ordered', 'patches')
		patch_file = 'tokenized_patches/' + patch_file
		r_f = open(result_file, 'r')
		w_f = open(patch_file, 'w')
		result_lines = r_f.readlines()
		
		for rl in result_lines:
			prob = rl.split(',')[4]
			patch = rl[rl.find('<s>')+3:rl.find('</s>')].strip().replace('\t',' ')
			patch = patch + '\t' + prob + '\n'
			w_f.write(patch)
			
		r_f.close()
		w_f.close()

