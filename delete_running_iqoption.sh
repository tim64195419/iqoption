IQORDER=$(ps aux | grep iqoption.py | awk '{print $2}' | xargs echo)

ps aux | grep iqoption.py | awk '{print $2}' | xargs echo
for i in $IQORDER;do kill -9 $i;done
rm ./current_running_market.txt
touch current_running_market.txt
