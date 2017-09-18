longview-backend
================
A Flask Restful Service to obtain performance metrics from the longview agent

Previously started as PHP backend for custom Linode Longview implementation.
Used to obtain performance metrics, attach them via filebeat to a central ELK instance.

## Installation

```bash
mkdir /opt/longview-backend
cd /opt/longview-backend
git clone git@github.com:BenMatheja/longview-backend.git
virtualenv longview-backend-env
pip install -e .
# 
useradd -s /bin/false -r longview
cp longview-backend.service /etc/systemd/system/                                        
vi /etc/systemd/system/todoist-flask.service
 
systemctl daemon-reload
systemctl enable longview-backend
systemctl start longview-backend
systemctl status longview-backend
 ```
 
 