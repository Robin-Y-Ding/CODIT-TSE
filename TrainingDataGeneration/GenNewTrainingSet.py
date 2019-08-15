import glob
import os

def GenNewTrainingSet():
	buggyBase = "/home/robin/Documents/OneLineDataForCODIT/DataSetSmall/buggy"
	patchBase = "/home/robin/Documents/OneLineDataForCODIT/DataSetSmall/patch"
	dataType = "*.java"
	smallTrain = open("smallTrainingList.txt", 'w')
	
	for i in range(len(next(os.walk(buggyBase))[1])):
		buggyDir = os.path.join(buggyBase, str(i))
		patchDir = os.path.join(patchBase, str(i))
		buggy = glob.glob(os.path.join(buggyDir, dataType))
		patch = glob.glob(os.path.join(patchDir, dataType))
		if len(buggy) > 1 or len(patch) > 1:
			print (buggyDir + " or " + patchDir + " has more than one file!!!")
		elif len(buggy) == 0 or len(patch) == 0:
			print (buggyDir + " or " + patchDir +" has no file")
			continue
		else:
			smallTrain.write(buggy[0] + "\t" + patch[0] + '\n')


GenNewTrainingSet()