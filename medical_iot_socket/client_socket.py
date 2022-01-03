import socketio
sio = socketio.Client(logger=True, engineio_logger=True)
sio.connect('http://68.183.80.245:5002')
#sio.sleep(1.0)
#sio.emit('videostream', {'data': 'test'})

@sio.event
def videostream_mobile(data):
    print('I received a message! from socket frame stream')
    print(data)
    
@sio.event
def device_move(data):
    print('I received a message! from socket frame stream')
    print(data)
    
    
