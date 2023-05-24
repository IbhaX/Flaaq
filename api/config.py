

# /src/config.py

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Development(object):
    """
    Development environment configuration
    """
    aws_access_key_id = "AKIA3XV24F6SPZAKNCWZ"
    aws_secret_access_key = "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"
    region_name = "ap-south-1"

    channel_name = "test1"
    latency_mode = "NORMAL"

class Production(object):
    """
    Production environment configurations
    """
    aws_access_key_id = "AKIA3XV24F6SPZAKNCWZ"
    aws_secret_access_key = "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"
    region_name = "ap-south-1"

    channel_name = "test1"
    latency_mode = "NORMAL"

class Testing(object):
    """
    Development environment configuration
    """
    aws_access_key_id = "AKIA3XV24F6SPZAKNCWZ"
    aws_secret_access_key = "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"
    region_name = "ap-south-1"

    channel_name = "test1"
    latency_mode = "NORMAL"




config = Development