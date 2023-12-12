FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install ffmpeg for format conversion
RUN apt-get update && apt-get install -y build-essential cmake  gcc  ffmpeg libsm6 libxext6 libgl1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]