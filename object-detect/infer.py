import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import matplotlib
import argparse
import json
matplotlib.use('Agg')

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

from utils import label_map_util

sys.path.append("..")

# command line arguments
parser = argparse.ArgumentParser(description='Validate image for object detection.')
parser.add_argument('inModel', type=str, help='The frozen model file used in detection')
parser.add_argument('inImageDir', type=str, help='The directory with raw input images')
parser.add_argument('outDir', type=str, help='Output directory for detected object files')
parser.add_argument('threshold', type=float, help='Threshold for object detection')
args = parser.parse_args()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = args.inModel

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = '/tensorflow/models/object_detection/data/mscoco_label_map.pbtxt'

NUM_CLASSES = 90

# Load the frozen tensorflow model.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

# Load the label map.
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Helper.
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# Detection
PATH_TO_TEST_IMAGES_DIR = args.inImageDir

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    for dirpath, dnames, fnames in os.walk(PATH_TO_TEST_IMAGES_DIR):
      for f in fnames:
        image = Image.open(os.path.join(dirpath, f))
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        # Output JSON files for each image with detected classes.
        objects = []
        basename = f.split('.')[0]
        devID = basename.split('_')[0]
        timestamp = basename.split('_')[1]
        for idx, score in enumerate(scores[0]):
            if score > args.threshold:
                objects.append({"score": str(score), "class": int(classes[0][idx])})
        if len(objects) > 0:
            if not os.path.exists(args.outDir + devID): 
                os.makedirs(args.outDir + devID)
            with open(args.outDir + devID + '/' + timestamp + '.json', 'w') as fp:
                json.dump({"objects": objects}, fp, indent=4)
