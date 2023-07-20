import ssl
from flask import Flask, request, jsonify
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

@app.route('/upload_glb', methods=['POST'])
def upload_glb():
    email = request.form.get('email')
    glb_file = request.files['glbData']

    if not email or not glb_file:
        return jsonify({'message': 'Email or GLB file not provided'}), 400

    # Save the GLB file to a folder on the server
    file_path = os.path.join('Assets', f'{email}.glb')
    glb_file.save(file_path)

    # Check if the GLB file is received in the Assets folder and start rendering
    if os.path.exists(file_path):
        # Your code to trigger the rendering process using the email and GLB data
        # For example, you can call a function or execute a script to start rendering
        subprocess.Popen(['bash', 'Render.sh', email])
        return jsonify({'message': 'GLB file received and rendering started'}), 200
    else:
        return jsonify({'message': 'Failed to save GLB file'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
