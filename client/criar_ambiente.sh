rm -rf env
virtualenv --system-site-packages --python=python2.7 env
source /env/bin/activate
pip --version
pip install rpi.gpio flask pyserial
python PIGPIO/setup.py install
