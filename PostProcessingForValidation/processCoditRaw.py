import os
import glob
from shutil import copyfile

def processCodit():
	patchDict = dict()
	for i in range(75):
		buggyinfoFile = open(os.path.join(str(i), "info.txt"), 'r')
		buggyinfo = buggyinfoFile.readline()
		path = buggyinfo.split('\t')[0]
		bug = path.split('/')[2]
		bugid = bug.replace('_buggy', '').capitalize()
		os.mkdir(bugid)
		fileName = os.path.basename(path)
		if patchDict.get(bugid):
			print("Warning: bugid exists!")
		
		patchDict[bugid] = dict()
		patchDict[bugid]["fileName"] = fileName
		patchDict[bugid]["fileList"] = list()
		text_files = os.path.join(str(i), "*.patch")
		fn_list = glob.glob(text_files)
		for fn in fn_list:
			idx = fn.split(' ')[0].split('/')[-1]
			patchdir = os.path.join(bugid, idx)
			os.mkdir(patchdir)
			prob = float(fn.split(' ')[1].replace('.patch', ''))
			fl = [idx, prob, fn]
			patchDict[bugid]["fileList"].append(fl)
			patchWhole = os.path.join(patchdir, fileName)
			copyfile(fn, patchWhole)
			buggyFileName = bugid.lower() + '_buggy_' + fileName
			buggyWhole = os.path.join("FormattedBuggyFiles", buggyFileName)
			patchDiff = os.path.join(patchdir, "patch.diff")
			cmd = "git diff " + buggyWhole + ' ' + patchWhole + ' > ' + patchDiff
			os.system(cmd)


		

processCodit()