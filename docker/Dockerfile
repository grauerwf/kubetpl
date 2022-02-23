FROM debian:bullseye-slim
MAINTAINER grauerwf <grauerwf@gmail.com>

RUN apt update -y && apt install -y openssh-client python3 python3-dev python3-pip git gcc rustc cargo wget curl &&  \
    pip3 install --no-cache-dir --upgrade pip &&  \
    pip3 install --no-cache-dir --upgrade awscli kubetpl &&  \
    rm -rf /var/cache/apk/* &&  \
    wget -q https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt -O -)/bin/linux/amd64/kubectl -O /usr/local/bin/kubectl &&  \
    chmod +x /usr/local/bin/kubectl &&  \
    wget -q https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/aws-iam-authenticator -O /usr/local/bin/aws-iam-authenticator  &&  \
    chmod +x /usr/local/bin/aws-iam-authenticator && \
    wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-373.0.0-linux-x86_64.tar.gz && \
    tar -xf google-cloud-sdk-373.0.0-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh
ENV PATH="/google-cloud-sdk/bin:${PATH}"