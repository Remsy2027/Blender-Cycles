import ssl
from flask import Flask, render_template, request, jsonify
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
CORS(app, origins=["*"])

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('/home/remsy/certificate.pem')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')

    if not email:
        return 'Email not provided', 400

    # Execute the batch file
    subprocess.Popen(['bash', 'Render.sh', email])

    return 'Rendering started. The image will be sent to {}'.format(email)


@app.route('/upload_glb', methods=['POST'])

def upload_glb():
    email = request.form.get('email')
    glb_file = request.files['glbData']

    if not email or not glb_file:
        return jsonify({'message': 'Email or GLB file not provided'}), 400

    # Save the GLB file to a folder on the server
    file_path = os.path.join('Assets', f'{email}.glb')
    glb_file.save(file_path)

    # Your code to process the GLB data or trigger other actions based on the email and GLB data

    return jsonify({'message': 'GLB file received and saved successfully'}), 200


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
