# 🎬 Transcode Nexus - Cloud Video Converter Web App

**Transcode Nexus** is a cloud-based video converter web application built with **Flask** and **FFmpeg**.
It allows users to upload video files, convert them into other formats, and download the result. 
It supports conversion between MP4, AVI, MOV, WEBM, and MKV. The app can be deployed either manually or using Docker, and is accessible via a web browser with NGINX reverse proxy.

------------------------------------------------------------------------------------------------------

## 🚀 Features

- Upload and convert videos in popular formats
- Limit file uploads to 100MB
- Automatically delete files after 1 hour
- Simple Bootstrap frontend with conversion progress
- Dockerized for fast deployment
- Public access via NGINX reverse proxy

-----------------------------------------------------------------------------------------------------

## 📁 Folder Structure

transcode-nexus/
├── app.py # Flask backend
├── templates/
│ └── index.html # Frontend UI
├── uploads/ # Temporary upload storage
├── outputs/ # Temporary output storage
├── Dockerfile # Docker configuration
├── README.md # You're reading it!

------------------------------------------------------------------------------------------------------

# 🧰 Requirements

- OS: Linux (Tested on AWS Amazon Linux 2023)
- Python 3.9+
- FFmpeg
- Flask
- Docker (optional)
- NGINX (for reverse proxy)

------------------------------------------------------------------------------------------------------

# ⚙️ Manual Installation (No Docker)

### ✅ Step 1: Install Python and Flask

```
sudo dnf install python3 python3-pip -y
pip3 install flask
```

### ✅ Step 2: Install FFmpeg (Static Build)
```
cd /usr/local/bin
sudo mkdir ffmpeg && cd ffmpeg

sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
sudo tar -xf ffmpeg-git-amd64-static.tar.xz
```
Add FFmpeg to system path
```
sudo ln -s /usr/local/bin/ffmpeg/ffmpeg-git-*/ffmpeg /usr/bin/ffmpeg
```
Verify installation
```
ffmpeg -version
```

### ✅ Step 3: Clone This Repository
```
git clone https://github.com/ajmal0202/transcode-nexus.git
cd transcode-nexus
```
### ✅ Step 4: Run Flask App
```
python3 app.py
```
Then open in browser:
🌐 http://<your_server_ip>:5000 (Make sure port 5000 is open in your EC2 security group)

### ✅ Step 5: Set Up NGINX Reverse Proxy
```
sudo yum install nginx -y
sudo systemctl enable --now nginx
```
Create config file:
```
sudo vim /etc/nginx/conf.d/transcode-nexus.conf
```
Paste:
```
server {
    listen 80;
    server_name _;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
    }
}
```

Then restart NGINX:
```
sudo systemctl restart nginx
```
Your app will now be live at:
🌍 http://<your_public_ip>

------------------------------------------------------------------------------------------------------

# 🐳 Docker-Based Deployment (Recommended)

### ✅ Step 1: Install Docker
```
sudo yum install -y docker
sudo systemctl enable --now docker
```
### ✅ Step 2: Clone This Repository
```
git clone https://github.com/ajmal0202/transcode-nexus.git
cd transcode-nexus
```
### ✅ Step 3: Build Docker Image
```
sudo docker build -t transcode-nexus .
```
### ✅ Step 4: Run Docker Container
```
sudo docker run -d --network=host --name nexus transcode-nexus
```
App will now be available on:
📍 http://<your_server_ip>:5000 (Make sure port 5000 is open in your EC2 security group)

### ✅ Step 5: Set Up NGINX
Use the same NGINX steps from the manual installation section to make the app public on port 80.

------------------------------------------------------------------------------------------------------

🧹 Auto File Deletion
Uploaded and converted files are automatically deleted after 1 hour using Python's threading module.

------------------------------------------------------------------------------------------------------

⚠️ Notes
Make sure port 80 is open in your EC2 security group

File size limit is enforced both on client and server (100MB max)

You must have FFmpeg in PATH for manual install

Use tmux or screen if you want to keep your app running after logout

------------------------------------------------------------------------------------------------------
