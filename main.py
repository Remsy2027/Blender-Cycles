from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')

    if not email:
        return 'Email not provided', 400

    # Execute the batch file
    subprocess.Popen(['render.bat', email])

    return 'Rendering started. The image will be sent to {}'.format(email)

if __name__ == '__main__':
    app.run(debug=True)
