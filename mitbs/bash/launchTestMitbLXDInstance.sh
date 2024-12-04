#!/usr/bin/bash
pubkey=`cat /home/jj/.ssh/id_rsa.pub`
privatekey=`cat /home/jj/.ssh/id_rsa`
cat mitb.lxd.profile.yaml | lxc profile edit mitb
lxc launch ubuntu:24.04 mitbs -p mitb
cd /home/jj/.config/
tar --exclude logs -jcvf /tmp/gcloud.tar.bz2 gcloud
lxc file push /tmp/gcloud.tar.bz2 mitbs/root/gcloud.tar.bz2
lxc file push /home/jj/.ssh/id_rsa mitbs/root/.ssh/
lxc file push /home/jj/.ssh/id_rsa.pub mitbs/root/.ssh/

