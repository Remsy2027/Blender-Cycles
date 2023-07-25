from flask import Flask, request, jsonify
import subprocess
import os
from queue import Queue
from threading import Thread
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app, origins=["*"])
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Create a queue to hold the GLB file requests
request_queue = Queue()

def render_worker():
    while True:
        email, file_path, file_data = request_queue.get()
        # Save the GLB file to the temporary file path on the server
        with open(file_path, 'wb') as f:
            f.write(file_data)
        # Execute the batch file with the email as an argument
        subprocess.Popen(['bash', 'Render.sh', email])
        request_queue.task_done()

# Start the worker thread
worker_thread = Thread(target=render_worker)
worker_thread.daemon = True
worker_thread.start()

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the GLB Upload and Rendering Service"

@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')

    if not email:
        return 'Email not provided', 400

    # Add the email to the queue for processing by the worker thread
    request_queue.put((email, '', ''))

    return 'Rendering started. The image will be sent to {}'.format(email)

@app.route('/upload_glb', methods=['POST'])
def upload_glb():
    email = request.form.get('email')
    print(email)

    glb_file = request.files['glbData']

    # Get the binary data of the GLB file
    file_data = glb_file.read()

    # Save the GLB file to a temporary file path on the server
    temp_file_path = os.path.join('Assets/GLB_Files', f'{email}.glb')

    # Add the request to the queue for processing by the worker thread
    request_queue.put((email, temp_file_path, file_data))

    return jsonify({'message': 'GLB file received and added to the queue for rendering'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
