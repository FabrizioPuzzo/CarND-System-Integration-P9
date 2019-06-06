from styx_msgs.msg import TrafficLight
import tensorflow as tf
import numpy as np
import cv2
import rospy

class TLClassifier(object):
    def __init__(self):


        # Use model for simulator
        #graph_path = 'light_classification/model/frozen_inference_graph_sim.pb'

        # Use model for real world (Carla)
        graph_path = 'light_classification/model/frozen_inference_graph_real.pb'

        # Initialize graph
        self.graph = tf.Graph()
        self.score_threshold = .5 # minimum score for prediction to be valid

        # Load model
        with self.graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(graph_path, 'rb') as fid:
                od_graph_def.ParseFromString(fid.read())
                tf.import_graph_def(od_graph_def, name='')

            self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
            self.num_detections = self.graph.get_tensor_by_name('num_detections:0')
            self.boxes = self.graph.get_tensor_by_name('detection_boxes:0')
            self.scores = self.graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.graph.get_tensor_by_name('detection_classes:0')

        self.sess = tf.Session(graph=self.graph)


    def get_classification(self, image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv::Mat): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """

        # Prediction step 
        with self.graph.as_default():
            img_expand = np.expand_dims(image, axis=0)
            (boxes, scores, classes, num_detections) = self.sess.run(
                [self.boxes, self.scores, self.classes, self.num_detections], feed_dict={self.image_tensor: img_expand})

        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)

        # Analyzing result und returning light state
        if scores[0] > self.score_threshold:
            if classes[0] == 1:
                return TrafficLight.GREEN

            elif classes[0] == 2:
                return TrafficLight.RED

            elif classes[0] == 3:
                return TrafficLight.YELLOW

        return TrafficLight.UNKNOWN
