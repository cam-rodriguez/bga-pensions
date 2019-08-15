#!/bin/bash
set -euo pipefail

# Make sure the deployment group specific variables are available to this
# script.
source /home/datamade/bga-pensions/configs/$DEPLOYMENT_GROUP_NAME-config.conf

# Set some useful variables
DEPLOYMENT_NAME="$APP_NAME-$DEPLOYMENT_ID"
PROJECT_DIR="/home/datamade/$DEPLOYMENT_NAME"
VENV_DIR="/home/datamade/.virtualenvs/$DEPLOYMENT_NAME"

# Move the contents of the folder that CodeDeploy used to "Install" the app to
# the deployment specific folder
mv /home/datamade/bga-pensions $PROJECT_DIR

# Create a deployment specific virtual environment
python3 -m venv $VENV_DIR

# Set the ownership of the project files and the virtual environment
chown -R datamade.www-data $PROJECT_DIR
chown -R datamade.www-data $VENV_DIR

# Upgrade pip and setuptools. This is needed because sometimes python packages
# that we rely upon will use more recent packaging methods than the ones
# understood by the versions of pip and setuptools that ship with the operating
# system packages.
sudo -H -u datamade $VENV_DIR/bin/pip install --upgrade pip
sudo -H -u datamade $VENV_DIR/bin/pip install --upgrade setuptools

# Install the project requirements into the deployment specific virtual
# environment.
sudo -H -u datamade $VENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt --upgrade

# Move project configuration files into the appropriate locations within the project.
mv $PROJECT_DIR/configs/local_settings.$DEPLOYMENT_GROUP_NAME.py $PROJECT_DIR/bga_database/local_settings.py

# OPTIONAL If you're using PostgreSQL, check to see if the database that you
# need is present and, if not, create it setting the datamade user as it's
# owner.
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'bga_pensions'" | grep -q 1 || createdb -U postgres -O datamade bga_pensions

# OPTIONAL Run migrations and other management commands that should be run with
# every deployment
$VENV_DIR/bin/python $PROJECT_DIR/manage.py migrate
$VENV_DIR/bin/python $PROJECT_DIR/manage.py createcachetable
$VENV_DIR/bin/python $PROJECT_DIR/manage.py collectstatic --no-input

# Create the directory for compressed files and give the datamade user the
# appropriate permissions to write to and read from it
COMPRESSOR_DIR="$PROJECT_DIR/static/compressor"
mkdir $COMPRESSOR_DIR && chown -R datamade.datamade $COMPRESSOR_DIR && chmod -R g+r $COMPRESSOR_DIR

# Echo a simple nginx configuration into the correct place, and tell
# certbot to request a cert if one does not already exist.
# Wondering about the DOMAIN variable? It becomes available by source-ing
# the config file (see above).
if [ ! -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ]; then
    echo "server {
        listen 80;
        server_name $DOMAIN;

        location ~ .well-known/acme-challenge {
            root /usr/share/nginx/html;
            default_type text/plain;
        }

    }" > /etc/nginx/conf.d/$APP_NAME.conf
    service nginx reload
    certbot -n --nginx -d $DOMAIN -m devops@datamade.us --agree-tos
fi

# Install Jinja into the virtual environment and run the render_configs.py
# script.
$VENV_DIR/bin/pip install Jinja2==2.10
$VENV_DIR/bin/python $PROJECT_DIR/scripts/render_configs.py $DEPLOYMENT_ID $DEPLOYMENT_GROUP_NAME $DOMAIN $APP_NAME

# Write out the deployment ID to a Python module that can get imported by the
# app and returned by the /pong/ route (see above).
echo "DEPLOYMENT_ID='$DEPLOYMENT_ID'" > $PROJECT_DIR/bga_database/deployment.py

# Install npm
which node || (
    apt-get update
    apt-get install -y nodejs npm
    ln -s /usr/bin/nodejs /usr/bin/node 2&>1 || echo '/usr/bin/node already exists'
)

# Install npm requirements.
cd $PROJECT_DIR && npm install

# Password-protect the application.
echo $DOMAIN_USERNAME:$(openssl passwd -crypt "$DOMAIN_PASSWORD") > /etc/nginx/conf.d/bga-pensions-htpasswd
