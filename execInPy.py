#!/usr/bin/env python3

import boto3
import logging 
import os
from datetime import datetime
from botocore.exceptions import ClientError
import docker
client = docker.from_env()

# create backup from gitlab container
container = client.containers.get('22394c19337f')
container.exec_run('gitlab-backup create')
# end of backup


def upload():
    logging.basicConfig(level=logging.INFO)
    
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='endpoint',
            aws_access_key_id='',
            aws_secret_access_key=''
        )
    except Exception as exc:
        logging.error(exc)
    
    else:
        try:
            bucket = s3_resource.Bucket('atiyeh')
            file_path = 'gitlab_backup.tar.gz'
            object_name = f'gitlab_backup {datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}.tar.gz'
    
            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
        except ClientError as e:
            logging.error(e)

def gitlabgz():
    os.system(commad)
    commad= f"tar -pczvf gitlab_backup.tar.gz  /srv/gitlab/data/backups/"

def remove():
    commad= f"rm -rf /srv/gitlab/data/backups/*"
    os.system(commad)

def main():
    gitlabgz()
    upload()
    remove()


if __name__ == "__main__":

    main()
