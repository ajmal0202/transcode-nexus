FROM python:3.10-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Create app directory
WORKDIR /app

# Copy app code
COPY . .

# Install Flask
RUN pip install flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

