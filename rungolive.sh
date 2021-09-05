set -a # automatically export all variables
source .env
set +a

python server.py