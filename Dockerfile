FROM python:3.7-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc
ADD app.py /
#RUN useradd -m -u 8877 mm
#ENV PATH=/home/mm/.local/bin:$PATH
#USER mm
RUN pip install i --no-cache rpi.gpio gpiozero requests
CMD [ "python", "./app.py" ]
