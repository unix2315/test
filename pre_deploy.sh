#!/bin/sh

redis-cli config get dir
redis-cli config get stop-writes-on-bgsave-error