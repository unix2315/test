#!/bin/sh

redis-cli config get stop-writes-on-bgsave-error
redis-cli config get save
redis-cli BGSAVE
redis-cli config get logfile
redis-cli set logfile logl.log
ls -l
cat logl.log