#!/bin/bash

# Check the OS version and install according packages manually
debian_version=`egrep "jessie|strech" /etc/os-release`
if [ `echo $debian_version|grep -c "jessie"` == 1  ]
then
    echo "No Kafka support provided for Raspbian Jessie"
elif [ `echo $debian_version|grep -c "stretch"` == 1  ]
then
    wget -P /tmp/ http://ftp.de.debian.org/debian/pool/main/libr/librdkafka/librdkafka1_0.11.6-1~bpo9+1_armhf.deb
    wget -P /tmp/ http://ftp.de.debian.org/debian/pool/main/libr/librdkafka/librdkafka++1_0.11.6-1~bpo9+1_armhf.deb
    wget -P /tmp/ http://ftp.de.debian.org/debian/pool/main/libr/librdkafka/librdkafka-dev_0.11.6-1~bpo9+1_armhf.deb
    cd /tmp/
    LIBRDKAFKA=$(sudo dpkg -i librdkafka1_0.11.6-1~bpo9+1_armhf.deb)
    if [ "" == "$LIBRDKAFKA"  ]; then
        echo "Cannot install librdkafka1_0.11.6. Aborting..."
        exit -1
    fi
    LIBRDKAFKA++=$(sudo dpkg -i librdkafka++1_0.11.6-1~bpo9+1_armhf.deb)
    if [ "" == "$LIBRDKAFKA++"  ]; then
        echo "Cannot install librdkafka++1_0.11.6. Aborting..."
        exit -1
    fi
    LIBRDKAFKADEV=$(sudo dpkg -i librdkafka-dev_0.11.6-1~bpo9+1_armhf.deb)
    if [ "" == "$LIBRDKAFKADEV"  ]; then
        echo "Cannot install librdkafka-dev_0.11.6. Aborting..."
        exit -1
    fi

else
    echo "No support provided for this version!"
    echo "Please upgrade either to Jessie or Stretch"
    exit -1

fi

# Print the Kernel version
kernel_version=`uname -a|awk '{print $3}'`
if [ $kernel_version == "4.4"  ]
then
    echo "Kernel version: " $kernel_version
else
    echo "Kernel version: " $kernel_version
fi

# Install requirements with pip
for package in $(cat requirements.txt); do
    sudo pip install package
    if [ $? -ne 0  ]; then
        echo "Could not install $package. Aborting..."
        exit 1
    fi
done

# Install MESP as a systemd service
PWD=$(pwd)
# Edit Unit file
CMD=$PWD"/py/agent.py -f "$PWD"/conf/agent.ini"
STR=`awk -v var="$CMD" '{if(/ExecStart=/) {print$0var}}' $PWD/conf/agent.service`
echo $STR
sed -i "s:ExecStart=:$STR:g" $PWD/conf/agent.service

# Link Unit file to systemd dir
echo "Linking file "$PWD"/py/agent.py to systemd directory"
chmod 664 conf/agent.service
sudo ln -s $PWD/conf/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
echo "Done!"
