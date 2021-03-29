import urllib.request
import cv2
import numpy as np
URL='http://10.42.0.70:8080/shot.jpg'

while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
    img = cv2.imdecode(img_arr,-1)
    img = cv2.resize(img,(640,480))
    cv2.imshow('IPWebcam',img)

    # Close and break the loop after pressing "q" key
    if cv2.waitKey(1) &0XFF == ord('q'):
        break

# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()
