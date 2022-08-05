#!/usr/bin/env python3

import rospy
from std_msgs.msg import Empty
import sounddevice as sd
import math

DURATION = 1
FS = 44100

class Sound:
    def __init__(self):
        rospy.init_node("sound", anonymous=True)
        self.takeoff_sub = rospy.Subscriber("/sound/takeoff", Empty, self.detect)
        self.takeoff_pub = rospy.Publisher("/sound/takeoff_to", Empty, queue_size = 10)

    def detect(self):
        record = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
        sd.wait()

        diffs = []
        for nidx in range(1, record.shape[0]):
            cur = record[nidx]
            prev = record[nidx - 1]
            diffs.append(cur - prev)

        mean = sum(diffs)/len(diffs)
        varianceList = [abs(diff-mean)**2 for diff in diffs]
        variance = math.sqrt(sum(varianceList)/len(diffs))

        if variance > 0.02:
            self.takeoff_pub.publish(Empty())


    def run(self):
        rospy.spin()


if __name__ == "main":
    try:
        detector = Detector()
        detector.run()
    except rospy.ROSInterruptException:
        pass
