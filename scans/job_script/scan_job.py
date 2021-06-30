#!/usr/bin/env python

import sys
import argparse
import model_scan as ms


def main(args):

    model_scan_job = ms.scan_job(args.job_config_path)
    processed_param_pts = model_scan_job.process_param_pts()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='model scan job')

    parser.add_argument("job_config_path",  help="model scan job configuration path")
    args = parser.parse_args()

    print(args)

    main(args)

