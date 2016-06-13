
# Misc scripts by SubSite

A small collection of some of the scripts I use frequently, kept here for easier distribution among the servers we work with. I usually clone this repo somewhere in home and then symlink the scripts I need to `/usr/local/sbin`. 

###check_railo

Requests a testpage using a timeout, and restarts Railo (or Adobe ColdFusion server, or something else) if the page doesn't respond. Also logs http status code if not "200 OK".

USAGE: `check_railo [testpage url]`

Run as root, special dependencies: curl

Cron example (every three minutes during working hours):   
`*/3 7-18 * * * root  /usr/local/sbin/check_webserver http://localhost/testpage.cfm`


###db_backup

Dump script for PostgreSQL databases, Fredrik Welander 2013

Run as postgres

USAGE: `db_backup [database] [user] [dest path/filename]`  
CRON EXAMPLE:  
`00 01 * * * postgres      /usr/local/sbin/db_backup mydb myuser /var/db_backup/mydb_daily.pgdump`

###diskspace

Sends and alert email if the available space on a partition is less than treshold.   
USAGE: `diskspace [partition] [treshold]`  

Crontab example (sends alert if /dev/sda1 has less than 50GB free):  
`0 0 * * * root /usr/local/sbin/diskspace /dev/sda1 5`

###pushpull

A Git script for doing a quick push-pull operation from a devel repository to a 
production repoistory. Both repositories must be in the same rootpath on the same webserver.
Saves you the trouble of doing 'git push [wait], cd ../website, git pull [wait], cd ../website_devel. 
Includes basic checking for correct path and branch, dirty-state and unpushed commits. 

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

###snapshotbackup

A pretty complete solution for time freezed incremental backups. This one has earned its own repo: https://github.com/subsite/snapshotbackup
