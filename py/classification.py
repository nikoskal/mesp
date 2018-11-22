import os
import threading
import logging
import tensorflow as tf


class TensorflowClassifier(threading.Thread):

    def __init__(self, ll, labels, graph, camera, logger):
        threading.Thread.__init__(self)
        # Just disables the warning, doesn't enable AVX/FMA
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(ll)

        # Keep the camera instance
        self.camera = camera
        self.logger = logger

        # Loads label file, strips off carriage return
        self.label_lines = [line.rstrip() for line
            in tf.gfile.GFile(labels)]

        # Unpersists graph from file
        with tf.gfile.FastGFile(graph, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')


    def classify(self, img):

        if not (os.path.exists(img)):
            raise ValueError('No such image file: {}.'.format(img))

        # Read in the image_data
        image_data = tf.gfile.FastGFile(img, 'rb').read()

        # Feed the image_data as input to the graph and get first prediction
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
            self.logger.debug(predictions)
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            info_table = dict()
            for node_id in top_k:
                human_string = self.label_lines[node_id]
                score = predictions[0][node_id]
                info_table[human_string] = score
                # self.logger.info('%s (score = %.5f)' % (human_string, score))

        return info_table
