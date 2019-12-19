import json
import re
import javalang
import sys
import random
import subprocess
import os
import shutil
import argparse
import numpy as np

MAX_PULL_TIME = 60

def extractGitLog():
	small = open('bugsLarge.json','r')

	#smallStr = open('/home/robin/Documents/one-line-bug-dataset/BugsSmall.txt', 'w')
	#largeStr = open('/home/robin/Documents/one-line-bug-dataset/BugsLarge.txt', 'w')

	smallData = json.load(small)

	ProjDir = "/home/robin/Documents/projects"
	if not os.path.isdir(ProjDir):
		os.makedirs(ProjDir)

	projs = list()

	for idx, sd in enumerate(smallData):
		projectName = sd["projectName"]
		projs.append(projectName)
		
		#lineNum = sd["lineNum"]

	projs = set(projs)

	for proj in projs:

		p = proj.split('.')[-1]
		bugProj = os.path.join(ProjDir, p)
		print("Currently pulling: " + p)
		
		if not os.path.isdir(bugProj):
			cmd = ""
			cmd += "cd " + ProjDir + ";"
			cmd += "git clone https://github.com/" + proj.replace('.', '/') + ".git"
			process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
			try:
				output, error = process.communicate(timeout=MAX_PULL_TIME)
			except subprocess.TimeoutExpired:
				process.kill()
				process.wait()
				continue
		
		resultDir = os.path.join("/home/robin/Documents/dataset-analysis/results", proj.replace('.', '___'))
		if not os.path.isdir(resultDir):
			os.makedirs(resultDir)
		cmd = ""
		cmd += "cd " + bugProj + ";"
		#We design the commit in specific formats for further operation:
		# -----
		# Sha
		# k files changed, p insertions, q deletions
		cmd += "git log --shortstat --pretty=format:'-----%n%H' --follow *.java > " + os.path.join(resultDir, "java_stats.txt") + ";"
		
	
		subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)

		if os.path.isdir(bugProj):
			shutil.rmtree(bugProj)
	'''

	baseDirLarge = "/home/robin/Documents/DataSetLarge"
	if not os.path.isdir(baseDirLarge):
		os.makedirs(baseDirLarge)

	bugBaseDirLarge = os.path.join(baseDirLarge, "buggy")
	if not os.path.isdir(bugBaseDirLarge):
		os.makedirs(bugBaseDirLarge)

	patchBaseDirLarge = os.path.join(baseDirLarge, "patch")
	if not os.path.isdir(patchBaseDirLarge):
		os.makedirs(patchBaseDirLarge)


	for idx, sd in enumerate(largeData):
		projectName = sd["projectName"]
		proj = projectName.split('.')[-1]
		patchSHA1 = sd["commitSHA1"]
		patchFile = sd["commitFile"]
		#lineNum = sd["lineNum"]
		bugDir = os.path.join(bugBaseDirLarge, str(idx))
		if not os.path.isdir(bugDir):
			os.makedirs(bugDir)

		patchDir = os.path.join(patchBaseDirLarge, str(idx))
		if not os.path.isdir(patchDir):
			os.makedirs(patchDir)

		bugProj = os.path.join(ProjDir, proj)
		if not os.path.isdir(bugProj):
			cmd = ""
			cmd += "cd " + ProjDir + ";"
			cmd += "git clone https://github.com/" + projectName.replace('.', '/') + ".git"
			result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
		cmd = ""
		cmd += "cd " + bugProj + ";"
		cmd += "git checkout " + patchSHA1 + "^" + ";"
		cmd += "cp " + patchFile + " " + bugDir + ";"
		cmd += "git checkout " + patchSHA1 + ";"
		cmd += "cp " + patchFile + " " + patchDir
		subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	'''


def extractSingleFileChange():
	projDir = "/home/robin/Documents/dataset-analysis/tmpProject"
	prevDataDir = "/home/robin/Documents/dataset-analysis/data/prev"
	postDataDir = "/home/robin/Documents/dataset-analysis/data/post"
	stats = "/home/robin/Documents/dataset-analysis/results"
	oneFileChanges = list()

	if not os.path.isdir(projDir):
		os.makedirs(projDir) #Dir to store java projects

	#projs = os.listdir("/home/robin/Documents/dataset-analysis/results/")
	projs = os.listdir(stats)
	fileCnt = 0
	
	for proj in projs:
		statsFile = os.path.join(proj, 'java_stats.txt')
		singleFileCommit = list()
		with open(os.path.join(stats, statsFile), 'r') as sf:
			gitLogs = list(filter(None, sf.read().split("-----\n"))) #each element is a commit
			for gl in gitLogs:
				if "1 file changed" in gl:
					commit = list(filter(None, gl.split('\n')))
					singleFileCommit.append(commit[0])

		owner, repo = proj.split('___')
		bugProj = os.path.join(projDir, repo)
		print("Currently pulling: " + repo)
		if not os.path.isdir(bugProj):
			#pull the project
			cmd = ""
			cmd += "cd " + projDir + ";"
			cmd += "git clone https://github.com/" + proj.replace('___', '/') + ".git"
			process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
			try:
				output, error = process.communicate(timeout=MAX_PULL_TIME)
				print (repo + " is pulled.")
			except subprocess.TimeoutExpired:
				process.kill()
				process.wait()
				continue
		# get the name of modified file
		for sha in singleFileCommit:
			print("Currently processing: No. " + str(fileCnt) + " sample.")
			prevDir = os.path.join(prevDataDir, str(fileCnt))
			postDir = os.path.join(postDataDir, str(fileCnt))
			if not os.path.isdir(prevDir):
				os.makedirs(prevDir) #Dir to store original files
			if not os.path.isdir(postDir):
				os.makedirs(postDir)

			detail = dict()
			detail["index"] = str(fileCnt)
			detail["Project"] = proj
			detail["Commit"] = sha
			cmd = ""
			cmd += "cd " + bugProj + ";"
			cmd += "git diff --name-only " + sha + " " + sha + '^ ' + "*.java" + ';'
			result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
			result = result.stdout.decode('utf-8')
			result = list(filter(None, result.split('\n')))

			if len(result) > 1:
				print ("More than 1 file modified")
				print (result)
			modifiedFile = result[0]
			detail["Modified"] = modifiedFile
			oneFileChanges.append(detail)

			cmd = ""
			cmd += "cd " + bugProj + ";"
			cmd += "git checkout " + sha + ";"
			cmd += "cp " + modifiedFile + " " + postDir + ';'
			cmd += "git checkout " + sha + "^" + ";"
			cmd += "cp " + modifiedFile + " " + prevDir + ";"
			
			subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
			fileCnt += 1

		if os.path.isdir(bugProj):
			shutil.rmtree(bugProj)

	with open("OneFileChanges.json", 'w') as cf:
		cf.write(json.dumps(oneFileChanges, indent=4))




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--type", help="type of extracting: [log, file]")
	args = parser.parse_args()
	if args.type == 'log':
		extractGitLog()
	elif args.type == 'file':
		extractSingleFileChange()