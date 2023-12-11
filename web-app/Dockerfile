FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]