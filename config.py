#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun

# 全局日志配置
import logging
import os

# logging
logging.basicConfig(level=logging.DEBUG,
                    datefmt="%Y/%m/%d %H:%M:%S",
                    format="%(asctime)s %(levelname)8s %(process)05d L%(lineno)03d %(funcName)s %(message)s")

# mongo
MONGO_HOST = os.getenv("MONGO_HOST", "mongo.zlikun.com")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
