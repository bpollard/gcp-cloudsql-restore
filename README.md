# Run MySQL Backup

## Requirments
If python 3 is not installed, follow the link below to install.

### software
python3 <https://www.python.org/>

gcloud  <https://cloud.google.com/sdk/install>

### infrastructure
CloudSQL instances are running

## How to Use
The default is to run this in staging DR

`make all`

To run in production DR

`DEPLOY_ENV=production make all`

## Notes
The production_env.sh and staging_env.sh will need to be updated if a CloudSQL instance name has changed. The project IDs are also defined here.
