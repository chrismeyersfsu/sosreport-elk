#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
import json
import requests
import pyzstd
from urllib.parse import urlparse

logging.basicConfig()
logger = logging.getLogger('tools.scripts.replay_log')
logger.setLevel(logging.DEBUG)

class OTLPCompressedFileProcessor:
    # TODO: Prefer the non compressed path. This code will probably bitwrot now
    # This code is NOT being called.
    def __init__(self, file):
        self.file = file
        self.byte_count = 0

    def __iter__(self):
        with open(self.file, 'rb') as f:
            while num_bytes := f.read(4):
                try:
                    num_bytes = int.from_bytes(num_bytes, "big", signed=False)
                    compressed = f.read(num_bytes)
                    self.byte_count += 4
                    if not compressed:
                        raise ValueError(f"Expected to read {self.byte_count} but only got {len(compressed)} bytes")
                    decompressed = pyzstd.decompress(compressed)

                    decoded = decompressed.decode('utf-8')

                    yield json.loads(decoded)
                    self.byte_count += num_bytes
                except pyzstd.ZstdError as e:
                    logger.debug("decompress() error {e}")
                    raise
                except ValueError:
                    raise


class OTLPFileProcessor:
    def __init__(self, file):
        self.file = file
        self.byte_count = 0

    def __iter__(self):
        with open(self.file, 'rb') as f:
            for line in f:
                yield json.loads(line.strip())


class OTELLogRecordReplayer:
    def __init__(self, file, url, verify=True):
        self._file = file
        self._headers = {
            'Content-Type': 'application/json',
        }
        self._verify = verify

        # Assume http otel exporter endpoint
        u = urlparse(url)
        u = u._replace(scheme='http') if not u.scheme else u
        u = u._replace(path='/v1/logs') if (not u.path or u.path == '/') else u

        # TODO: add support for span and metrics replay + endpoints

        self._url = u.geturl()

    def send_logrecord(self, record):
        payload = json.dumps(record).encode('utf-8')
        res = requests.post(self._url, data=payload, headers=self._headers, verify=self._verify)
        if res.status_code != 204:
            logger.warning(f"Failed to POST log to endpoint {res.status_code} - {self._url} {res.content}")

    def run(self):
        processor = OTLPFileProcessor(self._file)
        count = 0
        failed_count = 0
        try:
            for i, record in enumerate(processor):
                self.send_logrecord(record)
                count += 1
        except pyzstd.ZstdError as e:
            failed_count += 1

        return count, failed_count


class Command():
    help = 'Replay OpenTelemetry Collector file logs to a remote OTLP server (i.e. loki, tempo).'

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            '--url',
            dest='url',
            type=str,
            metavar='u',
            required=True,
            help='http(s)://otlp-host.com:4318 for example. Note that the appropriate endpoint will be appended (i.e. /v1/logs). If grpc then it will be discovered.',
        )
        self.parser.add_argument('--file', dest='file', type=str, metavar='f', required=True, help='zstd compressed OTEL collector filexporter log file.')
        self.parser.add_argument('--verify', dest='verify', type=bool, metavar='k', default=True, help='Skip verify url certs.')

    def handle(self):
        options = self.parser.parse_known_args()[0]

        url = options.url
        file = options.file
        verify = options.verify

        success, failed = OTELLogRecordReplayer(file, url, verify=verify).run()
        logger.info(f"Sent {success} records successfully. Failed to send {failed}", extra={'success': success, 'failed': failed, 'url': url, 'file': file, 'verify': verify})

if __name__ == "__main__":
    cmd = Command()
    cmd.handle()
