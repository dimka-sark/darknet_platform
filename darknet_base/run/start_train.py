from utils.dataset import prepare_dataset
from utils.config import result_data
import json
import os
import shlex
import subprocess

def run_command(command):
	return subprocess.call(shlex.split(command))
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

	path_to_darknet_bin = os.environ.get('DARKNET_BIN_PATH', '/yolo/darknet_platform/darknet_base/darknet') 

	override_weight_path = os.environ.get('TRAIN_PATH_TO_INIT', None) 

	save_to_one_file = os.path.join(os.environ.get('MODEL_SAVE_DATA_PATH', 'D:\\Downloads\\yolo_prepare\\out') ,'all_cnn_net_info.json')
	
	obj_names_path = os.path.join(dataset_out_folder, 'obj.names')
	obj_config_path = os.path.join(dataset_out_folder, 'yolo-obj.cfg')


	load_mapping_from_file = False

	if override_weight_path:
		load_mapping_from_file = True
		loaded_config = None
		
		with open(save_to_one_file, 'r') as file:
			loaded_config = json.load(file)

		with open(obj_names_path,'w') as file:
			file.write(loaded_config['obj.names'])

		with open(obj_config_path,'w') as file:
			file.write(loaded_config['yolo-obj.cfg'])


	visible_gpu = os.environ.get('CUDA_VISIBLE_DEVICES', None)
	if visible_gpu:
		visible_gpu = '-gpus {} '.format(visible_gpu)
	else:
		visible_gpu = ''

	save_step_count =  int(os.environ.get('SAVE_EACH_STEPS', 200))
	min_loss =  float(os.environ.get('TRAIN_MIN_LOSS', 0.1))

	prepare_dataset(zip_file_path, dataset_out_folder, load_mapping_from_file=load_mapping_from_file)
	result_data(dataset_out_folder, data_folder, 
		dataset_out_folder, weigth_out_put, generate_config= (not load_mapping_from_file))


	result = {}

	with open(os.path.join(dataset_out_folder, 'obj.data'),'r') as file:
		result['obj.data'] = file.read()

	with open(obj_names_path,'r') as file:
		result['obj.names'] = file.read()

	with open(obj_config_path,'r') as file:
		result['yolo-obj.cfg'] = file.read()


	with open(save_to_one_file, 'w') as file:
		json.dump(result, file)

	path_to_start_weight = override_weight_path if override_weight_path else os.path.join(data_folder, 'darknet53.conv.74')
	run_command_str = '{} detector train {} {} {} {}-save {} -loss {}'.format(
		path_to_darknet_bin,
		os.path.join(dataset_out_folder, 'obj.data'), 
		os.path.join(dataset_out_folder, 'yolo-obj.cfg'),
		path_to_start_weight,
		'',
		save_step_count,
		min_loss)
	print(run_command_str)
	run_command(run_command_str)


if __name__ == '__main__':
	main()