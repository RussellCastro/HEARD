import cv2 ## OpenCV Library, important in general & here, especially, for the HOGDescriptor and SVMDetector
from djitellopy import Tello ## To interact with the tello
import time ## to rate things

tello = Tello() ## Instantiate the tello
tello.connect() ## Connect to the tello
tello.send_command_with_return( "downvision 1" ) ## Switch to the tello's down-facing camera
tello.streamon() ## Start streaming! If you get the chance, later on, when it's no longer important, use "tello.streamoff()"

frame_read = tello.get_frame_read() ## Create a BackgroundFrameRead object to access the .frame of later!

hog = cv2.HOGDescriptor() ## Instantiate a HOGDescriptor!
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() ) ## Set the HOGDescriptor's SVMDetector to the HOGDescriptor's default people detector!

### 
### THIS IS WHERE THINGS WILL CHANGE DRASTICALLY IN OUR ACTUAL APPLICATION, BTW
###

tello.takeoff()           ## The drone needs to fly around and look around the house in our application. here,
tello.move_up( 50 )       ## I just have the drone takeoff(), move_up(), and move_forward(), which was perfect for testing,
tello.move_forward( 100 ) ## But I know we'll need to change this to make it work for what we need to do 

i = 1 ## We won't need this, it was just for testing.

while True: ## Our loop in ROS will probably be a while not rospy.is_shutdown() or whatever, and not this. this while True: was just for testing in a single script
    frame = frame_read.frame ## This will also be the first line of our eventual final while-loop, as, of course, we'll need the frame to find the person
    humans = hog.detectMultiScale( frame,               ## This is where we detect the humans in the image and save any and all humans found to a iterable
                                   winStride = ( 4, 4 ),## of ( x, y, w, h ) iterables each representing the x, y, w, and h of the rectangles of the humans in 
                                   padding = ( 4, 4 ),  ## the frame. It should be noted that this detector can detect people at an angle or not "upright" from its
                                   scale = 1.21 )[ 0 ]  ## perspective, but the rectangles of these people will be wonky. The drone loves being not too close 
                                                        ## to the people in the frame, also. It works much better at a sizeable but not too sizeable distance from the
                                                        ## people in the frame. At the end of this doc-filed file, I'll have a bunch of articles containing the info 
                                                        ## I found about all of this. There's one that specifically delves into how the parameters work and what they do
                                                        ## and what not. I'll put a * next to it!
    if len( humans ) > 0: ## Just for testing, not actually necessary unless you want to draw rectangles on any humans found.
        x, y, w, h = humans[ 0 ] ## ||
        cv2.rectangle( frame, ( x, y ), ( x + w, y + h ), ( 255, 0, 255 ), 1 ) ## ||
        cv2.imwrite( f"human-12-{i}.png", frame ) ## ||
        i += 1 ## ||

    time.sleep( 0.1 ) ## Keeps things going at a rate of (10 hertz?)

## https://www.etutorialspoint.com/index.php/316-human-body-detection-program-in-python-opencv 
## https://data-flair.training/blogs/python-project-real-time-human-detection-counting/
## https://pyimagesearch.com/2015/11/16/hog-detectmultiscale-parameters-explained/ *