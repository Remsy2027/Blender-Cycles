#!/bin/bash

email=$1

# Extract the username from the email address
username=$(echo "$email" | cut -d '@' -f 1)
current_datetime=$(date +"_%Y/%d-%m/%H-%M_")

script_path="Render.py"
output_path="Assets/Render_Images/${username}${current_datetime}Render_Image.PNG"

# Run Blender to render the image
blender -b -P "$script_path" -- "$email"

# Send the rendered image via email
python3 "send_email.py" "$email" "$output_path"
