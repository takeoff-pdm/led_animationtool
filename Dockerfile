# FROM Debian:latest


# # Install Python 3.11 and pip
# RUN apt-get install -y python3.11 python3-pip

# # Set the working directory
# WORKDIR /home/led_strip/python_program/led_animationtool

# # Copy the main.py file into the container
# COPY main.py .

# Run the main.py file
# CMD ["python3.11", "main.py"]

# FROM python:3.11-alpine

# WORKDIR .

# RUN apk add --no-cache gcc musl-dev linux-headers

# RUN apk add tzdata
# RUN ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# EXPOSE 5000

# COPY . .

# CMD ["python3.11", "main.py"]


# FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt

# COPY . .

FROM python:3.11

ADD . .

RUN pip install -r requirements.txt

CMD ["python3.11", "main.py"]
