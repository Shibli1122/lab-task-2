sudo apt update -y

# 1. Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# 2. Start and enable the database service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 3. Create the database and user exactly as your Python script expects
sudo -u postgres psql -c "CREATE DATABASE portfolio_db;"
sudo -u postgres psql -c "CREATE USER portfolio_user WITH PASSWORD 'portfolio_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;"
sudo -u postgres psql -d portfolio_db -c "GRANT ALL ON SCHEMA public TO portfolio_user;"