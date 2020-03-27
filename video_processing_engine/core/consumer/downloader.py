import json
import os

import pika

from video_processing_engine.utils.aws import access_file_update
from video_processing_engine.utils.downloads import (
    download_from_azure, download_from_google_drive, download_using_ftp)
from video_processing_engine.utils.logs import log
from video_processing_engine.utils.paths import downloads

log = log(__file__)


def pika_connect():
  credentials = pika.PlainCredentials('test', 'inpoint20200318')
  connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='159.89.52.183',
                              credentials=credentials,
                              virtual_host='testvm'))
  channel = connection.channel()
  channel.queue_declare(queue='file-transfer-Q')
  log.info('Pika connection established.')
  return channel


def compute(json_obj):
  json_data = json.loads(json_obj)
  if json_data.get('access_type', None) == 'GCP':
    log.info('Download file via Google Drive.')
    download_from_google_drive(json_data.get('g_url', None),
                                json_data.get('stored_filename', None))
  elif json_data.get('access_type', None) == 'Microsoft':
    log.info('Download file via Microsoft Azure.')
    download_from_azure(json_data.get('azure_account_name', None),
                        json_data.get('azure_account_key', None),
                        json_data.get('azure_container_name', None),
                        json_data.get('azure_blob_name', None),
                        json_data.get('stored_filename', None))
  elif json_data.get('access_type', None) == 'FTP':
    log.info('Transfer file via FTP.')
    download_using_ftp(json_data.get('remote_username', None),
                        json_data.get('remote_password', None),
                        json_data.get('remote_public_address', None),
                        json_data.get('remote_file', None),
                        json_data.get('stored_filename', None))
  elif json_data.get('access_type', None) == 'S3':
    log.info('Download file via Amazon S3 storage.')
    access_file_update(json_data.get('s3_access_key', None),
                        json_data.get('s3_secret_key', None),
                        json_data.get('s3_url', None),
                        json_data.get('stored_filename', None),
                        json_data.get('s3_bucket_name', None))
  elif json_data.get('access_type', None) == 'FTP TOOL':
    log.info('Transfer file via TeamViewer (FTP Tool).')
    os.path.join(downloads, json_data.get('stored_filename', None))


def callback(channel, method, properties, body):
  log.info(f'Received: {body}')
  compute(body)


channel = pika_connect()
channel.basic_consume(queue='file-transfer-Q',
                      on_message_callback=callback,
                      auto_ack=True)


def consume():
  global channel
  try:
    channel.start_consuming()
  except Exception:
    log.warning('Downloader consumer stopped after downloading huge file.')
    channel = pika_connect()
    log.info('Downloader consumer restarted.')
    consume()


while True:
  consume()
