#!/bin/bash
sudo apt -y update
sudo apt -y erlang
sudo apt -y install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmqctl status
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmq-plugins enable rabbitmq_auth_backend_jwt
sudo cat <<EOF >> /etc/rabbitmq/rabbitmq-env.conf
# Use JWT for authentication
auth_backends.1 = jwt

# Set up JWT secret or public key for verification
# For HMAC signing (e.g., HS256):
auth_jwt.secret_key = "your_jwt_secret_key_here"

# OR, for RSA or ECDSA signing (e.g., RS256):
# auth_jwt.public_key = "/path/to/public_key.pem"

# Define additional JWT configuration options
auth_jwt.default_user_claim = "sub"  # The claim that stores the username
auth_jwt.key_refresh_interval = 3600  # Time (in seconds) to refresh the key
EOF
sudo systemctl restart rabbitmq-server
