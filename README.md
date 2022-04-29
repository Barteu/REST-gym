# REST-gym project


python3 -m virtualenv venv
source venv/bin/activate



curl http://localhost:5000/todos -H 'Content-Type: application/json' -d '{"task":"something"}' -X POST -v   
