import sys
import os
import subprocess
import glob
import re


def	GenPatches(patch_dir, N):
	text_files = 'split_result/*.txt'
	fn_list = sorted(glob.glob(text_files))
	bug_id_list = list()
	resultFile = open('resultsTokenOnly.txt', 'w')
	for fn in fn_list:
		bug_id = os.path.basename(fn).replace('_ordered.txt', '')	
		base_dir = os.path.join(patch_dir, bug_id)
		proj = bug_id.split('_')[0]
		id = bug_id.split('_')[1]
		os.makedirs(base_dir)
		SinglePatch(proj, id, bug_id, N, base_dir, resultFile)
	resultFile.close()


def SinglePatch(proj, bug_id, full_id, N, base_dir, resultFile):
	bug_info_list = ExtractInfo(proj, bug_id, N)
	for index, bug_info in enumerate(bug_info_list):
		#buggy_file_lines = open(bug_info[0], "r", encoding='iso-8859-1').readlines()
		buggy_file_lines = open(bug_info[0], "r").readlines()
		buggy_line_number = int(bug_info[1])
		buggy_line = buggy_file_lines[buggy_line_number-1]
		prediction, prob = bug_info[2].split('\t')
		if prediction.find('"str"') != -1:
			prediction = ReplaceStr(buggy_line, prediction)
		white_space_before_buggy_line = buggy_line[0:buggy_line.find(buggy_line.lstrip())]
		o_f = os.path.join(base_dir, str(index+1), os.path.basename(bug_info[0]))
		os.makedirs(os.path.dirname(o_f))
		#output_file = open(o_f, "w", encoding='iso-8859-1')
		output_file = open(o_f, "w")
		for j in range(len(buggy_file_lines)):
			if(j+1 == buggy_line_number):
				output_file.write(white_space_before_buggy_line+prediction)
			else:
				output_file.write(buggy_file_lines[j])
		output_file.close()
		cwd = os.getcwd()
		o_f = os.path.join(cwd, o_f)
		result = full_id + ',' + o_f + ',' + prob
		resultFile.write(result)
		'''
		diff_file = os.path.join(base_dir, str(index+1), "patch.diff")
		cmd = "git diff " + bug_info[0] + ' ' + o_f + ' > ' + diff_file
		os.system(cmd)
		'''


def ExtractInfo(proj, id, N):
	bug_info_list = list()
	
	info_file = 'split_result/' + proj + '_' + id + '_ordered.txt'
	patch_file = 'JavaSource_patches/' + proj + '_' + id + '_patches_JavaSource.txt'
	i_f = open(info_file, 'r')
	p_f = open(patch_file, 'r')
	info_lines = i_f.readlines()
	patch_lines = p_f.readlines()
	
	for i in range(0,min(int(N), len(patch_lines))):
		# bug_info: [file_loc, line_no, patch]
		bug_info = list()
		bug_info = [info_lines[i].split(',')[1], info_lines[i].split(',')[2], patch_lines[i]]
		bug_info_list.append(bug_info)
	
	i_f.close()
	p_f.close()
	
	return bug_info_list


def ReplaceStr(buggy, patch):
	str_list = re.findall(r"(\'.*\')|(\".*\")", buggy)

	nostr_patch = None
	if len(str_list) > 0:		
		for s_l in str_list:
			if nostr_patch is None:
				nostr_patch = patch
			nostr_patch = nostr_patch.replace('"str"', s_l[0] if s_l[0] != '' else s_l[1], 1)

		nostr_patch = nostr_patch.replace('"str"', str_list[-1][0] if str_list[-1][0] != '' else str_list[-1][1])
	else:
		nostr_patch = patch
	return nostr_patch
	