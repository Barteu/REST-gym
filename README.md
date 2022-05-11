# REST-gym project


python3 -m virtualenv venv
source venv/bin/activate


curl http://localhost:5000/gyms -v
curl 'http://localhost:5000/gyms?limit=5&offset=0' -v   
curl http://localhost:5000/gyms -X POST -v  





curl http://localhost:5000/gyms/1 -v

curl http://localhost:5000/gyms/1 -H 'Content-Type: application/json' -H 'If-None-Match: "5811c82822a08ae75a4083f8aec3fc6e"' -d '{"name":"gymex","location":"Kornicka 100, Poznan"}' -X PUT -v   

curl http://localhost:5000/gyms/2 -H 'Content-Type: application/json' -H 'If-None-Match: "e6a9459bc0ba30924b3b649f4905a29c"' -d '{"location":"Osiedlowa 99, Poznan"}' -X PATCH -v   

curl http://localhost:5000/gyms/1 -X DELETE -v




curl http://localhost:5000/gyms/1/cleanups -X POST -v




curl http://localhost:5000/users -v
curl http://localhost:5000/users -X POST -v  

curl http://localhost:5000/users/3 -H 'Content-Type: application/json' -H 'If-None-Match: "cbcad765b9ee6db9551d74a7bc1d936a"' -d '{"first_name":"Jacek","last_name":"Kowalski","birth_year":1990}' -X PUT -v   

curl http://localhost:5000/users/3 -H 'Content-Type: application/json' -H 'If-None-Match: "ad104657fe767051fe3bdb5bca640531"' -d '{"last_name":"Duda"}' -X PATCH -v   

curl http://localhost:5000/users/3 -X DELETE -v






curl http://localhost:5000/gym-memberships -v

curl http://localhost:5000/gym-memberships -H 'Content-Type: application/json' -d '{"user_id":1,"gym_id":1,"entries":12}' -X POST -v




curl http://localhost:5000/gym-memberships/2 -v

curl http://localhost:5000/gym-memberships/2 -H 'Content-Type: application/json' -H 'If-None-Match: "41f4770b7edc7166388fa2da44cb87fb"' -d '{"entries":10}' -X PATCH -v




curl 'http://localhost:5000/equipments?limit=5&offset=10' -v

curl http://localhost:5000/equipments  -X POST -v


curl http://localhost:5000/equipments/12 -v

curl http://localhost:5000/equipments/23 -H 'Content-Type: application/json' -H 'If-None-Match: "97788b6a7ddb6b8f58ae941330e064c1"' -d '{"name":"bench"}' -X PUT -v   

curl http://localhost:5000/equipments/23 -H 'Content-Type: application/json' -H 'If-None-Match: "497781c84faf634cbd4ee74e083757e2"' -d '{"is_clean":false}' -X PATCH -v   

curl http://localhost:5000/equipments/23 -X DELETE -v



curl 'http://localhost:5000/equipment-affiliations?limit=3&offset=6' -v

curl http://localhost:5000/equipment-affiliations -X POST -v

curl http://localhost:5000/equipment-affiliations/23 -H 'Content-Type: application/json' -H 'If-None-Match: "a9067d29b8380e5542d024107ee3fb64"' -d '{"gym_id":2,"equipment_id":4}' -X PUT -v   

curl http://localhost:5000/equipment-affiliations/23 -X DELETE -v




curl http://localhost:5000/equipment-transfers -H 'Content-Type: application/json' -d '{"transfers":[{"equipment_id":1,"new_gym_id":2},{"equipment_id":2,"new_gym_id":1}]}' -X POST -v
  

  






https://flask-restful.readthedocs.io/en/latest/reqparse.html

