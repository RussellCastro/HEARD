#!/usr/bin/env python3

import cv2
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Empty

class Detector:
    def __init__( self ):
        rospy.init_node( "detector", anonymous = True ) 

        self.detected_humans_pub = rospy.Publisher( "/drone/detected_humans", Image, queue_size = 10 )
        self.emergency_pub = rospy.Publisher( "/drone/emergency", Empty, queue_size = 10 )

        self.downward_cam_sub = rospy.Subscriber( "/drone/downward_cam", Image, self.detect )

        self.bridge = CvBridge()

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

        self.EMERGENCY_THRESHOLD = 1.0


    def detect( self, data ):

        frame = self.bridge.imgmsg_to_cv2( data )

        humans, values = self.hog.detectMultiScale( frame,
                                                    winStride = ( 2, 2 ),
                                                    padding = ( 4, 4 ),  
                                                    scale = 1.01 )

        for ( x, y, w, h ), value in zip( humans, values ):
            cv2.rectangle( frame, 
                           ( x, y ), 
                           ( x + w, y + h ), 
                           ( 0, 0, 255 ), 
                           1 )

            frame = cv2.putText( frame, 
                                 str( value ), 
                                 ( x, y ), 
                                 cv2.FONT_HERSHEY_COMPLEX, 
                                 1.0, 
                                 ( 0, 0, 255 ),
                                 1 )

            if value >= self.EMERGENCY_THRESHOLD:
                self.emergency_pub.publish()

        self.detected_humans_pub.publish( self.bridge.cv2_to_imgmsg( frame ) )


    def run( self ):
        # while not rospy.is_shutdown():
        rospy.spin()


if __name__ == "main":
    try:
        detector = Detector()
        detector.run()
    except rospy.ROSInterruptException:
        pass
        