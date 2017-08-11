# Overview

This code will setup Google perfkit and ELK to run benchmarks, collect metrics and visulise the data.

The code can operate in two ways:

- complete setup including ELK
- workload-launcher only which can send to an existing ELK stack

# Complete Setup

## Pre-reqs

The code requires two servers

- workload-launcher: Ubuntu 14.04
- perfkit-elk: Centos 7.3

The workload launcher must be configured for keyless to the centos server using the centos user for ansible to work.

Firewall rules must be as follows:

- workload-launcher: 22
- perfkit-elk: 80 for kibana, 22 and 9200 from the workload-launcher for ansible and elasticsearch

## Get the code

```
git clone https://github.com/UKCloud/perfkit.git
cd perfkit
```

## Environment variable setup

You need to add the elasticsearch endpoint (internal IP of the elasticsearch node setup above):

/home/ubuntu/perfkit/inventories/production/hosts

e.g.
```
[elk]
192.168.0.23 ansible_user=centos
```

/home/ubuntu/perfkit/roles/perfkit/vars/main.yml

e.g.
```
ELASTICSEARCH_ENDPOINT: 192.168.125.5
```

## Run the deployment

Once configure run:

ansible-playbook -i inventories/production/hosts site.yml

# Workload-launcher only

## Pre-reqs

The code requires a single server

- workload-launcher: Ubuntu 14.04

Firewall rules must be as follows:

- workload-launcher: 22

## Get the code

```
git clone https://github.com/UKCloud/perfkit.git
cd perfkit
```

## Environment variable setup

You need to add the elasticsearch endpoint:

/home/ubuntu/perfkit/roles/perfkit/vars/main.yml

e.g.
```
ELASTICSEARCH_ENDPOINT: 23.4.5.6
```

## Run the deployment

Once configure run:

ansible-playbook -i inventories/production/hosts workload-launcher.yml
