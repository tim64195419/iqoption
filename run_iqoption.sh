echo "welcome to iqoption world!"

python3 check_open_market_iqoption.py

COUNT=$(wc -l open_market_check.txt | awk '{print $1}' | xargs echo)
for i in $(seq 1 $COUNT)
do
    python3 iqoption.py &
done

