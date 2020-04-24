# Logfilter

Intrusion detection system Logfilter provides flexible configuration and the addition of its own rules for any service.

### Prerequisites

First, you must have installed MySQL and a database created, in which data about user accounts and logs will be stored. Then specify the database information in the configuration file config.py

### Installation

```sh
$ ./install
```

In http server configuration file
```sh
server {
    error_log syslog:server=unix:/dev/log;
    access_log syslog:server=unix:/dev/log;
    ...
}
```

### How to use
After installation, go to http://localhost:8000 and log in using the data you entered during installation. It's all. Now you can add the rules for various services to the rules/ folder. File names must match service names. 
