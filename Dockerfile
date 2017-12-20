From python:3.5.2

MAINTAINER chenshangtao@rawstone.com

RUN mkdir -p /srv/www/xk-ms

#COPY app.py hooks Makefile README requirements.txt schema settings.py TODO data __init__.py model README2 resources schema-allinone.yaml test unit.py /srv/www/xk-ms/

COPY . /srv/www/xk-ms/


WORKDIR /srv/www/xk-ms/

ENV HTTP_PORT=8000
ENV MONGO_HOST=127.0.0.1
ENV MONGO_PORT=27017
ENV MONGO_DB=cb
ENV MONGO_DB_USER=user
ENV MONGO_DB_PASSWD=passwd
ENV TZ=Asia/Shanghai

RUN cd /srv/www/xk-ms/ \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --requirement requirements.txt

EXPOSE 8000

CMD ["bash","-c","uwsgi uwsgi.ini"]
