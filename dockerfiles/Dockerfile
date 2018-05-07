FROM nvidia/cuda:9.1-cudnn7-devel

ENV WORKDIR_PATH /yolo
ENV N_JOBS 4

RUN apt-get update && apt-get install -y \
    git \
    wget \
    python \
    python-pip \
    python3

RUN mkdir $WORKDIR_PATH \
    && cd $WORKDIR_PATH \
    && git clone https://github.com/dimka-sark/darknet_platform.git \
    && cd darknet_platform \
    && make -j $N_JOBS \
    && cd $WORKDIR_PATH/darknet_platform/darknet_base/run/all_data/ \
    && rm darknet53.conv.74 \
    && wget https://pjreddie.com/media/files/darknet53.conv.74

WORKDIR $WORKDIR_PATH/darknet_platform