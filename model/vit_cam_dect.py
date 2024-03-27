# from ultralytics import YOLO
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor
# import cv2
# import os 
# import keras
# import numpy as np
import tensorflow as tf
# from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa
# from keras.preprocessing import image

# model_face = YOLO("/home/ubuntu/codes/kafka/prod/model/yolov8n-face.pt")
# img_path = r"D:\BIG_PROJECT\face-detection-yolov8\examples\face2.jpg"
# img = cv2.imread(img_path)


###############################

#Patches
class Patches(layers.Layer):
    def __init__(self, patch_size, **kwargs):
        super(Patches, self).__init__()
        self.patch_size = patch_size

    def call(self, images):
        batch_size = tf.shape(images)[0]
        patches = tf.image.extract_patches(
        images=images,
        sizes=[1,self.patch_size, self.patch_size, 1],
        strides=[1,self.patch_size, self.patch_size, 1],
        rates=[1,1,1,1],
        padding='VALID',
        )
        patch_dims = patches.shape[-1]
        patches = tf.reshape(patches, [batch_size, -1, patch_dims])
        return patches

####Patchencoder
class PatchEncoder(layers.Layer):
    def __init__(self, num_patches, projection_dim, **kwargs):
      super(PatchEncoder, self).__init__()
      self.num_patches = num_patches
      self.projection = layers.Dense(units=projection_dim)
      self.position_embedding = layers.Embedding(input_dim=num_patches, output_dim=projection_dim)

    def call(self, patch):
      position = tf.range(start=0, limit=self.num_patches, delta=1)
      encoded = self.projection(patch) + self.position_embedding(position)
      return encoded


#################################

vit_local = "model/local_vit_500.h5"



custom_objects = {'Patches': Patches, 'PatchEncoder': PatchEncoder}
model = tf.keras.models.load_model(vit_local, custom_objects=custom_objects)


# camera.get_camera_detect(model_face, model)

