# Installing OSQA-JSON on Centos 5.5

Install the EPEL repo for yum support:

    rpm -Uvh http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-4.noarch.rpm

Install the essential dependencies:

    yum install mysql-server mysql-devel httpd httpd-devel python26 python26-devel python26-distribute

Install required Python modules:

    easy_install-2.6 django MySQL-python html5lib markdown

Download and compile mod_wsgi:

    cd /opt
    wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz
    tar zxvf mod_wsgi-3.3.tar.gz
    cd mod_wsgi-3.3
    ./configure --with-python=/usr/bin/python26
    make
    make install

Activate mod_wsgi Apache module:

    echo 'LoadModule wsgi_module modules/mod_wsgi.so' > /etc/httpd/conf.d/mod_wsgi.conf
    chown -R apache /etc/httpd/logs
    chmod -R 775 /etc/httpd/logs

Clone and configure osqa-json repo:

    cd /opt
    git clone git://github.com/philchristensen/osqa-json.git osqa_json
    cd osqa_json
    chgrp apache log
    chmod 775 log
    mkdir cache
    chgrp apache cache
    chmod 775 cache

Enable VHOSTs on Apache:

```bash
    echo >> /etc/httpd/conf/httpd.conf
    echo 'NameVirtualHost *:80' >> /etc/httpd/conf/httpd.conf
    echo 'Include /etc/httpd/conf/vhosts/*.conf' >> /etc/httpd/conf/httpd.conf
```

Create apache VHOST directory, add symlink for apache config:

```bash
    mkdir /etc/httpd/conf/vhosts
    ln -s /opt/osqa_json/apache-vhost.conf /etc/httpd/conf/vhosts/osqa.ct.srv.kodingen.com.conf
```

Start up MySQL

```bash
    /etc/init.d/mysqld start
```

Secure MySQL installation:

```bash
    mysql_secure_installation
```

Connect to mysql as root, execute:

```sql
    CREATE DATABASE osqa;
    USE osqa;
    GRANT ALL ON osqa.* TO osqa@localhost IDENTIFIED BY 'liejujryn';
    FLUSH PRIVILEGES;
```

Install OSQA database (answer 'no' when asked to create a superuser):

```bash
    python manage.py syncdb
```

Connect to mysql as root again, execute:

```sql
    UPDATE auth_user SET is_superuser=1, is_staff=1 WHERE username = 'admin';
```

Start up Apache:

```bash
    /etc/init.d/httpd start
```

Visit home page to test site:

    http://osqa.ct.srv.kodingen.com/osqa/

Create a user account:

    http://osqa.ct.srv.kodingen.com/osqa/account/local/instantiate/?username=admin&email=admin@example.com

Give yourself a test Kodingen cookie:

    http://osqa.ct.srv.kodingen.com/osqa/account/local/authenticate-test/?username=admin

Login to OSQA:

    http://osqa.ct.srv.kodingen.com/osqa/account/local/authenticate/?url=/osqa
