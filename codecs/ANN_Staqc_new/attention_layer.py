from tensorflow.keras import backend as K
from tensorflow.keras.layers import *
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


# 定义自定义层
class AttentionLayer(Layer):

    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    # 在build函数中定义层的参数
    def build(self, input_shape):
        # 确保输入是一个长度为2的列表，列表中每个元素的维度应为[batch_size, sequence_length, embedding_dimension]
        if not isinstance(input_shape, list) or len(input_shape) != 2:
            raise ValueError('An attention layer should be called '
                             'on a list of 2 inputs.')
        # 确保两个输入的embedding维度相等
        if not input_shape[0][2] == input_shape[1][2]:
            raise ValueError('Embedding sizes should be of the same size')

        # 初始化权重kernel并添加到该层参数列表中
        self.kernel = self.add_weight(shape=(input_shape[0][2], input_shape[0][2]),
                                      initializer='glorot_uniform',
                                      name='kernel',
                                      trainable=True)

        super(AttentionLayer, self).build(input_shape)

    # 定义层的前向传播逻辑
    def call(self, inputs):
        # 对第一个输入进行线性变换以匹配维度
        a = K.dot(inputs[0], self.kernel)
        # 对第二个输入进行维度转换以匹配第一个输入
        y_trans = K.permute_dimensions(inputs[1], (0, 2, 1))
        # 计算注意力权重
        b = K.batch_dot(a, y_trans, axes=[2, 1])
        # 对注意力权重使用双曲正切激活函数
        return K.tanh(b)

    # 定义输出维度
    def compute_output_shape(self, input_shape):
        return None, input_shape[0][1], input_shape[1][1]  # 输出的维度为(batch_size, sequence_length1, sequence_length2)
