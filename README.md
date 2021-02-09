# HR APP

## Requirements
- Linux OS
- Docker: https://docs.docker.com/engine/install
- Docker Compose: https://docs.docker.com/compose/install

## Steps

- Open a new terminal.
- Clone the repo into hr-app directory.
- Change the working directory to the above directory.
- Run this command `docker-compose up -d` to build and start the project.
- Run this command `docker exec -it hr-app tail -fn444 /var/log/flask-hr-app.log` for outputting the log file. 
- Open another terminal to test the below APIs.

## Endpoints


- Create new candidate API.

```
curl 'http://localhost:5000/v1/create/candidate' \
  -X 'POST' \
  -F file=@<PATH_TO_PDF_OR_DOCX_FILE> \
  -F 'department=IT' \
  -F 'name=Ali' \
  -F 'yoe=1' \
  -F 'birth_date=2000-10-10'
```

- List all applicants API.

```
curl 'http://localhost:5000/v1/applicants' -H 'X-ADMIN: 1'
```

- Download resume API.

```
curl 'http://localhost:5000/v1/download/resume/<APPLICANT_ID>' -H 'X-ADMIN: 1' --output <FILE-NAME>
```

## Rebuild and start the project

- `docker-compose down -v && docker-compose build --no-cache  && docker-compose up -d`


