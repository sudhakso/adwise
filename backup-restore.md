# Backup and Restore #

This document records the steps that are necessary to get backup the data and restore for Failure tolerance.

### How do I backup? ###

# Backing up Database #

mongodump -d my_database -o /tmp/_dbbackup/
Here, my_database is the name of the DB to backup.

# Backing up elasticsearch indexes #

STEP1: vi elasticsearch.yml, path.repo: ['/tmp/_esbackup'], restart ES

STEP2:
curl -XPUT 'localhost:9200/_snapshot/my_backup?pretty' -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/tmp/_esbackup/my_backup/"
  }
}
'
STEP3:
curl -XPUT 'localhost:9200/_snapshot/my_backup/snapshot_1?wait_for_completion=true&pretty'


### How do I restore? ###

# Restoring up Database #

mongorestore -d my_database /tmp/_db/my_database/
Here, my_database is the name of the DB to backup.

# Restoring elasticsearch indexes #

STEP1: vi elasticsearch.yml, path.repo: ['/tmp/_esbackup'], restart ES

STEP2:
curl -XPUT 'localhost:9200/_snapshot/my_backup?pretty' -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/tmp/_esbackup/my_backup/"
  }
}
'
STEP3:
curl -XPOST 'localhost:9200/*/_close?pretty'

STEP4:
curl -XPOST 'localhost:9200/_snapshot/my_backup/snapshot_1/_restore?pretty'

STEP5:
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/mediaaggregate/_open?pretty'
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/ad/_open?pretty'
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/oohmediasource/_open?pretty'
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/offer/_open?pretty'
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/campaign/_open?pretty'
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/offerextension/_open?pretty'
ubuntu@ip-172-31-19-119:~/adwise-userprofile-mgr$ curl -XPOST 'localhost:9200/mediauser/_open?pretty'

