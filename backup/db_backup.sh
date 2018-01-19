docker exec -it oj-postgres pg_dumpall -c -U onlinejudge > db_backup_`date +%Y_%m_%d"_"%H_%M_%S`.sql
