FROM debian:bullseye-slim
MAINTAINER grauerwf <grauerwf@gmail.com>

RUN apt update -y && apt install -y openssh-client python3 python3-dev python3-pip git gcc cargo wget curl &&  \
    pip3 install --no-cache-dir --upgrade pip &&  \
    pip3 install --no-cache-dir --upgrade awscli kubetpl &&  \
    wget -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" -O /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl &&  \
    wget -q https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/aws-iam-authenticator -O /usr/local/bin/aws-iam-authenticator  && chmod +x /usr/local/bin/aws-iam-authenticator