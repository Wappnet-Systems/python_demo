import ffmpeg_streaming
from ffmpeg_streaming import Formats
video = ffmpeg_streaming.input('/var/www/html/videostreamiot/output1.avi')

dash = video.dash(Formats.h264())
dash.auto_generate_representations()
dash.output('/var/www/html/videostreamiot/dash_video/dash.mpd')


