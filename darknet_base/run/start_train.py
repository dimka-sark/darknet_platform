from utils.dataset import prepare_dataset
from utils.config import result_data
import json
import os
import shlex
import subprocess

def run_command(command):
	process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
	while True:
		output = process.stdout.readline()
		if output == '' and process.poll() is not None:
			break
		if output:
			print(output.strip())
			if False and output.startswith('!!!'):
				print(output)

	rc = process.poll()
	return rc

def main():
	zip_file_path = os.environ.get('TRAIN_DATASET_PATH', 'D:\\Downloads\\yolo_prepare\\validation.zip') 
	dataset_out_folder = os.environ.get('TEMP_DATASET_PATH', 'D:\\Downloads\\yolo_prepare\\out')
	data_folder = os.environ.get('IN_DATA_PATH', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'all_data'))
	weigth_out_put =  os.environ.get('TRAIN_PATH_TO_SAVE_RESULT', 'D:\\Downloads\\yolo_prepare\\out\\weights') 

	prepare_dataset(zip_file_path, dataset_out_folder)
	result_data(dataset_out_folder, data_folder, 
		dataset_out_folder, weigth_out_put)

	save_to_one_file = os.path.join(os.environ.get('MODEL_SAVE_DATA_PATH', 'D:\\Downloads\\yolo_prepare\\out') ,'all_cnn_net_info.json')

	result = {}

	with open(os.path.join(dataset_out_folder, 'obj.data'),'r') as file:
		result['obj.data'] = file.read()

	with open(os.path.join(dataset_out_folder, 'obj.names'),'r') as file:
		result['obj.names'] = file.read()

	with open(os.path.join(dataset_out_folder, 'yolo-obj.cfg'),'r') as file:
		result['yolo-obj.cfg'] = file.read()


	with open(save_to_one_file, 'w') as file:
		json.dump(result, file)


	run_command('./darknet  detector train {} {} {} -gpus 1'.format(
		os.path.join(dataset_out_folder, 'obj.data'), 
		os.path.join(dataset_out_folder, 'yolo-obj.cfg'),
		os.path.join(data_folder, 'darknet53.conv.74')))


if __name__ == '__main__':
	main()