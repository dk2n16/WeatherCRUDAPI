# WeatherCRUDAPI
API for weather

## Reflections
At the bottom of the README is the intended workflow for the devlopment of this API within 2-hours. Unfortunately, I was only able to get to step 10 (CICD pipeline). Time permitting, I may have considered the following:
1. Set up Swagger/OpenAPI page as documentation and sandbox in which to test API hands on.
2. Create another `db table` dict holding users, their hashed passwords and roles. I would then add a `/weather/login` endpoint which returns a `JWT token`. I would then add decorators to the `POST`, `DELETE` and `PUT` endpoints to check the `Bearer token` in the request to ascertain whether users were authorised to make changes to the database.
3. Add `async` functionality
4. Create a `Docker` file and `docker-compose.yaml` for installation convenience and to possibly run the app in a `minikube/kind` cluster. 

Based on the brief, I developed under the assumption that the database would only hold **one** record per city, with the timestamp indicating when changes were made to the record. If the intention was to hold multiple records per city, I might have used the timestamp (`DD-MM-YYYY` format) as the dict key (primary key) of the database, and add multiple unique cities per timestamp. The API could then request cities by their date.

## Set up

### UV Pacakge manager
This API was developed using Flask3 using [UV](https://docs.astral.sh/uv/) as a package manager using `Python 3.12`. If users have `UV` installed, dependencies can be installed by running:
```bash
uv sync
```
The application can be started by either:
- Running the `UV` command:
```bash
uv run flask run --port 5000
```
OR
- Instantiating the environment created in the sync command:
```bash
source .venv/bin/activate
```
and then starting the application as a `Python` command:
```bash
flask run --port 5000
```

### Using pip
If `UV` is not installed, users can install create a virtual environment and run the appropriate `pip` or `pipenv` commands:
```bash
pip install -r requirements.txt
```

OR 

```bash
pipenv install -r requirements.txt
```

## API Usage
The API endpoints are defined in `./app/api.py`. There was not sufficient to create an OpenAPI docs page. With the app running, the API can be queried using the following examples.

### Endpoints

#### Create a Weather Report
**POST** `/weather/<city>`

- **Body (JSON):**
  ```json
  {
    "temperature": 20.0,
    "condition": "Sunny"
  }
  ```
- **Example:**
  ```bash
  curl -X POST http://localhost:5000/weather/london \
    -H "Content-Type: application/json" \
    -d '{"temperature": 20.0, "condition": "Sunny"}'
  ```

#### Get a Weather Report
**GET** `/weather/<city>`

- **Example:**
  ```bash
  curl http://localhost:5000/weather/london
  ```

#### Update a Weather Report
**PUT** `/weather/<city>`

- **Body (JSON):**
  ```json
  {
    "temperature": 22.0,
    "condition": "Cloudy"
  }
  ```
- **Example:**
  ```bash
  curl -X PUT http://localhost:5000/weather/london \
    -H "Content-Type: application/json" \
    -d '{"temperature": 22.0, "condition": "Cloudy"}'
  ```

#### Delete a Weather Report
**DELETE** `/weather/<city>`

- **Example:**
  ```bash
  curl -X DELETE http://localhost:5000/weather/london
  ```

## Testing
Simple unit tests are defined in the `tests` directory. 
To run the test suite, make sure your virtual environment is activated and all dependencies are installed (using `uv sync` or `pip install -r requirements.txt`).

Then run:

```bash
pytest tests
```

This will run all tests in the `tests/` directory, including:

- Endpoint tests for all CRUD operations (`POST`, `GET`, `PUT`, `DELETE`)
- Validation tests for invalid input data
- Tests for correct error handling (e.g., non-existent cities)

A test client `fixture` and in-memory database `fixture` are defined in the `tests/conftest.py` file.

You can also run linting, pip-audit and type checks with:

```bash
./scripts/linting_typing.sh
```

## CI Pipeline
A simple CI pipeline for the associated Github repository has been defined in `.github/workflows/`. When pushing to a branch or merging a pull request, the pipeline will run automatically in Github, installing the dependencies in an `Ubuntu` container, runing the unit tests and finally the linting script. Merges cannot proceed unless this pipeline passes.

## Steps to complete
**TASKS COMPLETE**
1. Install dependencies
2. Set up simple API
3. Write POST, GET, PUT, DELETE endpoints
4. Make datatypes
5. Validation
6. Database dict
7. Error handling
8. Tests
9. Local linting and type checks
10. CI/CD
**STILL TODO**
11. Swagger docs
12. Authentication and roles/permissions
13. uvi/gunicorn
14. docker and docker-compose
15. database
16. Integration tests
17. Load/stress tests
18. Kubernetes/minikube (?)