FROM aaron465/matplotlib
RUN apt-get update && apt-get install -y python-tk \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ADD plot.py /code/plot.py
