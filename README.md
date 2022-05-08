# REST-gym project


python3 -m virtualenv venv
source venv/bin/activate


curl http://localhost:5000/gyms -v
curl http://localhost:5000/gyms/1 -v
curl http://localhost:5000/gyms -H 'Content-Type: application/json' -d '{"name":"gymex1"}' -X POST -v   
curl http://localhost:5000/gyms/1 -H 'Content-Type: application/json' -d '{"name":"gymex01"}' -X PUT -v   
curl http://localhost:5000/gyms/1 -H 'Content-Type: application/json' -H 'If-None-Match: "8373f4dbd14b345b4b464b6442cbaabe"' -d '{"name":"gymex01"}' -X PUT -v   




https://flask-restful.readthedocs.io/en/latest/reqparse.html


