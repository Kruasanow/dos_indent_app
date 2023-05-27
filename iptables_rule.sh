#!/bin/bash
iptables -A $1 -p $2 -j DROP