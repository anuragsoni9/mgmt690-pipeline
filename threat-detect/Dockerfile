FROM alpine:3.6

RUN set -x \
    && apk update \
    && apk --no-cache add python3 \
    && ln -s /usr/bin/python3.6 /usr/bin/python \
    && find /usr/lib/python3.6 -name __pycache__ | xargs rm -r \
    && rm -rf /root/.[acpw]* 

ADD threatdetect.py /code/threatdetect.py
