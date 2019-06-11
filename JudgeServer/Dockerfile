FROM registry.docker-cn.com/library/ubuntu:16.04

COPY build/java_policy /etc

RUN buildDeps='software-properties-common git libtool cmake python-dev python3-pip python-pip libseccomp-dev' && \
    apt-get update && apt-get install -y python python3.5 python-pkg-resources python3-pkg-resources gcc g++ $buildDeps && \
    add-apt-repository ppa:openjdk-r/ppa && apt-get update && apt-get install -y openjdk-8-jdk && \
    pip3 install --no-cache-dir psutil gunicorn flask requests && \
    cd /tmp && git clone -b newnew  --depth 1 https://github.com/QingdaoU/Judger && cd Judger && \
    mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python3 setup.py install && \
    apt-get purge -y --auto-remove $buildDeps && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /code && \
    useradd -u 12001 compiler && useradd -u 12002 code && useradd -u 12003 spj && usermod -a -G code spj

HEALTHCHECK --interval=5s --retries=3 CMD python3 /code/service.py
ADD server /code
WORKDIR /code
RUN gcc -shared -fPIC -o unbuffer.so unbuffer.c
EXPOSE 8080
ENTRYPOINT /code/entrypoint.sh
