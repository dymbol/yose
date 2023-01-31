pip3 install -r ../src/requierments.txt --user
mkdir -p /tmp/yose_output
cp ../src/settings.py_EXAMPLE ../src/settings.py
python3 ../src/harvest.py
python3 ../src/generate.py

