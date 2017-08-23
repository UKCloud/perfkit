#!/usr/bin/env python

import yaml
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--cloud_provider", help="Service provider to benchmark \
                    [UKCloud-OpenStack | UKCloud-vCloud | AWS-UK | AWS-US | Azure | Google]", required=True)
parser.add_argument("--config", help='Path to perfkit yaml config', required=True)
ARGS = parser.parse_args()

class ukcloudPerfkit():

    def __init__(self):
        self.config = self.import_yaml()
        self.core_config = self.config['core_config']
        self.common_config = self.config['common_config']
        self.cloud_config = self.config['cloud_config'][ARGS.cloud_provider]
        self.benchmarks = self.config['benchmarks']

    def import_yaml(self):
    
        with open(ARGS.config, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_date(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%M-%d-%H-%m")

    def format_results_log(self, benchmark, mode, workload):

        logPath = '--json_path=' \
                  + self.core_config['json_path'] \
                  + self.cloud_config['options']['cloud_provider'] \
                  + '.' + self.cloud_config['flavor_name'] \
                  + '.' + benchmark + '.'
        if workload:
            logPath = logPath + workload \
                    + '.' + self.get_date() + '.'
        logPath = logPath + 'results.json'
        return logPath
    
    def build_base_command(self, benchmark, mode=None, workload=None, storage_type=None, storage_tier=None):
    
        command = './pkb.py ' \
                  + 'benchmark=' + benchmark \
                  + self.format_results_log(benchmark, mode, workload)
        if mode:
            command = command + ' --' + mode + '=' + workload 
        for option, value in self.common_config.iteritems():
            command = command + (' --' + str(option) + '=' + str(value))
        for option, value in self.cloud_config['options'].iteritems():
            command = command + (' --' + str(option) + '=' + str(value))
        return command
    
    def run_benchmark_group(self, BENCHMARKGROUP):
    
        if self.cloud_config['storage_tiers']:
          print('y')
        for benchmarkName, sub_tests in self.benchmarks[BENCHMARKGROUP].iteritems():
            if sub_tests:
                for mode in sub_tests:
                    for test in self.benchmarks[BENCHMARKGROUP][benchmarkName][mode]:
                        print(self.build_base_command(benchmarkName, mode, test))
            else:
                print(self.build_base_command(benchmarkName))
    
    def run_storage_benchmarks(self):
        
        self.run_benchmark_group('storage_benchmarks')
    
def main():

    perfkitRun = ukcloudPerfkit()
    perfkitRun.run_storage_benchmarks()


main()
