import socketio
import imagezmq
import cv2
import base64

sio = socketio.Client()
sio.connect('http://68.183.88.216:5001/')

# from . import wsgi_app
imageHub = imagezmq.ImageHub(open_port='tcp://68.183.88.216:5555')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output1.avi', fourcc, 12.0, (320, 240))
sio.sleep(1.0)

# out = cv2.VideoWriter('appsrc ! videoconvert ! '
#  'x264enc noise-reduction=10000 speed-preset=ultrafast 
#   tune=zerolatency ! '
#  'rtph264pay config-interval=1 pt=96 !'
#  'tcpserversink host=68.183.80.245 port=5000 sync=false',
#  0, 12.0, (320,240))

while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (deviceId, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    # cv2.imshow('frame', frame)

    # out.write(frame)
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    base64_message = jpg_as_text.decode('ascii')

    # print(jpg_as_text)
    # exit()

    sio.emit('videostream', data=['data:image/jpg;base64,' + base64_message, deviceId])

    cv2.waitKey(1)

    # if a device is not in the last active dictionary then it means
    # that its a newly connected device
    # if rpiName not in lastActive.keys():
    # 	print("[INFO] receiving data from {}...".format(rpiName))
    # record the last active time for the device from which we just
    # received a frame
    # lastActive[rpiName] = datetime.now()
