import os
import re
import sys
import fire
import glob
import subprocess

def post_process(basedir='un-goals'):
	'''
	Post-processes the Grover-generated files, preserving text between 
	Sample x of y and <|endoftext|>. Each sample goes to a different file.
	:param basedir: where all responses are saved
	'''
	# grabs all txt files in the directories inside basedir
	responses = sorted(glob.glob('{}/*/*.txt'.format(basedir))) 

	for r in responses:
		print('Processing ', r)
		# creates a directory for that response (basedir/*/{response}.txt)
		response_dir = os.path.join(os.path.splitext(r)[0])
		os.makedirs(response_dir, exist_ok='True')

		
		with open(r) as r_file:
			content = r_file.read()

			# each file contains 10 samples. Each sample lies between Sample x of y and <|endoftext|>

			# splits the samples on the header 'Sample x of y'. Ignores the first element, as it is useless info
			samples = re.split(r'Sample,\s+\d+\s+of\s+\d+\n', content)[1:]
			
			#if samples is None:
			#	print("Error! No samples found in {}. Ignoring this file...".format(r))
			#	continue
			
			for s_num, sample in enumerate(samples):
				sample = re.split('<\|endoftext\|>', sample)[0]  # ignores whathever comes after <|endoftext|>

				# saves the sample to its output file
				with open(os.path.join(response_dir, 'sample_{}.txt'.format(s_num+1)), 'w') as s_file:
					print("\tCreating file for sample {}".format(s_num+1))
					s_file.write(sample)

if __name__ == '__main__':
	fire.Fire(post_process)



