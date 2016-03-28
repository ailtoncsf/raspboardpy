rm -rf env
virtualenv --system-site-packages --python=python2.7 env
source env/bin/activate
pip install rpi.gpio flask pyserial
cd PIGPIO/
python setup.py install
cd ../libsensorPy
python setup.py install
cd ..
pip install eventlet
pip install flask-socketio
