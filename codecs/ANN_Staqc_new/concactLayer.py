from keras.layers import *
import os
import numpy as np
import random
import tensorflow as tf

# 设置随机种子
seed = 42
np.random.seed(seed)
tf.random.set_seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
random.seed(seed)


# 自定义层，用于将输入的block-level code在第二维度进行拼接
class concatLayer(Layer):
    def __init__(self, **kwargs):
        super(concatLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        super(concatLayer, self).build(input_shape)

    def call(self, inputs, **kwargs):
        # 将输入数据按照第二维(也就是block的维度)进行分割
        block_level_code_output = tf.split(inputs, inputs.shape[1], axis=1)
        # 将分割后的数据拼接起来形成一个大的张量
        block_level_code_output = tf.concat(block_level_code_output, axis=2)
        # 将第二维(也就是block的维度)移除，将张量变为二维
        # shape为(bs, 600)
        block_level_code_output = tf.squeeze(block_level_code_output, axis=1)
        print(block_level_code_output)
        return block_level_code_output

    def compute_output_shape(self, input_shape):
        print("===========================", input_shape)
        # 输出形状为(batch_size, 每个block的数据维度之和)
        return input_shape[0], input_shape[1] * input_shape[2]
