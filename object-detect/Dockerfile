FROM deeone/tensorflow-object-detection:1.2.1
RUN apt-get update && apt-get install -y python-tk \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ADD infer.py /tensorflow/models/object_detection/

