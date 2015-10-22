#!/bin/sh
# insurance_harvest.sh
# insurance data collection program
# Oct. 22, 2015
# Harvard Kennedy School
# Bo Zhao
# bo_zhao@hks.harvard.edu
# sudo python /home/bo/Workspace/wbcrawler/insurance_crawler.py
PATH=/home/bo/Workspace/wbscrawler
export Path

sudo pkill firefox
sudo free -m
python insurance_crawler.py
python insurance_crawler_parallel.py