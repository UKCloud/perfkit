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

> Please Note: If you are creating your servers on openstack, then please use security groups for implementing firewall rules

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
## Check if Ansible is installed
If you are downloading a minimal iso image of ubuntu then most probably, there is not ansible installed.
Check by running following command:
```
ansible --version
```

## Update ansible if less than version 2.2

If ansible is installed and the version is less than 2.2 then please make sure that you have the latest version of ansible. The playbooks will not work for versions below 2.2
Run following commnds to install latest version of ansible
```
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

## Run the deployment
Once configure run:
```
ansible-playbook -i inventories/production/hosts site.yml
```

## Configure cloud credentials

### OpenStack
You'll need to have downloaded a valid OpenStackRC file and placed it in /home/ubuntu/openstack_rc.sh

### AWS
run:
```
aws configure
```

### Azure
run:
```
azure login
```

### Google Cloud
run:
```
gcloud init
```

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
```
ansible-playbook -i inventories/production/hosts workload-launcher.yml
```

> Please note that at the end of deployment a cronjob is created for the benchmark to run at 5:00AM and 10:00 PM everyday.

# Running the benchmarks

To run the benchmarks run:

```
usage: perfkit.py [-h] --cloud_provider CLOUD_PROVIDER --config CONFIG

optional arguments:
  -h, --help            show this help message and exit
  --cloud_provider CLOUD_PROVIDER
                        Service provider to benchmark [OpenStack |
                        VMware | AWS-UK | AWS-US | Azure | Google]
  --config CONFIG       Path to perfkit yaml config
```

Example: Assuming that perfkit is installed in /home/ubuntu/perfkit
```
./perfkit.py --config /home/ubuntu/perfkit/region2.config --cloud_provider OpenStack
```

## Following data is required for the benchmarks to run first time
| Key | Value |
|----|----|
| flavor_name | t1.small |
| zones | 00021-2 |
| image | '"Ubuntu 14.04"' |
| openstack_network | net-1 |
| openstack_volume_type | TIER1 |


