from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Path di mana FFmpeg menghasilkan file .m3u8 dan segmen .ts
HLS_DIRECTORY = '/hls/stream.m3u8'

@app.route('/hls/<path:filename>')
def serve_hls_files(filename):
    return send_from_directory(HLS_DIRECTORY, filename)

@app.route('/stream.m3u8')
def serve_m3u8():
    return send_from_directory(HLS_DIRECTORY, 'stream.m3u8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
