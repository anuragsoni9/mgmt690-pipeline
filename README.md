# MGMT690 Image Processing Pipeline

## Create input repositories

Create the repos that will be used for input data:

```sh
$ pachctl create-repo images
$ pachctl create-repo model
$ pachctl create-repo rules
```

Then put our model and rules in the respective repos:

```sh
$ wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz
$ tar -xvf ssd_mobilenet_v1_coco_11_06_2017.tar.gz
$ cd ssd_mobilenet_v1_coco_11_06_2017
$ pachctl put-file model master -c -f frozen_inference_graph.pb
$ cd ../threat-detect/example_rule 
$ pachctl put-file rules master -c -f rule.json
$ cd ../../
```

## Create the pipelines

```sh
$ pachctl create-pipeline -f validate.json
$ pachctl create-pipeline -f object-detect.json
$ pachctl create-pipeline -f threat-detect.json
$ pachctl create-pipeline -f plot.json
```

## Processing images

Images can now be committed to the input directory `images`, and they will automatically be process to generate notifications and plots.
