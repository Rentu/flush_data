#/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import redis
import memcache as mem
import os
import time

flush_redis_flg = False
flush_mem_flg = False
restart_fpm = True

db_host = ""
db_user = ""
db_pwd = ""

redis_host = ""
redis_port = ""

db_list = ["", "", "", ""]
db_list_new = []

# 清空user库
def truncate(dbName):
    db = mdb.connect(db_host, db_user, db_pwd, dbName)
    c = db.cursor()
    c.execute("show tables")
    tables = c.fetchall()
    for table in tables:
        truncate_sql = "truncate table {table_name}".format(table_name=table[0])
        c.execute(truncate_sql)
        print truncate_sql
    db.close()

    
# mysql
try:
    if db_list_new:
        for dbName in db_list_new:
            if dbName == "":
                for i in range(0, 100):
                    newDbName = dbName+str(i)
                    print "当前数据库:"+newDbName
                    truncate(newDbName)
            truncate(dbName)
except Exception, e:
    print e.message

# redis
if flush_redis_flg:
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    r.flushall()
    print "redis已经清空"

# memcached
if flush_mem_flg:
    mc = mem.Client(["127.0.0.1:11211"])
    mc.flush_all()
    print "memcache已经清空"
# php

def get_fpm_pid():
    fpm_pid_path = ""
    f = open(fpm_pid_path)
    line = f.readline()
    return line

if restart_fpm:
    line = get_fpm_pid()
    os.system("sudo kill -USR2 "+line)
    print "已重启fpm进程"+line
    time.sleep(1)
    print "当前进程"+get_fpm_pid()