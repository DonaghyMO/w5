FROM amd64/python:3.8.2
MAINTAINER SanJin<lauixData@gmail.com>
WORKDIR /w5
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    mv /etc/apt/source.list /etc/apt/source.list.bk &&  \
    echo "# deb http://snapshot.debian.org/archive/debian/20200422T000000Z buster main\ndeb http://deb.debian.org/debian buster main\n# deb http://snapshot.debian.org/archive/debian-security/20200422T000000Z buster/updates main\ndeb http://security.debian.org/debian-security buster/updates main\n# deb http://snapshot.debian.org/archive/debian/20200422T000000Z buster-updates main\ndeb http://deb.debian.org/debian buster-updates maindeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse\ndeb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse" >> /etc/apt/resource.list  \
    && sed -i 's/\\n/\n/g' /etc/apt/source.list && apt update && apt install nmap sudo
COPY ./docker/supervisord.conf /etc/supervisord.conf
COPY . .
CMD ["supervisord", "-c", "/etc/supervisord.conf"]