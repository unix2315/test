#!/bin/sh

redis-cli shutdown
redis-server --daemonize yes