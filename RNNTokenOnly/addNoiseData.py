import argparse
import random
import numpy as np

def add_noise(word_ids):
	word_ids = word_ids.copy()
	#set omit_prob = 0.1

	rc = random.choice(["omit", "swap"])
	if rc == "omit":
		num_omissions = int(0.1 * len(word_ids))
		if num_omissions < 1: num_omissions = 1
		inds_to_omit = np.random.permutation(len(word_ids))[:num_omissions]
		for i in inds_to_omit:
			word_ids[i] = ""
	# Second, swap some of adjacent words
	# set swap_prob to be 0.1
	else:
		num_swaps = int(0.1 * (len(word_ids) - 1))
		if num_swaps < 1: num_swaps = 1
		inds_to_swap = np.random.permutation(len(word_ids) - 1)[:num_swaps]
		for i in inds_to_swap:
			word_ids[i], word_ids[i+1] = word_ids[i+1], word_ids[i]

	return word_ids


def construct_data(words_batch):
	f = open('NoiseData.txt', 'w')
	pre = open('preNoiseData.txt','w')
	post = open('postNoiseData.txt', 'w')
	noise_word_ids_batch = [add_noise(words) for words in words_batch]


	inputs = ['\t'.join(noise_words) for noise_words in noise_word_ids_batch]
	outputs = ['\t'.join(words) for words in words_batch]
	if len(inputs) != len(outputs): 
		print("construct_data failed!")
		return
	for idx, inp in enumerate(inputs):
		if inp.strip() != outputs[idx].strip():
			pre.write(inp.strip() + '\n')
			post.write(outputs[idx].strip() + '\n')
			f.write(inp.strip() + " ---> " + outputs[idx].strip() + '\n')
		

	

def sample(data, sample_prob):
	num_sample = int(sample_prob * len(data))
	sample_inds = np.random.permutation(len(data))[:num_sample]
	words_sample = [data[i].strip().split('\t') for i in sample_inds]
	#print (words_sample)
	construct_data(words_sample)
	


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("srcFile", help="Tokenized data to add noise")
	#ap.add_argument("tgtFile", help="Noisy data pairs")
	args = ap.parse_args()

	srcFile = open(args.srcFile, 'r')
	preList = srcFile.readlines()

	sample(preList, 0.1)


if __name__ == '__main__':
	main()
