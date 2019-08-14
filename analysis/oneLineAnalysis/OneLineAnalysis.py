import subprocess
import json
import os
import sys
import re
import glob
import statistics


def readProj():
	small = open('bugs.json','r')

	smallData = json.load(small)

	ProjDir = "/home/robin/Documents/projects"
	if not os.path.isdir(ProjDir):
		print ("Error projects!")
		return

	projs = list()

	for idx, sd in enumerate(smallData):
		projectName = sd["projectName"]
		projs.append(projectName)
		
	projs = set(projs)
	#finalReport = open('finalReport.txt', 'w')
	finalReport = open('finalReportAll.txt', 'w')

	totalOneRepCnt = 0
	totalCnt = 0

	for proj in projs:
		p = proj.split('.')[-1]
		

		bugProj = os.path.join(ProjDir, p)
		if not os.path.isdir(bugProj):
			print ("No such project: " + p)
			continue

		finalReport.write("----------------------\n")
		finalReport.write("Project: " + p + '\n')

		resultDir = os.path.join("/home/robin/Documents/dataset-analysis/results", p)
		if not os.path.isdir(resultDir):
			print ("Error results!")
			return

		statsFile = open(os.path.join(resultDir, "stats.txt"), 'r', encoding="ISO-8859-1")
		statsString = statsFile.read()
		oneReplaceCnt = statsString.count("| 2 +-\n 1 file changed, 1 insertion(+), 1 deletion(-)\n")
		oneInsertCnt = statsString.count(" 1 file changed, 1 insertion(+)\n")
		oneDeleteCnt = statsString.count(" 1 file changed, 1 deletion(-)\n")

		oneLineChange = oneReplaceCnt + oneInsertCnt + oneDeleteCnt
		
		totalOneRepCnt = totalOneRepCnt + oneLineChange
		
		finalReport.write("Count of commits that only contains one line replacement: " + str(oneReplaceCnt) + '\n')
		finalReport.write("Count of commits that only contains one line insertion: " + str(oneInsertCnt) + '\n')
		finalReport.write("Count of commits that only contains one line deletion: " + str(oneDeleteCnt) + '\n')
		finalReport.write("Count of commits that contains one line change: " + str(oneLineChange) + '\n')

		cmd = ""
		cmd += "cd " + bugProj + ";"
		cmd = cmd + "git rev-list --count HEAD"
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
		result = result.stdout.decode('utf-8').strip()

		totalCnt = totalCnt + int(result)
		
		finalReport.write("Count of commits: " + result + '\n')

		pct = 100 * oneLineChange / int(result)
		finalReport.write("Percentage of one line replacement: " + str(pct) + '%' + '\n')

	finalReport.write("----------------------------------\n----------------------------------\n")
	finalReport.write("Total one line replacement count: " + str(totalOneRepCnt) + '\n')
	finalReport.write("Count of commits: " + str(totalCnt) + '\n')
	totalPct = 100 * totalOneRepCnt / totalCnt
	finalReport.write("Overall percentage of one line replacement: " + str(totalPct) + '%' + '\n')

	small.close()
	finalReport.close()


def readProjJavaOnly():
	small = open('bugs.json','r')

	smallData = json.load(small)

	ProjDir = "/home/robin/Documents/projects"
	if not os.path.isdir(ProjDir):
		print ("Error projects!")
		return

	projs = list()

	for idx, sd in enumerate(smallData):
		projectName = sd["projectName"]
		projs.append(projectName)
		
	projs = set(projs)
	finalReport = open('finalReportJavaOnlyAll.txt', 'w')

	totalOneRepCnt = 0
	totalCnt = 0

	for proj in projs:
		p = proj.split('.')[-1]
		

		bugProj = os.path.join(ProjDir, p)
		if not os.path.isdir(bugProj):
			print ("No such project: " + p)
			continue

		finalReport.write("----------------------\n")
		finalReport.write("Project: " + p + '\n')

		resultDir = os.path.join("/home/robin/Documents/dataset-analysis/results", p)
		if not os.path.isdir(resultDir):
			print ("Error results!")
			return

		statsFile = open(os.path.join(resultDir, "java_stats.txt"), 'r', encoding="ISO-8859-1")
		statsString = statsFile.read()
		oneReplaceCnt = statsString.count("| 2 +-\n 1 file changed, 1 insertion(+), 1 deletion(-)\n")
		oneInsertCnt = statsString.count(" 1 file changed, 1 insertion(+)\n")
		oneDeleteCnt = statsString.count(" 1 file changed, 1 deletion(-)\n")

		oneLineChange = oneReplaceCnt + oneInsertCnt + oneDeleteCnt
		
		totalOneRepCnt = totalOneRepCnt + oneLineChange
		
		finalReport.write("Count of commits that only contains one line replacement: " + str(oneReplaceCnt) + '\n')
		finalReport.write("Count of commits that only contains one line insertion: " + str(oneInsertCnt) + '\n')
		finalReport.write("Count of commits that only contains one line deletion: " + str(oneDeleteCnt) + '\n')
		finalReport.write("Count of commits that contains one line change: " + str(oneLineChange) + '\n')

		result = statsString.count("Author: ")
		result = str(result)

		totalCnt = totalCnt + int(result)
		
		finalReport.write("Count of commits: " + result + '\n')

		pct = 100 * oneLineChange / int(result)
		finalReport.write("Percentage of one line replacement: " + str(pct) + '%' + '\n')

	finalReport.write("----------------------------------\n----------------------------------\n")
	finalReport.write("Total one line replacement count: " + str(totalOneRepCnt) + '\n')
	finalReport.write("Count of commits: " + str(totalCnt) + '\n')
	totalPct = 100 * totalOneRepCnt / totalCnt
	finalReport.write("Overall percentage of one line replacement: " + str(totalPct) + '%' + '\n')

	small.close()
	finalReport.close()
	

def genProjectsList():
	small = open('bugs.json','r')
	projList = open("ProjList.txt", 'w')
	smallData = json.load(small)
	projs = list()

	for sd in smallData:
		projectName = sd["projectName"]
		projs.append(projectName)
		
	projs = set(projs)

	for proj in projs:
		p = proj.replace('.','/')
		projList.write(p + '\n')


def mergeCSV():
	csvFiles = 'ChangeSummary/*.csv'
	fnList = glob.glob(csvFiles)
	merged = open("ChangeSummary.csv", 'w')
	for fn in fnList:
		f = open(fn, 'r')
		content = f.read().replace("project,sha,author,author_email,commit_date,is_bug\n", '')
		merged.write(content)
		f.close()


def allChangeAnalysis():
	statBase = '/home/robin/Documents/allchangestat'
	numStatBase = '/home/robin/Documents/allchangenumstat'
	projBase = 'projects'
	projList = open('ProjList.txt', 'r')
	projs = projList.readlines()
	for proj in projs:
		proj = proj.strip().replace('/', "\\'__\\'")
		projStat = proj.strip().replace('/', "\\'__\\'") + '_stat.txt'
		projNumStat = proj.strip().replace('/', "\\'__\\'") + '_numstat.txt'
		cmd = ''
		cmd += "cd " + os.path.join(projBase, proj) + ';'
		cmd += "git log --stat --follow *.java > " + os.path.join(statBase, projStat) + ';'
		#print (cmd)
		cmd += "git log --numstat --follow *.java > " + os.path.join(numStatBase, projNumStat) + ';'
		subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)



def bugFixAnalysis():
	csvFiles = 'Top100BuggyChangeSummary/*.csv'
	fnList = glob.glob(csvFiles)

	for fn in fnList:
		changeSum = open(fn, 'r')
		#changeSum = open('Top100BuggyChangeSummary.csv', 'r')
		#bugFixCommitsStat = open('BugFixCommitsStats.txt', 'w')
		#bugFixCommitsNumstat = open('BugFixCommitsNumstats.txt', 'w')
		projectsBase = "projects/"
		bugStatBase = "bugfixstat/"
		bugNumStatBase = "bugfixnumstat/"
		commits = changeSum.readlines()
		cnt = 0

		stat = open(os.path.join(bugStatBase, os.path.basename(fn).replace("ChangeSummary.csv", "Stats.txt")), 'w')
		numstat = open(os.path.join(bugNumStatBase, os.path.basename(fn).replace("ChangeSummary.csv", "NumStats.txt")), 'w')
		for c in commits:
			proj, sha, author, email, date, bugFix = c.strip().replace("'", "").split(',')
			proj = proj.replace('"', "\\'")

			if bugFix == 'True':
				projPath = os.path.join(projectsBase, proj)
				#print(projPath)
				cmd = ''
				cmd = cmd + "cd " + projPath + ";"
				cmd = cmd + "git show --stat " + sha
				result1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
				result1 = result1.stdout.decode('utf-8')
				stat.write(result1)

				cmd = ''
				cmd = cmd + "cd " + projPath + ";"
				cmd = cmd + "git show --numstat " + sha
				result2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
				result2 = result2.stdout.decode('utf-8')
				numstat.write(result2)

				cnt += 1

		print(proj + "--->>>" + "Total bug fix commits: " + str(cnt))
		stat.close()
		numstat.close()


#TODO: If open-source, do refactoring --> Design Class to implement these.

def countAllChange():
	#countReport = open('AllChangeReport.txt', 'w')
	totalMod = 0
	totalOnelineMod = 0
	ratioList = list()
	allChange = dict()

	fs = 'allchangestat/*.txt'
	fnList = glob.glob(fs)
	details = dict()
	for fn in fnList:
		projDetail = dict()
		bugFixCommitsStat = open(fn, 'r', encoding="ISO-8859-1")
		bugFixCommitsNumstat = open(os.path.join("allchangenumstat", os.path.basename(fn).replace("stat.txt", "numstat.txt")), 'r', encoding="ISO-8859-1")

		projName = os.path.basename(fn).replace("_stat.txt", "").replace("'__'",'/')
		#countReport.write("---------------------------\n")
		#countReport.write("Project: " + projName + '\n')
		projDetail["projName"] = projName
		Stat = bugFixCommitsStat.readlines()
		Numstat = bugFixCommitsNumstat.read()

		modFile = 0
		for l in Stat:
			#if "file changed, " in l or "files changed, " in l:
			x = re.findall("\s[0-9]+\sfiles?\schanged,\s", l)
			if (x):
				m = int(x[0].split(' ')[1])
				modFile = modFile + m

		#countReport.write("Modified files: " + str(modFile) + '\n')
		projDetail["modFile"] = modFile
		totalMod += modFile

		#y = len(re.findall("commit\s[a-zA-Z0-9]+\nAuthor:\s", Numstat))
		#print(y)

		rep = Numstat.count("\n1\t1\t")
		dele = Numstat.count("\n1\t0\t")
		inst = Numstat.count("\n0\t1\t")

		modif = rep + dele + inst
		ratio = modif * 100 / modFile
		ratioList.append(ratio)
		#countReport.write("One-line modifed files: " + str(modif) + '\n')
		projDetail["modif"] = modif
		#countReport.write("Ratio of one line modifcation: " + str(ratio) + ' %' + '\n')
		projDetail["ratio"] = ratio
		totalOnelineMod += modif
		details[projName] = projDetail
		bugFixCommitsStat.close()
		bugFixCommitsNumstat.close()
		#print(modif)

	#countReport.write("\n\n<<<<<<<<<<<<<<<<<<<<Total>>>>>>>>>>>>>>>>>>\n")
	allChange["details"] = details
	ratioMedian = statistics.median(ratioList)
	ratioMax = max(ratioList)
	#countReport.write("Total modified files: " + str(totalMod) + '\n')
	allChange["totalMod"] = totalMod
	#countReport.write("Total one line modified files: " + str(totalOnelineMod) + '\n')
	allChange["totalOnelineMod"] = totalOnelineMod
	#countReport.write("Maximum ratio of one line modification: " + str(ratioMax) + ' %' + '\n')
	allChange["ratioMax"] = ratioMax
	#countReport.write("Median ratio of one line modification: " + str(ratioMedian) + ' %' + '\n')
	allChange["ratioMedian"] = ratioMedian
	#countReport.write("Average ratio of one line modification: " + str(totalOnelineMod * 100 / totalMod) + ' %' + '\n')
	allChange["ratioAvg"] = totalOnelineMod * 100 / totalMod
	#countReport.close()
	return allChange


def countBugFix():
	#bugCountReport = open('BugFixReport.txt', 'w')
	totalMod = 0
	totalOnelineMod = 0
	ratioList = list()
	bugFix = dict()

	fs = 'bugfixstat/*.txt'
	fnList = glob.glob(fs)
	details = dict()
	for fn in fnList:
		projDetail = dict()
		bugFixCommitsStat = open(fn, 'r')
		bugFixCommitsNumstat = open(os.path.join("bugfixnumstat", os.path.basename(fn).replace("Stats.txt", "NumStats.txt")), 'r')

		projName = os.path.basename(fn).replace("Stats.txt", "").replace("'__'",'/')
		#countReport.write("---------------------------\n")
		#countReport.write("Project: " + projName + '\n')
		projDetail["projName"] = projName
		Stat = bugFixCommitsStat.readlines()
		Numstat = bugFixCommitsNumstat.read()

		modFile = 0
		for l in Stat:
			#if "file changed, " in l or "files changed, " in l:
			x = re.findall("\s[0-9]+\sfiles?\schanged,\s", l)
			if (x):
				m = int(x[0].split(' ')[1])
				modFile = modFile + m

		#countReport.write("Modified files: " + str(modFile) + '\n')
		projDetail["modFile"] = modFile
		totalMod += modFile

		#y = len(re.findall("commit\s[a-zA-Z0-9]+\nAuthor:\s", Numstat))
		#print(y)

		rep = Numstat.count("\n1\t1\t")
		dele = Numstat.count("\n1\t0\t")
		inst = Numstat.count("\n0\t1\t")

		modif = rep + dele + inst
		ratio = modif * 100 / modFile
		ratioList.append(ratio)
		#countReport.write("One-line modifed files: " + str(modif) + '\n')
		projDetail["modif"] = modif
		#countReport.write("Ratio of one line modifcation: " + str(ratio) + ' %' + '\n')
		projDetail["ratio"] = ratio
		totalOnelineMod += modif
		details[projName] = projDetail
		bugFixCommitsStat.close()
		bugFixCommitsNumstat.close()
		#print(modif)

	#countReport.write("\n\n<<<<<<<<<<<<<<<<<<<<Total>>>>>>>>>>>>>>>>>>\n")
	bugFix["details"] = details
	ratioMedian = statistics.median(ratioList)
	ratioMax = max(ratioList)
	#countReport.write("Total modified files: " + str(totalMod) + '\n')
	bugFix["totalMod"] = totalMod
	#countReport.write("Total one line modified files: " + str(totalOnelineMod) + '\n')
	bugFix["totalOnelineMod"] = totalOnelineMod
	#countReport.write("Maximum ratio of one line modification: " + str(ratioMax) + ' %' + '\n')
	bugFix["ratioMax"] = ratioMax
	#countReport.write("Median ratio of one line modification: " + str(ratioMedian) + ' %' + '\n')
	bugFix["ratioMedian"] = ratioMedian
	#countReport.write("Average ratio of one line modification: " + str(totalOnelineMod * 100 / totalMod) + ' %' + '\n')
	bugFix["ratioAvg"] = totalOnelineMod * 100 / totalMod
	#countReport.close()
	return bugFix


def countFiles():
	allChange = countAllChange()
	bugFix = countBugFix()
	countReport = open("FinalReport.txt", 'w')

	projList = open("ProjList.txt",'r')
	projs = projList.readlines()
	for proj in projs:
		proj = proj.strip()

		countReport.write("---------------------------\n")
		countReport.write("Project: " + proj + '\n\n')

		countReport.write("All Change modified files: " + str(allChange["details"][proj]["modFile"]) + '\n')
		countReport.write("All Change one-line modified files: " + str(allChange["details"][proj]["modif"]) + '\n')
		countReport.write("All Change ratio of one-line modifcation: " + str(allChange["details"][proj]["ratio"]) + '%' + '\n')
		countReport.write('\n')

		countReport.write("Bug Fix modified files: " + str(bugFix["details"][proj]["modFile"]) + '\n')
		countReport.write("Bug Fix one-line modified files: " + str(bugFix["details"][proj]["modif"]) + '\n')
		countReport.write("Bug Fix ratio of one-line modifcation: " + str(bugFix["details"][proj]["ratio"]) + '%' + '\n')
	

	countReport.write("\n\n-----------------------Total--------------------")
	countReport.write("\n\n<<<<<<<<<<<<<<<<<<<<<Bug Fix>>>>>>>>>>>>>>>>>>>>\n")
	countReport.write("Total modified files: " + str(bugFix["totalMod"]) + '\n')
	countReport.write("Total one line modified files: " + str(bugFix["totalOnelineMod"]) + '\n')
	countReport.write("Maximum ratio of one line modification: " + str(bugFix["ratioMax"]) + ' %' + '\n')
	countReport.write("Median ratio of one line modification: " + str(bugFix["ratioMedian"]) + ' %' + '\n')
	countReport.write("Average ratio of one line modification: " + str(bugFix["ratioAvg"]) + ' %' + '\n')

	countReport.write("\n\n<<<<<<<<<<<<<<<<<<<<All Change>>>>>>>>>>>>>>>>>>\n")
	countReport.write("Total modified files: " + str(allChange["totalMod"]) + '\n')
	countReport.write("Total one line modified files: " + str(allChange["totalOnelineMod"]) + '\n')
	countReport.write("Maximum ratio of one line modification: " + str(allChange["ratioMax"]) + ' %' + '\n')
	countReport.write("Median ratio of one line modification: " + str(allChange["ratioMedian"]) + ' %' + '\n')
	countReport.write("Average ratio of one line modification: " + str(allChange["ratioAvg"]) + ' %' + '\n')
	countReport.close()


def countCommit():
	bugFixCommitsStat = open('BugFixCommitsStats.txt', 'r')
	Stat = bugFixCommitsStat.read()
	y = len(re.findall("commit\s[a-zA-Z0-9]+\nAuthor:\s", Stat))
	print("Commmit: " + str(y))

	rep = Stat.count("1 file changed, 1 insertion(+), 1 deletion(-)\n")
	dele = Stat.count("1 file changed, 1 insertion(+)\n")
	inst = Stat.count("1 file changed, 1 deletion(-)\n")

	modif = rep + dele + inst
	print("One Line Commit: " + str(modif))



#getOneLineChange()
#readProj()
#readProjJavaOnly()
#genProjectsList()

#bugFixAnalysis()

countFiles()

#countCommit()

#mergeCSV()

#allChangeAnalysis()

#countAllChange()
