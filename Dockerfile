FROM python:3.8

USER root
RUN apt update && apt upgrade -y
RUN cd /mnt
Copy hr_app /mnt/hr_app
RUN mkdir /mnt/hr_app/files
RUN /usr/local/bin/pip3.8 install -r /mnt/hr_app/requirements.txt

EXPOSE 5000
ENTRYPOINT /usr/local/bin/python3.8 /mnt/hr_app/run.py
