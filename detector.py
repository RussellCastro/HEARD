import cv2

class Detector: # Is this supposed to be a class..? I still dunno... 


    def __init__( self ): # Whenever we create a Detector object...
        self.hog = cv2.HOGDescriptor() # Create an instance of the HOGDescriptor class...
        self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() ) # And set its SVMDetector so that it detect humans...

        self.EMERGENCY_THRESHOLD = 1.0 # And set the emergency threshold to 1.0... any value greater than this for any 'human' detected will mean there's an emergency

    
    def detect( self, frame ): # Whenever we wanna detect if there are humans in a frame, frame (frame, a matrix / tensor / image )
        humans, values = self.hog.detectMultiScale( frame,                # Detect for humans in the image and store the 
                                                    winStride = ( 2, 2 ), # x, y, w, h, and value of each of the 'humans' 
                                                    padding = ( 4, 4 ),   # detected in the variables humans ( a tuple, ( x, y, w, h ) )
                                                    scale = 1.01 )        # and values ( the values, certainties that each detected 'human' is a human )

        for ( x, y, w, h ), value in zip( humans, values ): # Iterate over humans and values at the same time...
            cv2.rectangle( frame,            # And draw rectangles where the humans supposedly are...
                           ( x, y ), 
                           ( x + w, y + h ), 
                           ( 0, 0, 255 ), 
                           1 )

            frame = cv2.putText( frame,                    # And put the 'value' value of every human next to their rectangle.
                                 str( value ), 
                                 ( x, y ), 
                                 cv2.FONT_HERSHEY_COMPLEX, 
                                 1.0, 
                                 ( 0, 0, 255 ),
                                 1 )

            if value >= self.EMERGENCY_THRESHOLD: # If any 'value' repressenting the likelihood of a human existing in that rectangle  
                print( "THERE'S AN EMERGENCY" )   # exceeds the EMERGENCY_THRESHOLD, there's an emergency.