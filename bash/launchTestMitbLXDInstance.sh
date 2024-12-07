#!/usr/bin/bash
if [ -z "$1" ]
  then
    echo "No Host argument supplied"
  else
    HOST=$1
fi
pubkey=`cat /home/jj/.ssh/id_rsa.pub`
privatekey=`cat /home/jj/.ssh/id_rsa`
cat mitb.lxd.profile.yaml | lxc profile edit mitb
lxc launch ubuntu:24.04 $HOST -p mitb
cd /home/jj/.config/
tar --exclude logs -jcvf /tmp/gcloud.tar.bz2 gcloud
tar -jcvf /tmp/vim.tar.bz2 /home/jj/.vim /home/jj/.vimrc
lxc file push /tmp/gcloud.tar.bz2 $HOST/root/gcloud.tar.bz2
lxc file push /tmp/vim.tar.bz2 $HOST/root/vim.tar.bz2
lxc file push /home/jj/.ssh/id_rsa $HOST/root/.ssh/
lxc file push /home/jj/.ssh/id_rsa.pub $HOST/root/.ssh/

