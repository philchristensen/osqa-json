# Installing OSQA-JSON on Centos 5.5

Install the EPEL repo for yum support:

    rpm -Uvh http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-4.noarch.rpm

Install the essential dependencies:

    yum install mysql-server mysql-devel httpd httpd-devel python26 python26-devel python26-distribute

Install required Python modules:

    easy_install-2.6 django MySQL-python html5lib markdown

Clone osqa-json repo:

    cd /opt
    git clone git://github.com/philchristensen/osqa-json.git osqa_json

Enable VHOSTs on Apache:

    echo >> /etc/httpd/conf/httpd.conf
    echo 'NameVirtualHost *:80' >> /etc/httpd/conf/httpd.conf
    echo 'Include /etc/httpd/conf/vhosts/*.conf' >> /etc/httpd/conf/httpd.conf

Create apache VHOST directory:

    mkdir /etc/httpd/conf/vhosts