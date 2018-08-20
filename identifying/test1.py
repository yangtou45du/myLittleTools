#!/usr/bin/env python
# -*- coding: cp936 -*-
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import random
import time

# ��֤��ͼƬ�Ĵ��·��
CAPTCHA_IMAGE_PATH = 'C:\Users\Lenovo\PycharmProjects\myLittleTools\identifying\getVerifyCode.png'
# ��֤��ͼƬ�Ŀ��
CAPTCHA_IMAGE_WIDHT = 60
# ��֤��ͼƬ�ĸ߶�
CAPTCHA_IMAGE_HEIGHT = 30

CHAR_SET_LEN = 10
CAPTCHA_LEN = 4

# 60%����֤��ͼƬ����ѵ������
TRAIN_IMAGE_PERCENT = 0.6
# ѵ����������ѵ������֤��ͼƬ���ļ���
TRAINING_IMAGE_NAME = []
# ��֤��������ģ����֤����֤��ͼƬ���ļ���
VALIDATION_IMAGE_NAME = []
# ���ѵ���õ�ģ�͵�·��
MODEL_SAVE_PATH = 'E:/Tensorflow/captcha/models/'


def get_image_file_name(imgPath=CAPTCHA_IMAGE_PATH):
    fileName = []
    total = 0
    for filePath in os.listdir(imgPath):
        captcha_name = filePath.split('/')[-1]
        fileName.append(captcha_name)
        total += 1
    return fileName, total
print get_image_file_name()
'''
# ����֤��ת��Ϊѵ��ʱ�õı�ǩ������ά���� 40
# ���磬�����֤���� ��0296�� �����Ӧ�ı�ǩ��
# [1 0 0 0 0 0 0 0 0 0
#  0 0 1 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 1
#  0 0 0 0 0 0 1 0 0 0]
def name2label(name):
    label = np.zeros(CAPTCHA_LEN * CHAR_SET_LEN)
    for i, c in enumerate(name):
        idx = i * CHAR_SET_LEN + ord(c) - ord('0')
        label[idx] = 1
    return label


# ȡ����֤��ͼƬ�������Լ����ı�ǩ
def get_data_and_label(fileName, filePath=CAPTCHA_IMAGE_PATH):
    pathName = os.path.join(filePath, fileName)
    img = Image.open(pathName)
    # תΪ�Ҷ�ͼ
    img = img.convert("L")
    image_array = np.array(img)
    image_data = image_array.flatten() / 255
    image_label = name2label(fileName[0:CAPTCHA_LEN])
    return image_data, image_label


# ����һ��ѵ��batch
def get_next_batch(batchSize=32, trainOrTest='train', step=0):
    batch_data = np.zeros([batchSize, CAPTCHA_IMAGE_WIDHT * CAPTCHA_IMAGE_HEIGHT])
    batch_label = np.zeros([batchSize, CAPTCHA_LEN * CHAR_SET_LEN])
    fileNameList = TRAINING_IMAGE_NAME
    if trainOrTest == 'validate':
        fileNameList = VALIDATION_IMAGE_NAME

    totalNumber = len(fileNameList)
    indexStart = step * batchSize
    for i in range(batchSize):
        index = (i + indexStart) % totalNumber
        name = fileNameList[index]
        img_data, img_label = get_data_and_label(name)
        batch_data[i, :] = img_data
        batch_label[i, :] = img_label

    return batch_data, batch_label


# ������������粢ѵ��
def train_data_with_CNN():
    # ��ʼ��Ȩֵ
    def weight_variable(shape, name='weight'):
        init = tf.truncated_normal(shape, stddev=0.1)
        var = tf.Variable(initial_value=init, name=name)
        return var
        # ��ʼ��ƫ��

    def bias_variable(shape, name='bias'):
        init = tf.constant(0.1, shape=shape)
        var = tf.Variable(init, name=name)
        return var
        # ���

    def conv2d(x, W, name='conv2d'):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name=name)
        # �ػ�

    def max_pool_2X2(x, name='maxpool'):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name=name)

        # �����

    # ��ע�� X �� name���ڲ���modelʱ���õ���
    X = tf.placeholder(tf.float32, [None, CAPTCHA_IMAGE_WIDHT * CAPTCHA_IMAGE_HEIGHT], name='data-input')
    Y = tf.placeholder(tf.float32, [None, CAPTCHA_LEN * CHAR_SET_LEN], name='label-input')
    x_input = tf.reshape(X, [-1, CAPTCHA_IMAGE_HEIGHT, CAPTCHA_IMAGE_WIDHT, 1], name='x-input')
    # dropout,��ֹ�����
    # ��ע�� keep_prob �� name���ڲ���modelʱ���õ���
    keep_prob = tf.placeholder(tf.float32, name='keep-prob')
    # ��һ����
    W_conv1 = weight_variable([5, 5, 1, 32], 'W_conv1')
    B_conv1 = bias_variable([32], 'B_conv1')
    conv1 = tf.nn.relu(conv2d(x_input, W_conv1, 'conv1') + B_conv1)
    conv1 = max_pool_2X2(conv1, 'conv1-pool')
    conv1 = tf.nn.dropout(conv1, keep_prob)
    # �ڶ�����
    W_conv2 = weight_variable([5, 5, 32, 64], 'W_conv2')
    B_conv2 = bias_variable([64], 'B_conv2')
    conv2 = tf.nn.relu(conv2d(conv1, W_conv2, 'conv2') + B_conv2)
    conv2 = max_pool_2X2(conv2, 'conv2-pool')
    conv2 = tf.nn.dropout(conv2, keep_prob)
    # ��������
    W_conv3 = weight_variable([5, 5, 64, 64], 'W_conv3')
    B_conv3 = bias_variable([64], 'B_conv3')
    conv3 = tf.nn.relu(conv2d(conv2, W_conv3, 'conv3') + B_conv3)
    conv3 = max_pool_2X2(conv3, 'conv3-pool')
    conv3 = tf.nn.dropout(conv3, keep_prob)
    # ȫ���Ӳ�
    # ÿ�γػ���ͼƬ�Ŀ�Ⱥ͸߶Ⱦ���СΪԭ����һ�룬������������γػ�����Ⱥ͸߶Ⱦ���С8��
    W_fc1 = weight_variable([20 * 8 * 64, 1024], 'W_fc1')
    B_fc1 = bias_variable([1024], 'B_fc1')
    fc1 = tf.reshape(conv3, [-1, 20 * 8 * 64])
    fc1 = tf.nn.relu(tf.add(tf.matmul(fc1, W_fc1), B_fc1))
    fc1 = tf.nn.dropout(fc1, keep_prob)
    # �����
    W_fc2 = weight_variable([1024, CAPTCHA_LEN * CHAR_SET_LEN], 'W_fc2')
    B_fc2 = bias_variable([CAPTCHA_LEN * CHAR_SET_LEN], 'B_fc2')
    output = tf.add(tf.matmul(fc1, W_fc2), B_fc2, 'output')

    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=Y, logits=output))
    optimizer = tf.train.AdamOptimizer(0.001).minimize(loss)

    predict = tf.reshape(output, [-1, CAPTCHA_LEN, CHAR_SET_LEN], name='predict')
    labels = tf.reshape(Y, [-1, CAPTCHA_LEN, CHAR_SET_LEN], name='labels')
    # Ԥ����
    # ��ע�� predict_max_idx �� name���ڲ���modelʱ���õ���
    predict_max_idx = tf.argmax(predict, axis=2, name='predict_max_idx')
    labels_max_idx = tf.argmax(labels, axis=2, name='labels_max_idx')
    predict_correct_vec = tf.equal(predict_max_idx, labels_max_idx)
    accuracy = tf.reduce_mean(tf.cast(predict_correct_vec, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        steps = 0
        for epoch in range(6000):
            train_data, train_label = get_next_batch(64, 'train', steps)
            sess.run(optimizer, feed_dict={X: train_data, Y: train_label, keep_prob: 0.75})
            if steps % 100 == 0:
                test_data, test_label = get_next_batch(100, 'validate', steps)
                acc = sess.run(accuracy, feed_dict={X: test_data, Y: test_label, keep_prob: 1.0})
                print("steps=%d, accuracy=%f" % (steps, acc))
                if acc > 0.99:
                    saver.save(sess, MODEL_SAVE_PATH + "crack_captcha.model", global_step=steps)
                    break
            steps += 1


if __name__ == '__main__':
    image_filename_list, total = get_image_file_name(CAPTCHA_IMAGE_PATH)
    random.seed(time.time())
    # ����˳��
    random.shuffle(image_filename_list)
    trainImageNumber = int(total * TRAIN_IMAGE_PERCENT)
    # �ֳɲ��Լ�
    TRAINING_IMAGE_NAME = image_filename_list[: trainImageNumber]
    # ����֤��
    VALIDATION_IMAGE_NAME = image_filename_list[trainImageNumber:]
    train_data_with_CNN()
    print('Training finished')
'''