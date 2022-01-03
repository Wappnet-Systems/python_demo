import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)



@sio.event
def connect(sid, environ):
    print('connect ', sid)
    

@sio.event
def move_device(sid,data):
    print('movement_detail:')
    print(data)
    #print(data)
    sio.emit('device_move', {'data': data})

@sio.event
def device_feedback(sid,data):
    print('movement_detail:')
    print(data)
    #print(data)
    sio.emit('device_feedback_mobile', {'data': data})
    
eventlet.wsgi.server(eventlet.listen(('68.183.80.245', 5002)), app)	
