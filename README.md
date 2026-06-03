# Lab Task 2: Practice exercises for understanding Docker and containerization concepts.



#This command removes Windows-style carriage return characters (\r) from the listed files to convert their line endings to Unix format (LF)
```bash
sed -i 's/\r$//' DB_Setup.sh Dockerfile Dockerfile.frontend backend_server.js database_service.py
```


#This command grants executable permissions to the DB_Setup.sh script, allowing it to be run directly as a program.
```bash
chmod +x DB_Setup.sh
```



#This command executes the DB_Setup.sh script from the current directory, typically initializing and configuring your database.
```bash
./DB_Setup.sh
```



#This command builds a Docker image named portfolio-backend using the configuration specified in Dockerfile from the current directory.
```bash
sudo docker build -t portfolio-backend -f Dockerfile .
```




#This command runs the portfolio-backend image as a background container named backend-container using the host's network stack directly.
```bash
sudo docker run -d --name backend-container --network host portfolio-backend
```




# Build the frontend image
```bash
sudo docker build -t portfolio-frontend -f Dockerfile.frontend .
```



# Run the frontend container, mapping port 3000
```bash
sudo docker run -d --name frontend-container -p 3000:3000 portfolio-frontend
```



#These are URLs used to access your web application or backend service running on port 3000 via your EC2 instance's public IP address.
```
http://<YOUR_EC2_PUBLIC_IP>:3000
http://13.62.103.147:3000
```

#**To test data in DB:-** 
#This command connects to the PostgreSQL database as the postgres user and executes a SQL query to display all rows from the messages table inside the portfolio_db database.
```bash
sudo -u postgres psql -d portfolio_db -c "SELECT * FROM messages;"



#This command sends a HTTP POST request to a local API endpoint (/api/contact) with a JSON payload containing a name, email, and 
message to test contact form submission.
```bash
curl -X POST http://localhost:5000/api/contact \
     -H "Content-Type: application/json" \
     -d '{"name":"Terminal Test","email":"test@test.com","message":"Did this work?"}'
```





