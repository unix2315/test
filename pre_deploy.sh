#!/bin/sh

redis-cli config get stop-writes-on-bgsave-error
redis-cli config get save
redis-cli BGSAVE
redis-cli config get logfile
ls -l /var/log/redis/
sudo tail /var/log/redis/redis-server.log -n 100