#!/usr/bin/bash
cat > mitb.lxd.profile.yaml << EOF
name: mitb
description: ""
config:
  user.user-data: |
    #cloud-config
    users:
      - name: "ubuntu"
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /usr/bin/bash
        ssh_authorized_keys:
          - "$pubkey"
    write_files:
      - path: /var/lib/cloud/scripts/per-once/script.sh
        content: |
          #!/usr/bin/bash
          apt -y update
          apt -y upgrade
          apt -y install snap
          snap install google-cloud-sdk --classic
          snap install aws-cli --classic
          apt -y install bzip2 dmidecode less nfs-client
          mkdir -p /home/ubuntu/.config
          mkdir -p /home/ubuntu/.ssh
          touch /home/ubuntu/.ssh/id_rsa
          touch /home/ubuntu/.ssh/id_rsa.pub
          tar -jxvf /root/gcloud.tar.bz2 -C /home/ubuntu/.config/
          chown -R ubuntu:ubuntu /home/ubuntu
          mkdir -p /opt/pm
          cd /opt/pm
          gcloud config set account joel@perpetualmedia.com
          gcloud auth activate-service-account lxd-installer-key@perpetualmedia-1726.iam.gserviceaccount.com --key-file /home/ubuntu/.config/gcloud/pass.json
          gcloud source repos clone scripts --project=perpetualmedia-1726
        permissions: 0755
      - path: /home/ubuntu/.ssh/id_rsa
        content: |
          $privatekey

        permissions: '0600'
        owner: ubuntu:ubuntu

      - path: /home/ubuntu/.ssh/id_rsa.pub
        content: |
          $pubkey 
        permissions: '0644'
        owner: ubuntu:ubuntu
    runcmd:
      - mkdir -p /home/ubuntu/.ssh
      - chown -R ubuntu:ubuntu /home/ubuntu/.ssh
      - chmod 700 /home/ubuntu/.ssh
      - chmod 600 /home/ubuntu/.ssh/id_rsa
      - chmod 644 /home/ubuntu/.ssh/id_rsa.pub

    final_message: "Cloud-init completed successfully."
devices:
  eth0:
    name: eth0
    network: lxdbr0
    type: nic
  root:
    path: /
    pool: default
    type: disk
used_by:
- /1.0/instances/mitb1
EOF
cat mitb.lxd.profile.yaml | lxc profile edit mitb
lxc launch ubuntu:24.04 mitbs -p mitb
cd /home/jj/.config/
tar --exclude logs -jcvf /tmp/gcloud.tar.bz2 gcloud
lxc file push /tmp/gcloud.tar.bz2 mitbs/root/gcloud.tar.bz2
pubkey=`cat /home/jj/.ssh/id_rsa.pub`
privatekey=`cat /home/jj/.ssh/id_rsa`
