## Installation

Clone the project

```bash
  git clone git@github.com:snilli/hotel-work-order.git 
```

Go to the project directory

```bash
  cd hotel-work-order/apps
```

Install dev dependencies with pip

```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements/requirements.dev.txt
  cp .env.example .env // fullfill value
  python manage.py createsuperuser
  python manage.py init_role

```

After init prepen above then start local server and go to `/admin` with super user account for create user and give role like Guest, Super User and Maid Super User
    
## Run Locally

Start the server

```bash
  cd hotel-work-order
  python manage.py runserver
```

## Run Docker

```bash
  cd hotel-work-order
  docker-compose up -d
```


## Improvement

### In business path

Now this project has work order management for managing work orders in the hotel, but some kind of service is still poor,  Can be improvement more features should implement to complete the hotel management system.

- maid job management
- room management
- amenity stock management
- technician management


and a lot of features for serving data to the higher view for analysis data for planning strategy and stock resource for reserve service in closing future.

### In tech path
Now using Postgres DB for storing data, But in production mode, May be could use Serverless RDS like AWS Aurora Serverless for serving data cause, Them can autoscaling capacity and in realword can't predictable workloads if we reserve big db size that mean big cost. 
