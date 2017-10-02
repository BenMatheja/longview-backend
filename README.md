longview-backend
================
A Flask Restful Service to obtain performance metrics from the Longview Agent.
Metrics are written to a file, each line similar to this one

```json
{
   "Disk./dev/sda1.read_bytes":5450752,
   "Memory.swap.free":1048448,
   "Disk./dev/dm-0.writes":13298,
   "Memory.real.cache":472920,
   "Disk./dev/dm-0.fs.ifree":2481272,
   "Disk./dev/dm-1.writes":31,
   "@timestamp":"2017-10-02T10:35:04",
   "Disk./dev/dm-1.read_bytes":3371008,
   "Disk./dev/dm-0.fs.itotal":2526384,
   "Disk./dev/sda1.fs.free":434518016,
   "Disk./dev/dm-0.reads":9527,
   "CPU.cpu0.user":21387,
   "Network.Interface.enp0s8.rx_bytes":1286,
   "Memory.real.free":402700,
   "Network.Interface.enp0s8.tx_bytes":2234,
   "Disk./dev/dm-0.read_bytes":366235648,
   "Disk./dev/sda1.reads":243,
   "Disk./dev/dm-1.write_bytes":126976,
   "Memory.swap.used":124,
   "Memory.real.used":613392,
   "Disk./dev/sda1.fs.total":494512128,
   "Disk./dev/dm-1.reads":144,
   "Network.Interface.enp0s3.rx_bytes":14582007,
   "CPU.cpu0.system":3932,
   "Disk./dev/dm-0.fs.free":39205806080,
   "Network.Interface.lo.tx_bytes":5488108,
   "Disk./dev/sda1.write_bytes":6144,
   "CPU.cpu0.wait":292,
   "Disk./dev/dm-0.write_bytes":450363392,
   "host":"vagrant",
   "Memory.real.buffers":24688,
   "Network.Interface.lo.rx_bytes":5488108,
   "Load":0,
   "Network.Interface.enp0s3.tx_bytes":2160387,
   "Disk./dev/sda1.fs.itotal":124928,
   "Disk./dev/sda1.fs.ifree":124625,
   "Disk./dev/sda1.writes":6,
   "Disk./dev/dm-0.fs.total":40576331776
}
```

Previously started as PHP backend for a custom Linode Longview implementation.
Used to obtain performance metrics, attach them via filebeat to a central ELK instance.

## Installation

```bash
export LC_ALL=C
apt-get install virtualenv python-pip
mkdir /opt/longview-backend
cd /opt/
git clone git@github.com:BenMatheja/longview-backend.git
virtualenv longview-backend-env
pip install -e .
# Configure Settings
cp settings_sample.py settings.py
vi settings.py
# Add systemd configuration
useradd -s /bin/false -r longview
cp longview-backend.service /etc/systemd/system/                                        
vi /etc/systemd/system/longview-backend.service
cd ..
chown -R longview:longview longview-backend/
#Activate & Launch
systemctl daemon-reload
systemctl enable longview-backend
systemctl start longview-backend
systemctl status longview-backend
 ```

## Misc
You may use the nginx_proxy_configuration example to put the backend behind a reverse proxy
 