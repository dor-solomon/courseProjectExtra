FROM python:3.11-alpine3.18
LABEL authors="dor"
ARG username
ARG password
ARG host
ENV username=${username}
ENV password=${password}
ENV host=${host}
COPY db_connector.py /
COPY rest_app.py /
EXPOSE 5000
RUN pip install flask pypika pymysql cryptography

CMD python rest_app.py ${username} ${password} ${host}