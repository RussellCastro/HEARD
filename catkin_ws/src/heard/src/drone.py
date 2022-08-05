#!/usr/bin/env python3

from cv_bridge import CvBridge
from djitellopy import Tello
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Empty


class Drone:

    def __init__(self):
        rospy.init_node("drone", anonymous=True)

        self.forward_cam_pub = rospy.Publisher("/drone/forward_cam", Image, queue_size=10)
        self.downward_cam_pub = rospy.Publisher("/drone/downward_cam", Image, queue_size=10)
        ## TODO SUBSCRIBE TO PATHING NODE
        ## TODO SUBSCRIBE TO SOUND NODE
        self.takeoff_pub = rospy.Publisher("/sound/takeoff", Empty, queue_size=10)
        self.to_takeoff_sub = rospy.Subscriber("/sound/takeoff_to", Empty, self.to_takeoff)

        self.to_forward_cam_sub = rospy.Subscriber("/drone/to_forward_cam", Empty, self.to_forward_cam)
        self.to_downward_cam_sub = rospy.Subscriber("/drone/to_downward_cam", Empty, self.to_downward_cam)

        self.tello = Tello()
        self.on_forward_cam = True
        self.has_taken_off = False
        self.rate = rospy.Rate(10)
        self.bridge = CvBridge()

    ## TODO PATHING NODE CALLBACK METHOD
    ## TODO SOUND NODE CALLBACK METHOD 

    def to_takeoff(self):
        self.tello.takeoff()
        self.has_taken_off = True

    def to_forward_cam(self, data):
        if type(self.tello.cap) != type(None):
            self.tello.cap.release()

        self.tello.send_command_with_return("downvision 0")

        self.tello.get_video_capture()

        self.on_forward_cam = True

    def to_downward_cam(self, data):
        if type(self.tello.cap) != type(None):
            self.tello.cap.release()

        self.tello.send_command_with_return("downvision 1")
        self.tello.get_video_capture()
        self.on_forward_cam = False

    def run(self):
        self.tello.connect()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        while not rospy.is_shutdown():
            if not self.has_taken_off:
                self.takeoff_pub(Empty())

            if self.on_forward_cam:
                self.forward_cam_pub.publish(self.bridge.cv2_to_imgmsg(self.tello.cam.read()[1]))
            else:
                self.downward_cam_pub.publish(self.bridge.cv2_to_imgmsg(self.tello.cam.read()[1]))
            self.rate.sleep()

        self.tello.streamoff()

        rospy.spin()


if __name__ == "__main__":
    try:
        drone = Drone()
        drone.run()
    except rospy.ROSInterruptException:
        pass
