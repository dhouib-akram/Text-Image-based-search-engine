FROM python:3.9 AS python
WORKDIR /backend
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
FROM python AS python1
COPY requirements.txt /backend
RUN pip3 install -r requirements.txt

COPY  . /backend

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000", "--reload"]