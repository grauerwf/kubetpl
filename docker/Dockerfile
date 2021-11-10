FROM alpine:3.7
MAINTAINER Serhii Puronen <serhii.puronen@ralabs.org>

RUN apk --update add openssh python3 git\
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir --upgrade awscli kubetpl \
    && rm -rf /var/cache/apk/*
RUN wget -q https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt -O -)/bin/linux/amd64/kubectl -O /usr/local/bin/kubectl &&  \
    chmod +x /usr/local/bin/kubectl &&  \
    wget -q https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/aws-iam-authenticator -O /usr/local/bin/aws-iam-authenticator  &&  \
    chmod +x /usr/local/bin/aws-iam-authenticator
RUN mkdir -p /root/.kube
#ADD config /root/.kube/config
