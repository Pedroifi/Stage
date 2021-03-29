import os
import cv2
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--person_name", type=str, required=True,
	help="Name of the person that is recording")
args = vars(ap.parse_args())

#Capture video from webcam
vid_capture = cv2.VideoCapture(0)
vid_cod = cv2.VideoWriter_fourcc(*'XVID')

try:
    # creating a folder named video 
    if not os.path.exists('video'): 
        os.makedirs('video') 
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of video') 

output = cv2.VideoWriter("video/" + args["person_name"] + ".mp4", vid_cod, 30.0, (640,480))

while(True):
     # Capture each frame of webcam video
     ret,frame = vid_capture.read()
     cv2.imshow("My cam video", frame)
     output.write(frame)
     # Close and break the loop after pressing "q" key
     if cv2.waitKey(1) &0XFF == ord('q'):
         break

# close the already opened camera
vid_capture.release()
# close the already opened file
output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()