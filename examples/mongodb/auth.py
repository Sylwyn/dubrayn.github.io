#!/usr/bin/env python

import sys
import pymongo.errors
import pickle
from pymongo import MongoClient
import bson.binary
import urllib
import numpy as np

username = urllib.quote_plus('user0')
password = urllib.quote_plus('pwd0')
client = MongoClient('mongodb://%s:%s@127.0.0.1/test_db' % (username, password))
db = client.test_db
results = db.test_results

print("### Insert data ###")
try:
  for i in range(3):
    data = { "run": "0000", "time": 0.01 * i, "norm": 1.0}
    data_id = results.insert_one(data).inserted_id
    print("id: %s" % (str(data_id)))
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Count data ###")
try:
  c = results.count()
  print("%d data" % (c))
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Find data ###")
try:
  for d in results.find():
    print("%s" % (str(d)))
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Delete data ###")
try:
  for d in results.find():
    dataId = d['_id']
    results.delete_one({"_id": dataId})
    print("deleted data with id: %s" % (dataId))
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Count data ###")
try:
  c = results.count()
  print("%d data" % (c))
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Insert numpy data ###")
try:
  for i in range(3):
    mat = np.eye(3) * i
    bindat = bson.binary.Binary(pickle.dumps(mat, protocol = 2))
    data = { "run": "0000", "mat": bindat}
    data_id = results.insert_one(data).inserted_id
    print("id: %s" % (str(data_id)))
    print(mat)
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Get numpy data ###")
try:
  for data in results.find():
    bindat = data["mat"]
    data_id = data["_id"]
    mat = pickle.loads(bindat)
    print("id: %s v:" % (str(data_id)))
    print(mat)
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))

print("### Delete data ###")
try:
  for d in results.find():
    dataId = d['_id']
    results.delete_one({"_id": dataId})
    print("deleted data with id: %s" % (dataId))
except pymongo.errors.OperationFailure as e:
  print("ERROR: %s" % (e))



