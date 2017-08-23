#!/usr/bin/env python

import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cloud_provider", help='UKCloud-OpenStack, UKCloud-vCloud, AWS-UK, AWS-US, Azure, Google', required=True)
parser.add_argument("--config", help='UKCloud-OpenStack, UKCloud-vCloud, AWS-UK, AWS-US, Azure, Google', required=True)
ARGS = parser.parse_args()

class ukcloudPerfkit():

    def __init__(self):
        self.config = self.import_yaml()

    def import_yaml(self):
    
        with open(ARGS.config, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    
    def build_base_command(self):
    
        command = './pkb.py --machine_type='
    
    def run_benchmark_group(self, BENCHMARKGROUP):
    
        for benchmarkName, sub_tests in self.config[BENCHMARKGROUP].iteritems():
            if sub_tests:
               print(benchmarkName)
    
    def run_storage_benchmarks(self):
        
        self.run_benchmark_group('storage_benchmarks')
    
def main():

    perfkitRun = ukcloudPerfkit()
    perfkitRun.run_storage_benchmarks()


main()
