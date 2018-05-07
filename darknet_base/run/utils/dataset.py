import argparse
import os
import shutil
import json
import random

from zipfile import ZipFile



def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path) 

def prepare_dataset(path_to_zip, out_folder, validate=False, load_mapping_from_file=False):
    makedirs(out_folder)
    with ZipFile(path_to_zip) as zip_file:
        annotaions_json = None
        with zip_file.open('annotations.json') as annotations_file:
            annotaions_json = json.loads(annotations_file.read().decode("utf-8"))


        raw_images = annotaions_json['images']
        raw_anns = annotaions_json['annotations']

        obj_name_file_path = os.path.join(out_folder, 'obj.names')

        innerIndex = 0
        class_map = {}        

        if load_mapping_from_file:
            with open(obj_name_file_path, 'r') as f:
                for line in f:
                    sline = line.strip()
                    if sline:
                        class_map[sline] = {'index':innerIndex}
                        innerIndex+=1

        else:
            names_array = []
            for cl in annotaions_json['categories']:
                class_map[cl["id"]] = {'index':innerIndex}
                names_array.append(str(cl["id"]))
                innerIndex+=1
                pass

            with open(obj_name_file_path, 'w') as f:
                f.write("\n".join(names_array) + '\n')

        


        train_out_folder = os.path.join(out_folder, 'train')
        val_out_folder = os.path.join(out_folder, 'val')

        train_out_file = open(os.path.join(out_folder, 'train.txt'), 'w')
        val_out_file = open(os.path.join(out_folder, 'val.txt'), 'w')

        makedirs(train_out_folder)
        makedirs(val_out_folder)

        anns_offset = 0

        for i in range(0,len(raw_images)):
            if i % 100:
                print('{}/{} images processes'.format(i,len(raw_images)))
            image_info = raw_images[i]
            darknet_format = []


            image_width = image_info['width']
            image_height = image_info['height']

            while True:
                if anns_offset >= len(raw_anns):
                    break

                ann = raw_anns[anns_offset]
                if raw_anns[anns_offset]['image_id'] != image_info['id']:
                    break 
                map_index = class_map[ann["category_id"]]['index']

                new_width = ann['bbox'][2]/image_width
                new_height = ann['bbox'][3]/image_height
                x = ann['bbox'][0]/image_width + new_width/2
                y = ann['bbox'][1]/image_height + new_height/2

                darknet_format.append('{} {} {} {} {}\n'.format(map_index, x,y,new_width, new_height))



                anns_offset+=1

            out_file_image_path = None
            if validate:
                out_file_image_path = os.path.join(val_out_folder, os.path.basename(image_info['file_name']))
                val_out_file.write(out_file_image_path + '\n')    
                
            else:
                out_file_image_path = os.path.join(train_out_folder, os.path.basename(image_info['file_name']))
                train_out_file.write(out_file_image_path + '\n')
 


            with open(out_file_image_path, 'wb') as file:
                with zip_file.open(image_info['file_name']) as image_file:
                    file.write(image_file.read())

            out_file_txt_path = os.path.splitext(out_file_image_path)[0] + '.txt'

            with open(out_file_txt_path, 'w') as ann_res_file:
                ann_res_file.write("".join(darknet_format) + '\n')
            pass

if __name__ == '__main__':
    prepare_dataset('D:\\Downloads\\yolo_prepare\\validation.zip', 'D:\\Downloads\\yolo_prepare\\out')