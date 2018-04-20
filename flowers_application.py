import os
import numpy as np
import tensorflow as tf
from tensorflow_vgg import utils
from tensorflow_vgg import vgg16

def classifier(image_path):
    g1 = tf.Graph()
    with g1.as_default():
        test_input = tf.placeholder(tf.float32, shape=[None, 4096])
# 加入一个256维的全连接的层
        fc = tf.contrib.layers.fully_connected(test_input, 256)
# 加入一个5维的全连接层
        logits = tf.contrib.layers.fully_connected(fc, 5, activation_fn=None)
        predicted = tf.nn.softmax(logits)
        saver = tf.train.Saver()
        with tf.Session() as sess:
            vgg = vgg16.Vgg16()
            input_ = tf.placeholder(tf.float32, [None, 224, 224, 3])
            with tf.name_scope("content_vgg"):
            # 载入VGG16模型
                vgg.build(input_)
                ckpt = tf.train.get_checkpoint_state('checkpoints')
                saver.restore(sess,ckpt.model_checkpoint_path)
                img = utils.load_image(image_path)
                img = img.reshape((1, 224, 224, 3))
                test_batch = []
                test_batch.append(img)
                image_one = np.concatenate(test_batch)
                feed1 = {input_: image_one}
                img_feature = sess.run(vgg.relu6, feed_dict=feed1)
                feed = {test_input: img_feature}
                res = sess.run(predicted, feed_dict=feed)
                test_acc = sess.run(predicted, feed_dict=feed)
            return np.argmax(test_acc)




