#!/bin/sh
# free_mememory.sh
# insurance data collection program
# Oct. 22, 2015
# Harvard Kennedy School
# Bo Zhao
# bo_zhao@hks.harvard.edu
sudo rm /home/bo/wbcrawler/crawler.log
sudo rm /home/bo/wbcrawler/crawler-info.log
sudo rm /home/bo/wbcrawler/crawler-path.log
sudo rm /home/bo/wbcrawler/crawler-geo.log
echo "the daily log has been deleted"
cd /home/bo/wbcrawler
sudo git checkout --force
sudo git pull
echo "the program has updated to the latest version"
echo "the crawler has rebooted. "
sudo shutdown -r now