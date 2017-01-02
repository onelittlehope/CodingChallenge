FROM ubuntu


RUN apt-get update && apt-get install -y \
    python3-pip \
  && rm -rf /var/lib/apt/lists/*


COPY "./" "/root"


RUN pip3 install -r /root/requirements.txt


EXPOSE 8081


WORKDIR /root


CMD ["python3","runserver.py"]
