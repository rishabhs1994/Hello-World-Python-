**Rate Limiting**

Rate Limiting is the process by which an API rejects requests.By implementing rate limiting, the developer essentially 
installs a safety system which can be relaxed to allow for greater flow, or tightened to reduce the flow within the system.

The main reason to implement Rate Limiting is to ensure that no single user dominates, ensure quality service and to make more
profit.

We can set a time duration in which a user can visit a url a certain number of times only. If he exceeds that count, he gets rate limited and is unable to view the content of url. After the time duration is complete, the rate limit gets lifted and he can again access the url.

I have used Redis which is in memory database to implement the same. When I want to implement the rate limiting by each user, I pass the username as the key which is unique. When I want to implement rate limiting by the IP address, I pass the IP address instead.

**Link**
<http://52.15.140.132:5000/home>

To register a user use the following command from the terminal
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"ABC","password":"ABC"}' http://52.15.140.132:5000/users


**USER TABLE**
  
  Name | Type
--- | ---
Username | String
Id | Integer, Primary key
Password_hash | String

Steps to run the project:
  1. Download all the files in a folder.
  2. Navigate to that folder using a terminal.
  3. run **python views.py** command in one terminal, in another terminal run **redis-server** and also run **python user_tester.py**.
     Running the user_tester file creates a user with username as "Rishabh" and password also as "Rishabh".
  4. Now you can visit <http://localhost:5000/home> which is Rate Limited on basis of user. That is one particular user can visit
     it specific number of times only in some fixed time interval. If the user gets Rate Limited, he has to wait for some time
     to again access the website.
  5. You can also visit <http://localhost:5000/api/resource> which is Rate Limited on basis of IP Address.
  6. You can also visiti <http://localhost:5000/api/resource/1> any number of times as this is not Rate Limited.
  7. Also please change the API key in mailgun.py and pagerduty.py. Also change the from and to fields in mailgun.py. You can      generate the keys by registering on the respective website.

**Technologies used:**
 1. Python
 2. Flask
 3. SqlAlchemy
 4. Pagerduty
 5. Mailgun

