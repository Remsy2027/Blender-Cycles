import ssl
import queue
import threading
from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
CORS(app, origins=["*"])

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('/home/remsy/certificate.pem')

# Create a queue to store incoming requests
request_queue = queue.Queue()

def render_worker():
    while True:
        # Get the next request from the queue (blocks if the queue is empty)
        email, glb_file = request_queue.get()

        # Remove the word after @ from the email address
        email_without_domain = email.split('@')[0]

        # Save the GLB file to a folder on the server
        file_path = os.path.join('Assets', f'{email_without_domain}.glb')
        glb_file.save(file_path)

        # Your code to process the GLB data or trigger other actions based on the email and GLB data
        # For example, you can call a function or execute a script to start rendering
        subprocess.Popen(['bash', 'Render.sh', email])

        # Mark the task as done in the queue
        request_queue.task_done()

# Start the worker thread to process requests
worker_thread = threading.Thread(target=render_worker)
worker_thread.daemon = True
worker_thread.start()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload_glb', methods=['POST'])
def upload_glb():
    email = request.form.get('email')
    glb_file = request.files['glbData']

    if not email or not glb_file:
        return jsonify({'message': 'Email or GLB file not provided'}), 400

    # Add the request to the queue for processing by the worker thread
    request_queue.put((email, glb_file))

    return jsonify({'message': 'GLB file received and added to the queue for rendering'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
