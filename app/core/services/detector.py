import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

import logging
import time

class ObjectDetector:
    module_handle = "/code/app/core/models"

    def __init__(self):
        self.detector = hub.load(self.module_handle).signatures["default"]

    def run(self, img_bytes, expand_animations=False):
        img = tf.image.decode_image(img_bytes, channels=3, expand_animations=expand_animations)
        converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

        result = self.detector(converted_img)
        result = { key : value.numpy() for key, value in result.items() }

        return result
