import argparse
import os
import shutil
import json
import random

def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path) 

def result_data(dataset_folder, data_folder, output_folder, path_for_weight):
	classCount = 0
	makedirs(output_folder)

	with open(os.path.join(dataset_folder, "obj.names"), 'r') as f:
		for line in f:
			if line.strip():
				classCount+=1

	filtersCount = (classCount+5)*3
	lineNumber=0

	with open(os.path.join(data_folder, "yolov3.cfg"), 'r') as f:
		with open(os.path.join(output_folder, "yolo-obj.cfg"), 'w') as f2:
			for line in f:
				lineNumber+=1

				processLine = line.strip()

				if lineNumber in [3]:
					processLine = "batch=64"
				if lineNumber in [4]:
					processLine = "subdivisions=16"

				if lineNumber in [610,696,783]:
					processLine = "classes="+str(classCount)

				if lineNumber in [603,689,776]:
					processLine = "filters="+str(filtersCount)

				f2.write(processLine + '\n')

	makedirs(path_for_weight)
	with open(os.path.join(output_folder, "obj.data"), 'w') as f:
		f.write("classes = {}\n".format(classCount))
		f.write("train = {}\n".format(os.path.join(dataset_folder,'train.txt')))
		f.write("valid = {}\n".format(os.path.join(dataset_folder,'val.txt')))
		f.write("names = {}\n".format(os.path.join(dataset_folder,'obj.names')))
		f.write("backup = {}\n".format(path_for_weight)) 



if __name__ == '__main__':
	result_data('D:\\Downloads\\yolo_prepare\\out', 
		'D:\\Projects\\NativeHell\\darknet\\darknet_base\\run\\data', 
		'D:\\Downloads\\yolo_prepare\\out', 
		'D:\\Downloads\\yolo_prepare\\weights')
