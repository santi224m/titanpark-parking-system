
  

<a  id="readme-top"></a>

  

[![Contributors][contributors-shield]][contributors-url] [![Issues][issues-shield]][issues-url] [![Python][Python]][Python-url]

  

<!-- PROJECT LOGO -->

<br />

<div align="center">

<a  href="https://github.com/santi224m/titanpark-parking-system">

<img  src="/assets/img/parking.svg"  alt="Logo"  height="60">

</a>

  

<h3 align="center">TitanPark Parking System</h3>

  

<p align="center">

This microservice handles parking space listings and dynamic pricing for the <a  href="https://github.com/nathanchamorro1/titanpark">TitanPark mobile app</a>.

<br />

<br />

<a  href="https://github.com/santi224m/titanpark-parking-system/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>

·

<a  href="https://github.com/santi224m/titanpark-parking-system/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>

</p>

</div>

  

<!-- GETTING STARTED -->

##  Getting Started

  

Clone the repository.

  

```bash

git clone  git@github.com:santi224m/titanpark-parking-system.git

cd titanpark-parking-system/

```

<br />

  

Create a virtual environment.

  

```bash

python -m  venv  .venv
source .venv/bin/activate

```

<br />

  

Install requirements.

  

```bash

pip install  -r  requirements.txt

```

<br />

  

## Database Setup

**Option A: (recommended) Using Docker:**
This will automatically start a PostgreSQL container with the correct credentials.

```bash
    docker compose up -d db
```

Once the container is running, set the database URL and run migrations:
```bash
    export DATABASE_URL=postgresql://postgres:titanpark@localhost:5432/titanpark_parking_system
    alembic upgrade head
```

This creates all required tables and inserts the default parking structures:

```bash
    1 | Nutwood Structure  
    2 | State College Structure  
    3 | Eastside North  
    4 | Eastside South
```

**Option B: Using a local PostgreSQL install:**

```bash
    # create the database (first time only)
    psql -U postgres -d postgres -f database/setup.sql
    
    # set connection URL
    export DATABASE_URL=postgresql://postgres@localhost:5432/titanpark_parking_system
    
    # apply migrations
    alembic upgrade head
```
  

<br />

  ## Run the Server

Start the [fastapi](https://fastapi.tiangolo.com/) server.

  

```bash

fastapi dev  src/main.py

```

  

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in the browser.

  

##  Testing

  

We use ```pytest``` to run unit tests. Running the code below will output a coverage report as html.

  

```bash

cd src/

pytest --cov=main  --cov-report=html  --cov-report=term-missing

```

  

##  API Routes

  

| Method | Endpoint | Description | Parameters | Response |

|--------|----------|-------------|------------|----------|

| GET | `/parking_data/all` | Get live parking data for all parking structures | None | JSON with all parking structure data |

| GET | `/parking_data/{struct_name}` | Get live parking data for a specific parking structure | `struct_name` (path) - Name of the parking structure | JSON with specific parking structure data |

| POST | `/add_vehicle` | Add a user's vehicle to the database | `user_id` (query), `make` (query), `model` (query), `year` (query), `color` (query), `license_plate` (query) | Confirmation response |

| GET | `/get_user_vehicles` | Get a list of vehicles belonging to a user | `user_id` (query) - User identifier | JSON array of user's vehicles |
| POST | `/delete_vehicle` | Delete a vehicle from the database | `vehicle_id` (query) | Confirmation response |

| POST | `/add_listing` | Add a listing to the database | `user_id` (query), `price` (query), `structure_id` (query), `floor` (query), `vehicle_id` (query), `comment` (query) | Confirmation response |

| GET | `/get_listings` | Get a list of all currently available listings | None | JSON array of all available listings |

  

##  Top Contributors

  

<a  href="https://github.com/santi224m/titanpark-parking-system/graphs/contributors">

<img  src="https://contrib.rocks/image?repo=santi224m/titanpark-parking-system"  alt="contrib.rocks image" />

</a>

  

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/santi224m/titanpark-parking-system.svg?style=for-the-badge

[contributors-url]: https://github.com/santi224m/titanpark-parking-system/graphs/contributors

[issues-shield]: https://img.shields.io/github/issues/santi224m/titanpark-parking-system.svg?style=for-the-badge

[issues-url]: https://github.com/santi224m/titanpark-parking-system/issues

  

[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python

[Python-url]: https://www.python.org/