FROM python:3

MAINTAINER zlikun <zlikun-dev@hotmail.com>

ENV VERSION v1.0.0
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017

WORKDIR /opt/__app__

ADD requirements.txt /opt/

RUN pip install -r /opt/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && rm -f /opt/requirements.txt

ADD ./*.py  /opt/__app__/
ADD ./web   /opt/__app__/web

EXPOSE 80

ENTRYPOINT ["python", "web/web.py"]