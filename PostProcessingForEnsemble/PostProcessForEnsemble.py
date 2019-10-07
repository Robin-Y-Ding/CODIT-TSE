import argparse
import os
from util import *
from detokenize import ProcessPredictions
from GeneratePatches import GenPatches

def matchBugId(args):
	onmtRes = open(args.onmtFile, 'r')
	res = open(args.tgtFile, 'w')
	oneLineBugInfo = open("Defects4J_oneLiner_metadata.csv", 'r')
	oneLineBugInfoLines = oneLineBugInfo.readlines()

	onmtResLines = onmtRes.readlines()
	if len(onmtResLines) != int(args.beamSize) * 75:
		print ("Warning: please check the number of lines in onmt results: " + str(len(onmtResLines)))
	for idx, line in enumerate(oneLineBugInfoLines):
		proj, bugId, rPath, lineNum = line.strip().split(',')
		for offset in range(0, int(args.beamSize)):
			currentIdx = idx * int(args.beamSize) + offset
			#print (onmtResLines[currentIdx])
			currentLine, currentProb = onmtResLines[currentIdx].strip('\n').split('\t')
			currentLine = '<s>\t' + currentLine.strip().replace(' ', '\t') + '\t</s>'
			bug = '_'.join([proj, bugId])
			abPathPre = "/home/robin/Documents/d4j-info/d4j/projects/" + proj.lower() + '/' + proj.lower() + '_' + bugId + '_' + "buggy"
			abPath = os.path.join(abPathPre, rPath)
			newLine = ','.join([bug, abPath, lineNum, "1.0", currentProb, currentLine]) + '\n'
			res.write(newLine)

	res.close()
	onmtRes.close()
	oneLineBugInfo.close()


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("onmtFile", help="Results from token-only model")
	ap.add_argument("tgtFile", help="Results that can fit into Robin's framework")
	ap.add_argument("beamSize", help="The beam size of onmt experiments")
	args = ap.parse_args()

	matchBugId(args)
	os.mkdir('split_result')
	split_loc = PreSplit(args.tgtFile)
	SplitCsv(args.tgtFile, split_loc)

	OrderResults('split_result/')

	os.mkdir('tokenized_patches')
	ExtractPatchForEnsemble('split_result/')

	os.mkdir('JavaSource_patches')
	ProcessPredictions('tokenized_patches/')

	os.mkdir('Patches')
	GenPatches('Patches', args.beamSize)

if __name__ == '__main__':
	main()