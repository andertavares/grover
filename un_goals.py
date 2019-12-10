import os
import sys
import fire
import glob
import subprocess

def generate(basedir='un-goals'):
	'''
	Generate the responses of language models to prompts regarding the UN SDGs.
	:param basedir: where all responses will be saved
	'''
	# grabs all txt files under basedir
	prompt_files = sorted(glob.glob('{}/*.txt'.format(basedir))) #['un-goals/goal_{}.txt'.format(str(g).zfill(2)) for g in range(0, 18)]

	for p_file in prompt_files:
		print('Processing ', p_file)
		# creates a directory for that prompt (basedir/{prompt})
		response_dir = os.path.join(os.path.splitext(p_file)[0])
		os.makedirs(response_dir, exist_ok='True')

		# each file contains one prompt per line (regarding one of the sustainable goals)
		# lines starting with comments are ignored
		prompts = [line.strip() for line in open(p_file).readlines() if not line[0] == '#']

		for pnum, prompt in enumerate(prompts):
			print('  Prompt {}: {}'.format(pnum+1, prompt))
			
			out_file = os.path.join(response_dir, 'goal_{}.out.txt'.format(str(pnum+1).zfill(2)))
			print(out_file)
			
			with open(out_file, 'a') as out:
				try:
					process = subprocess.run(
						'printf "{}" | PYTHONPATH=$(pwd) python3 sample/contextual_generate_cli_multiline.py -model_config_fn lm/configs/mega.json -samples 10 -model_ckpt models/mega/model.ckpt-800000 '.format(prompt) ,
						shell=True, check=True, capture_output=True
					)
					out.write(process.stdout.decode('utf-8'))
					out.write('\n')

				except subprocess.CalledProcessError as e:
					out.write('ERROR: {0}'.format(e))
					print('ERROR: {0}'.format(e))

if __name__ == '__main__':
	fire.Fire(generate)



