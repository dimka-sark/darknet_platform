mkdir /yolo2
cd /yolo2
git clone https://github.com/dimka-sark/darknet_platform.git
cd /yolo2/darknet_platform/darknet_base
make -j 8

export TRAIN_DATASET_PATH=/dataset2/validation.zip 
export TEMP_DATASET_PATH=/tmp
export TRAIN_PATH_TO_SAVE_RESULT=/output
export MODEL_SAVE_DATA_PATH=/output

export MODEL_SAVE_DATA_PATH=/output
export MODEL_SAVE_DATA_PATH=/output



apt-get install python3
cd /yolo2/darknet_platform/darknet_base/run/all_data/
rm darknet53.conv.74
wget https://pjreddie.com/media/files/darknet53.conv.74
cd /yolo2/darknet_platform/darknet_base/
python3 run/start_train.py
