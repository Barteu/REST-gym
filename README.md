# REST-gym project


python3 -m virtualenv venv
source venv/bin/activate


curl http://localhost:5000/gyms   
curl http://localhost:5000/gyms -H 'Content-Type: application/json' -d '{"name":"gymex1"}' -X POST -v   


curl http://localhost:5000/todos -H 'Content-Type: application/json' -d '{"task":"something"}' -X POST -v   
