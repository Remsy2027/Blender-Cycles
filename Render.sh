#!/bin/bash

email=$1

# Extract the username from the email address
username=$(echo "$email" | cut -d '@' -f 1)

script_path="Render.py"
output_path="/path/to/Render_Images/${username}_Render_Image.png"

# Run Blender to render the image
blender -b -P "$script_path" -- "$email"

# Send the rendered image via email
python "send_email.py" "$email" "$output_path"
