#!/bin/bash
 
MONGO_DATABASE="annotation"
MONGO_HOST="10.0.5.40"
MONGO_PORT="27017"
TIMESTAMP=`date +%Y-%m-%d-%H-%M-%S`
MONGODUMP_PATH=/usr/bin/mongodump
BACKUPS_DIR=~/sjyan/data/mongodb-backup/
BACKUP_NAME=$TIMESTAMP
SCRIPT_DIR=~/sjyan/scripts/

cd

$MONGODUMP_PATH -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE

mkdir -p $BACKUPS_DIR
mv dump $BACKUP_NAME
mv $BACKUP_NAME $BACKUPS_DIR

# delete backups which are older than 1 month
find $BACKUPS_DIR -ctime +30 -type d -exec rm -rf {} +

