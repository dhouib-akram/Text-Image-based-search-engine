FROM python:3.9-slim AS python
WORKDIR /front/


COPY ./requirements.txt /front/
RUN  pip3 install -r requirements.txt

FROM python AS python1

COPY /. /front/
EXPOSE 8501
CMD ["streamlit", "run", "./streamlit_app.py"]