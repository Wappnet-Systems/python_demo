import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connected to server----->', sid)
    print('environ----->', environ)


@sio.event
def videostream(sid, data):
    print('I received a message from zmq server')
    sio.emit('videostream_mobile', {'data': data[0]}, room=data[1])


eventlet.wsgi.server(eventlet.listen(('68.183.88.216', 5001)), app)
