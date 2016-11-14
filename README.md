
# Misc scripts by SubSite

A small collection of some of the scripts I use frequently, kept here for easier distribution among the servers we work with. I usually clone this repo somewhere in home and then symlink the scripts I need to `/usr/local/sbin`. 

###andsearch 

Search files in current folder including ALL given words.

USAGE: `andsearch "MATCH" [word1] [word2] ... `
EXAMPLE: `andsearch "*.txt" foo bar`

Source: [andsearch](https://github.com/subsite/misc-scripts/blob/master/andsearch)

###blacklist_hosts

Append external blacklist to /etc/hosts. Run as root using cron. 
Default blacklist from https://github.com/StevenBlack/hosts

Source: [blacklist_hosts](https://github.com/subsite/misc-scripts/blob/master/blacklist_hosts)

###check_railo

Requests a testpage using a timeout, and restarts Railo (or Adobe ColdFusion server, or something else) if the page doesn't respond. Also logs http status code if not "200 OK".

USAGE: `check_railo [testpage url]`

Run as root, special dependencies: curl

Cron example (every three minutes during working hours):   
`*/3 7-18 * * * root  /usr/local/sbin/check_webserver http://localhost/testpage.cfm`

Source: [check_railo](https://github.com/subsite/misc-scripts/blob/master/check_railo)

###db_backup

Dump script for PostgreSQL databases, Fredrik Welander 2013

Run as postgres

USAGE: `db_backup [database] [user] [dest path/filename]`  
CRON EXAMPLE:  
`00 01 * * * postgres      /usr/local/sbin/db_backup mydb myuser /var/db_backup/mydb_daily.pgdump`

Source: [db_backup](https://github.com/subsite/misc-scripts/blob/master/db_backup)

###diskspace

Sends and alert email if the available space on a partition is less than treshold.   
USAGE: `diskspace [partition] [treshold]`  

Crontab example (sends alert if /dev/sda1 has less than 50GB free):  
`0 0 * * * root /usr/local/sbin/diskspace /dev/sda1 50`

Source: [diskspace](https://github.com/subsite/misc-scripts/blob/master/diskspace)

###pushpull

A Git script for doing a quick push-pull operation from a devel repository to a 
production repoistory. Both repositories must be in the same rootpath on the same webserver.
Saves you the trouble of doing 'git push [wait], cd ../website, git pull [wait], cd ../website_devel. 
Includes basic checking for correct path and branch, dirty-state and unpushed commits. 

Source: [pushpull](https://github.com/subsite/misc-scripts/blob/master/pushpull)

###sftp_put

A cron-schedulable script for uploading files using sftp. This script is only relevant if you don't
have ssh shell access (server goes "This service allows sftp connections only"),
otherwise, forget this convoluted hack and use scp or rsync instead.

Usage: 
- A single file: sftp_put /payload/dir/file.txt user@sftp.server.com remote_directory
- Multiple files using an extension wildcard: sftp_put "/payload/dir/*.txt" user@sftp.server.com remote_directory

Note:
- Wildcard paths must be quoted
- Only \*.[extension] wildcards are supported (`*`, `*.*` or `file*` won't work)

Credits:
Thanks for the idea, Eric_G!
(http://www.unix.com/unix-for-dummies-questions-and-answers/24994-sftp-batch-script.html)

Source: [sftp_put](https://github.com/subsite/misc-scripts/blob/master/sftp_put)

###snapshotbackup

A pretty complete solution for time freezed incremental backups. This one has earned its own repo: 

Source: https://github.com/subsite/snapshotbackup

###split_pgdump.php

A php script that splits a PostgreSQL schema only dump into separate database object files. Useful for getting your database under version control.

Use with cron or as a pre-commit hook as described here: https://github.com/subsite/git-cheatsheet/blob/master/README.md#database-schema-hook

Usage: `split_pgdump.php SCHEMA_FILE OUTPUT_DIR`

Source: [split_pgdump.php](https://github.com/subsite/misc-scripts/blob/master/split_pgdump.php)

###telegrambot.py

Sends message as a Telegram Bot. See https://core.telegram.org/bots
Good for automated notifications from your servers.

Usage `telegrambot.py "Hello Telegram"`
