FROM python:3.6
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx && nginx
# ADD nginx-1.15.2.tar.gz /usr/src
# RUN cd /usr/src/nginx-1.15.2 \
#     && mkdir /usr/local/nginx \
#     && ./configure --prefix=/usr/local/nginx && make && make install \
#     && ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/ \
#     && nginx \
#     && rm -rf /usr/src/nginx-1.15.2
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN mkdir /web
COPY ./Flask-Tutorial /web
WORKDIR /web
RUN ls && pip install uwsgi \
    && pip install -r requirements.txt \
    && chmod +x start.sh \
    && mkdir instance \
    && cd instance \
    && touch flaskr.sqlite \
    && cd ..
CMD ./start.sh
EXPOSE 80


