longview-backend
================
A Flask Restful Service to obtain performance metrics from the longview agent

Previously started as PHP backend for custom Linode Longview implementation.
Used to obtain performance metrics, attach them via filebeat to the central ELK instance.

```

useradd -s /bin/false -r <username>

cp todoist-flask.service /etc/systemd/system/                                              │849-4af9-98f2-60a218c234f9
 1575  vi /etc/systemd/system/todoist-flask.service
 
 systemctl daemon-reload
 systemctl enable longview-backend
 