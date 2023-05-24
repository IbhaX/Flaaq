import boto3
from api.config import config


ivs_client = boto3.client('ivs',
        aws_access_key_id= config.aws_access_key_id,
        aws_secret_access_key= config.aws_secret_access_key,
        region_name=config.region_name
    )

def create_ivs_channel():

    response = ivs_client.create_channel(
        name=config.channel_name,
        latencyMode=config.latency_mode
    )

    channel_arn = response['channel']['arn']
    stream_key_arn = response['streamKey']['arn']
    return channel_arn, stream_key_arn

def get_ivs_channel_info(channel_arn):

    response = ivs_client.get_channel(arn=channel_arn)

    playback_url = response['channel']['playbackUrl']
    rtmps_server = response['channel']['ingestEndpoint']


    return playback_url, rtmps_server

def get_stream_key(channel_arn):

    response = ivs_client.get_stream_key(
        arn=channel_arn
    )
    streaming_key = response['streamKey']['value']
    return streaming_key

def get_ivs_streaming_info():
    channel_arn, stream_key_arn = create_ivs_channel()
    playback_url, rtmps_server = get_ivs_channel_info(channel_arn)
    streaming_key = get_stream_key(stream_key_arn)

    return playback_url, rtmps_server, streaming_key

playback_url, rtmps_server, streaming_key = get_ivs_streaming_info()


ivs_channel_data = {
    "playback_url": playback_url,
    "rtmps_server": rtmps_server,
    "streaming_key": streaming_key
}

