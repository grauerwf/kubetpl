FROM debian:bullseye-slim
MAINTAINER grauerwf <grauerwf@gmail.com>

RUN apt update -y && apt install -y openssh-client python3 python3-dev python3-pip git gcc cargo wget curl &&  \
    pip3 install --no-cache-dir --upgrade pip &&  \
    pip3 install --no-cache-dir --upgrade awscli kubetpl &&  \
    wget "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" -O /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl &&  \
    wget https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.5.9/aws-iam-authenticator_0.5.9_linux_amd64 -O /usr/local/bin/aws-iam-authenticator  && chmod +x /usr/local/bin/aws-iam-authenticator