import argparse


def get_system_args():
    # Configure system arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True)
    parser.add_argument("--database_url", required=True)
    parser.add_argument("--log_group_name", required=True)
    args = parser.parse_args()
    return args
