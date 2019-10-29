import sys
import subprocess
from shutil import copyfile, copy
from datetime import datetime
import os

MAX_COMPILE_TIME = 60
MAX_TEST_TIME = 300


def runCommand(workDir, strCmd, err):
	cmd = ""
	cmd += "cd " + workDir + ";"
	cmd += strCmd
	if err == "DEVNULL":
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	elif err == "PIPE":
		result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	return result


def resultToList(result):
	result = result.decode('utf-8')
	result = result.split("\n")
	result = list(filter(None, result))
	return result


def main(argv):
	global MAX_COMPILE_TIME,MAX_TEST_TIME
	if(not os.path.exists(argv[0])):
		sys.stderr.write("Found no patch in " + argv[0] + "\n")
		sys.stderr.flush()
		sys.exit(0)

	trigger_tests = []
	cmd = ""
	cmd += "cd " + argv[1] + ";"
	cmd += "defects4j export -p tests.trigger"
	result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	result = result.stdout.decode('utf-8')
	result = result.split("\n")
	result = list(filter(None, result))
	for i in range(len(result)):
		trigger_tests.append(result[i].strip())

	sys.stdout.write(argv[1] + " has following triggering tests:\n")
	for test in trigger_tests:
		sys.stdout.write(test+"\n")
		sys.stdout.flush()

	failling_tests = []
	cmd = ""
	cmd += "cd " + argv[1] + ";"
	cmd += "defects4j test"
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	try:
		output, error = process.communicate(timeout=MAX_TEST_TIME)
	except subprocess.TimeoutExpired:
		process.kill()
		process.wait()
		sys.stderr.write("Time limit exceeded when running the original bug version on " + argv[1] +"\n")
		sys.stderr.flush()
		sys.exit(1)
	result = output
	result = result.decode('utf-8')
	result = result.split("\n")
	result = list(filter(None, result))
	for i in range(len(result)):
		if(result[i].startswith("Failing tests:")):
			for j in range(i+1, len(result)):
				failling_tests.append(result[j][4:].strip())
			break

	sys.stdout.write(argv[1] + " has following failing tests:\n")
	for test in failling_tests:
		sys.stdout.write(test+"\n")
		sys.stdout.flush()
	

	bug_id = argv[0].split('/')[-2]
	#bug_info_file = 'split_result/' + bug_id + '_ordered.txt'
	b_i_f = open("d4jPath.txt", 'r')
	bif_lines = b_i_f.readlines()
	bifDict = dict()
	for l in bif_lines:
		buggyId = l.split('/')[8].replace("_buggy", '').capitalize()
		bifDict[buggyId] = l.split(' ')[0]


	#create separate folders when running mutiple experiments at the same time

	time_stamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

	tmp_folder = os.path.join('/tmp', time_stamp)
	if(not os.path.exists(tmp_folder)):
		os.mkdir(tmp_folder)
	else:
		tmp_folder = tmp_folder + "_1"
		os.mkdir(tmp_folder)


	for patch in os.listdir(argv[0]):
		buggy_prefix = argv[2] + bug_id
		# TODO: The following path should be flexible
		info_prefix = '/home/robin/Documents/d4j-info/d4j/projects/' + bug_id.split('_')[0].lower() + '/' + bug_id.lower() + '_buggy'
		full_name = bifDict[bug_id].replace(info_prefix, buggy_prefix)

		
		copyfile(full_name, os.path.join(tmp_folder,os.path.basename(full_name)))
		sys.stdout.write("Testing " + os.path.join(argv[0],patch,os.path.basename(full_name)) + "\n")
		sys.stdout.flush()
		copyfile(os.path.join(argv[0],patch,os.path.basename(full_name)), full_name)

		
		cmd = ""
		cmd += "cd " + argv[1] + ";"
		cmd += "defects4j compile"
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		try:
			output, error = process.communicate(timeout=MAX_COMPILE_TIME)
		except subprocess.TimeoutExpired:
			process.kill()
			process.wait()
			copyfile(os.path.join(tmp_folder,os.path.basename(full_name)), full_name)
			os.remove(os.path.join(tmp_folder,os.path.basename(full_name)))
			sys.stderr.write("Compile Timed out" + argv[1] +"\n")
			sys.stderr.flush()
			continue
		result = error
		result = result.decode('utf-8')
		result = result.split("\n")
		result = list(filter(None, result))
		compile_error = False
		for line in result:
			if(not line.endswith("OK")):
				compile_error = True
		if(compile_error):
			copyfile(os.path.join(tmp_folder,os.path.basename(full_name)), full_name)
			os.remove(os.path.join(tmp_folder,os.path.basename(full_name)))
			continue

		passing_triggerTests = True
		passing_oldTests = True

		for test in trigger_tests:
			cmd = ""
			cmd += "cd " + argv[1] + ";"
			cmd += "defects4j test -t " + test
			process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			try:
				output, error = process.communicate(timeout=MAX_TEST_TIME)
			except subprocess.TimeoutExpired:
				process.kill()
				process.wait()
				copyfile(os.path.join(tmp_folder,os.path.basename(full_name)), full_name)
				os.remove(os.path.join(tmp_folder,os.path.basename(full_name)))
				os.rename(os.path.join(argv[0],patch), os.path.join(argv[0],patch+"_compiled_trigger_timeout"))
				passing_triggerTests = False
				break
			result = output
			result = result.decode('utf-8')
			result = result.split("\n")
			result = list(filter(None, result))
			for i in range(len(result)):
				if(result[i].startswith("Failing tests:") and result[i] != "Failing tests: 0"):
					passing_triggerTests = False

		if passing_triggerTests == True:
			cmd = ""
			cmd += "cd " + argv[1] + ";"
			cmd += "defects4j test"
			process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			try:
				output, error = process.communicate(timeout=MAX_TEST_TIME)
			except subprocess.TimeoutExpired:
				process.kill()
				process.wait()
				copyfile(os.path.join(tmp_folder,os.path.basename(full_name)), full_name)
				os.remove(os.path.join(tmp_folder,os.path.basename(full_name)))
				os.rename(os.path.join(argv[0],patch), os.path.join(argv[0],patch+"_compiled_test_timeout"))
				continue
			result = output
			result = result.decode('utf-8')
			result = result.split("\n")
			result = list(filter(None, result))

			for i in range(len(result)):
				if(result[i].startswith("Failing tests:")):
					for j in range(i+1, len(result)):
						#if(result[j][4:] in trigger_tests):
							#passing_triggerTests = False
						if(result[j][4:] not in failling_tests):
							passing_oldTests = False
					break

		if(passing_triggerTests and passing_oldTests):
			os.rename(os.path.join(argv[0],patch), os.path.join(argv[0],patch+"_passed"))
		elif(passing_triggerTests and not passing_oldTests):
			os.rename(os.path.join(argv[0],patch), os.path.join(argv[0],patch+"_trigger_passed"))
		else:
			os.rename(os.path.join(argv[0],patch), os.path.join(argv[0],patch+"_compiled"))

		copyfile(os.path.join(tmp_folder,os.path.basename(full_name)), full_name)
		os.remove(os.path.join(tmp_folder,os.path.basename(full_name)))
		
	b_i_f.close()

	try:
		os.rmdir(tmp_folder)
	except OSError as e:
		print (e)

if __name__=="__main__":
	main(sys.argv[1:])
