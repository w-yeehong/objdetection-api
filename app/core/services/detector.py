import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

import json
import time

class ObjectDetector:
    module_handle = "/code/models"
    valid_class_json_file_path = "/code/app/data/valid_classes.json"

    try:
        with open(valid_class_json_file_path) as valid_class_json:
            valid_classes = json.load(valid_class_json)
        valid_classes = { key.encode() : value.encode() for key, value in valid_classes.items() }
    except:
        valid_classes = ""

    def __init__(self):
        self.detector = hub.load(self.module_handle).signatures["default"]

    def run(self, img_bytes, expand_animations=False):
        img = tf.image.decode_image(img_bytes, channels=3, expand_animations=expand_animations)
        converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

        start_time = time.time()
        result = self.detector(converted_img)
        end_time = time.time()

        if not self.valid_classes == "":
            result = self.filter(result)
        else:
            result = { key : value.numpy() for key, value in result.items() }
        inference_time = end_time - start_time

        return (result, inference_time)

    def filter(self, result):
        filter_list = []

        for entity in result["detection_class_names"].numpy():
            if entity in self.valid_classes:
                filter_list.append(True)
            else:
                filter_list.append(False)

        return { key : value.numpy()[filter_list] for key, value in result.items() }
