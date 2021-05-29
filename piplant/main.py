import argparse
import json
import os

import uvicorn

from dotmap import DotMap

from piplant.settings import settings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IOT server to monitor plants')
    parser.add_argument('--config', help='Path to configuration file', type=str)

    arguments = parser.parse_args()
    implicit_conf_path = os.path.join(os.getcwd(), 'piplant.conf.json')
    conf_path = None

    if arguments.config is not None:
        conf_path = arguments.config
    elif os.path.exists(implicit_conf_path):
        conf_path = implicit_conf_path

    if conf_path is not None:
        with open(conf_path, 'r') as config_file:
            settings.load(config_file)

    uvicorn.run('server:app', host=settings.interface, port=settings.port)
