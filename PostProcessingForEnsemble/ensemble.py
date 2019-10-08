import argparse
import json

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("result1", help="Results from first model")
	ap.add_argument("result2", help="Results from second model")
	ap.add_argument("beamSize", help="The beam size of onmt experiments")
	args = ap.parse_args()

	result1 = open(args.result1, 'r')
	result2 = open(args.result2, 'r')

	rl1 = result1.readlines()
	rl2 = result2.readlines()

	resDict = dict()

	for rl in rl1:
		bugId, path, prob = rl.strip().split(',')
		if not resDict.get(bugId):
			resDict[bugId] = list()
		resDict[bugId].append([path, float(prob)])

	for rl in rl2:
		bugId, path, prob = rl.strip().split(',')
		if not resDict.get(bugId):
			print('Warning: The bug ids do not match in both models')
			resDict[bugId] = list()
		resDict[bugId].append([path, float(prob)])

	for key in resDict.keys():
		tmp = sorted(resDict[key], key=lambda x : x[1], reverse=True)[:int(args.beamSize)]
		resDict[key] = tmp

	with open('result.json', 'w') as fp:
		json.dump(resDict, fp, indent=4)


if __name__ == "__main__":
	main()