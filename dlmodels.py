#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is based on 
# https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/download_models.py

from __future__ import print_function
import hashlib
import sys
import tarfile
if sys.version_info[0] < 3:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen


class Model:
    MB = 1024*1024
    BUFSIZE = 10*MB

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.url = kwargs.pop('url', None)
        self.filename = kwargs.pop('filename')
        self.sha = kwargs.pop('sha', None)
        self.archive = kwargs.pop('archive', None)
        self.member = kwargs.pop('member', None)

    def __str__(self):
        return 'Model <{}>'.format(self.name)

    def printRequest(self, r):
        def getMB(r):
            d = dict(r.info())
            for c in ['content-length', 'Content-Length']:
                if c in d:
                    return int(d[c]) / self.MB
            return '<unknown>'
        print('  {} {} [{} Mb]'.format(r.getcode(), r.msg, getMB(r)))

    def verify(self):
        if not self.sha:
            return False
        print('  expect {}'.format(self.sha))
        sha = hashlib.sha1()
        try:
            with open(self.filename, 'rb') as f:
                while True:
                    buf = f.read(self.BUFSIZE)
                    if not buf:
                        break
                    sha.update(buf)
            print('  actual {}'.format(sha.hexdigest()))
            return self.sha == sha.hexdigest()
        except Exception as e:
            print('  catch {}'.format(e))

    def get(self):
        if self.verify():
            print('  hash match - skipping')
            return True

        if self.archive or self.member:
            assert(self.archive and self.member)
            print('  hash check failed - extracting')
            print('  get {}'.format(self.member))
            self.extract()
        else:
            assert(self.url)
            print('  hash check failed - downloading')
            print('  get {}'.format(self.url))
            self.download()

        print(' done')
        print(' file {}'.format(self.filename))
        return self.verify()

    def download(self):
        try:
            r = urlopen(self.url, timeout=60)
            self.printRequest(r)
            self.save(r)
        except Exception as e:
            print('  catch {}'.format(e))

    def extract(self):
        try:
            with tarfile.open(self.archive) as f:
                assert self.member in f.getnames()
                self.save(f.extractfile(self.member))
        except Exception as e:
            print('  catch {}'.format(e))

    def save(self, r):
        with open(self.filename, 'wb') as f:
            print('  progress ', end='')
            sys.stdout.flush()
            while True:
                buf = r.read(self.BUFSIZE)
                if not buf:
                    break
                f.write(buf)
                print('>', end='')
                sys.stdout.flush()

models = [
    Model(
        name='MobileNet-SSD v1 (TensorFlow)',
        url='http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2017_11_17.tar.gz',
        sha='6157ddb6da55db2da89dd561eceb7f944928e317',
        filename='ssd_mobilenet_v1_coco_2017_11_17.tar.gz'),
    Model(
        name='MobileNet-SSD v1 (TensorFlow)',
        archive='ssd_mobilenet_v1_coco_2017_11_17.tar.gz',
        member='ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb',
        sha='9e4bcdd98f4c6572747679e4ce570de4f03a70e2',
        filename='frozen_inference_graph.pb'),
    Model(
        name='MobileNet-SSD v1 (pbtxt)',
        url='https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v1_coco_2017_11_17.pbtxt',
        sha='c7cf985ce0a4a8953daaa4b8cacdd3c8e31437a6',
        filename='config.pbtxt'),
]

# カレントディレクトリに講座に使うモデルをダウンロードします
if __name__ == '__main__':
    failedModels = []
    for m in models:
        print(m)
        if not m.get():
            failedModels.append(m.filename)

    if failedModels:
        print("Following models have not been downloaded:")
        for f in failedModels:
            print("* {}".format(f))
        exit(15)
