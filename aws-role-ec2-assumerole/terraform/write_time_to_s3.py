#!/usr/bin/env python3

import boto3
import datetime
import os


if __name__ == "__main__":
    """
    Write current time to file in S3 bucket defined in environment variable BUCKET_NAME
    """

    client = boto3.client('s3')

    if not os.environ.get('BUCKET_NAME'):
        print("ERROR: environment variable BUCKET_NAME not set! Exiting...")
        exit(1)

    bucket = os.environ.get('BUCKET_NAME')

    u = datetime.datetime.utcnow()

    thetime = f'{u.month:02}.{u.day:02}.{u.year}.{u.hour:02}.{u.minute:02}.{u.second:02}'

    filename = thetime + '.txt'
    content = "Current time is: " + f'{u.hour:02}:{u.minute:02}:{u.second:02}' + ' UTC'

    client.put_object(Body=content, Bucket=bucket , Key=filename)
