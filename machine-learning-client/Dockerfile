FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install build-essential, gcc, and cmake for face_recognition package
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gcc \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]