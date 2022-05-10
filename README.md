# REST-gym project


python3 -m virtualenv venv
source venv/bin/activate


curl http://localhost:5000/gyms -v

curl 'http://localhost:5000/gyms?limit=5&offset=0' -v   

curl http://localhost:5000/gyms/1 -v

curl http://localhost:5000/gyms -X POST -v   

curl http://localhost:5000/gyms/1 -H 'Content-Type: application/json' -d '{"name":"gymex01"}' -X PUT -v   

curl http://localhost:5000/gyms/1 -H 'Content-Type: application/json' -H 'If-None-Match: "ca6028065ab6f3746ec3cd1fb83bb747"' -d '{"name":"gymex01","location":"poznan 12"}' -X PUT -v   

curl http://localhost:5000/gyms/2 -H 'Content-Type: application/json' -H 'If-None-Match: "2f6819092fb77edab93d8f1f226d3feb"' -d '{"name":"gymex01"}' -X PATCH -v   


curl 'http://localhost:5000/equipments?limit=5&offset=0' -v    


https://flask-restful.readthedocs.io/en/latest/reqparse.html


