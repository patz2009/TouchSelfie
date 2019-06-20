'''
Modification of cv2_camera.py for the Yi Action Camera

Capture: Gets full quality images downloaded from camera.
Uses socket to interface with the camera via JSON.
'''

import os, re, sys, time, socket
import wget
import numpy as np
import cv2
from settings import camaddr
from settings import camport

class Camera:
    '''
    Thin wrapper for the cv2 camera interface to make it look like a PiCamera
    '''
    def __init__(self):
		srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv.connect((camaddr, camport))

	srv.send('{"msg_id":257,"token":0}')

	data = srv.recv(512)
	if "rval" in data:
		token = re.findall('"param": (.+) }',data)[0]	
	else:
		data = srv.recv(512)
		if "rval" in data:
			token = re.findall('"param": (.+) }',data)[0]	

	tosend = '{"msg_id":259,"token":%s,"param":"none_force"}' %token
	srv.send(tosend)
	srv.recv(512)

        self.cam = cv2.VideoCapture('rtsp://%s/live' %camaddr)
        time.sleep(.3) ## wait for auto adjust
        self.led = False
        self.previewing = False
        
    def start_preview(self):
        pass
            
    def stop_preview(self):
        self.previewing = False
        
    def capture(self, filename, resize=None):
		'''  100% Untested  '''
		srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		srv.connect((camaddr, camport))

		srv.send('{"msg_id":257,"token":0}')

		data = srv.recv(512)
		if "rval" in data:
			token = re.findall('"param": (.+) }',data)[0]	
		else:
			data = srv.recv(512)
			if "rval" in data:
				token = re.findall('"param": (.+) }',data)[0]	

		tosend = '{"msg_id":769,"token":%s}' %token
		srv.send(tosend)
		
		data = srv.recv(512)
		if "photo_taken" in data:
			url = 'http://' + camaddr + re.findall('"type": "photo_taken" ,"param":"\/tmp\/fuse_d(.+)"}',data)[0]  
		else:
			data = srv.recv(512)
			if "photo_taken" in data:
				url = 'http://' + camaddr + re.findall('"type": "photo_taken" ,"param":"\/tmp\/fuse_d(.+)"}',data)[0]  
		
		wget.download(url, filename)  

    def close(self):
        del self.cam

PiCamera = Camera

def test():
    cap = cv2.VideoCapture('rtsp://%s/live' %camaddr)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print('type "q" to quit')
    test()
