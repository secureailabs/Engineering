#! /bin/bash

sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo docker run hello-world

echo "Printing the current module"
echo $module

mkdir -p /opt/certs
cp nginx-selfsigned.crt /opt/certs
cp nginx-selfsigned.key /opt/certs
cp vm_initializer.py /opt/
cp decrypt_file.py /opt/
cp Run.sh /opt/
chmod +x /opt/Run.sh

docker build . -t $module

(crontab -l; echo "@reboot cd /opt; sudo ./Run.sh > VmImageInit.log") | crontab -

# To cleanup the user details
/usr/sbin/waagent -force -deprovision+user && export HISTSIZE=0 && sync
