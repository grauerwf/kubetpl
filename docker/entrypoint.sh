#!/usr/bin/env sh

if [ -z "${KUBE_CONFIG}" ]; then
  echo "KUBE_CONFIG" variable is unset, exiting...
  exit 1
fi

echo "${KUBE_CONFIG}" | base64 -d > ~/.kube/config


if [ -z "${SSH_KEY_PRIVATE}" ]; then
echo "SSH_KEY_PRIVATE" variable is unset, exiting...
exit 1
fi

echo "${SSH_KEY_PRIVATE}" | base64 -d > ~/.ssh/id_rsa
ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/id_rsa
