#!/usr/bin/env python3

import argparse
import yaml

from pprint import pprint

from pipeline import Pipeline

class Main:
    def __init__(self, args):
        self.args = args
        self.config_path = "./.idrc"
        self.config = {}

    def load_config(self, config):
        if config:
            self.config_path = config
        print(f"using config at {self.config_path}")
        with open(self.config_path, 'rb') as cf:
            self.config = yaml.safe_load(cf)
        print(f"config: {self.config}")

    def run(self):
        print(args)
        pipeline_names = self.config.keys()
        print(f"Found pipelines: {pipeline_names}")
        pipelines = []
        for pipeline_name in pipeline_names:
            pipelines.append(Pipeline(pipeline_name, self.config[pipeline_name]))

        # todo: multiprocessing here to run faster
        results = []
        for pipeline in pipelines:
            results.append(pipeline.run())

        pprint([it['abstracts'] for it in results])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Id",
        description="A tool for connecting your layers of understanding",
        epilog="Specify a verb, type of data, and target to start exploring"
    )

    # Options
    options = parser.add_argument_group('options')
    options.add_argument("-c", "--config", default=False, help="specify a config file to use")
    options.add_argument("-v", "--verbose", action="store_true", default=False, help="enable verbose output")

    args = parser.parse_args()
    main = Main(args)
    print(args)
    main.load_config(args.config)
    main.run()