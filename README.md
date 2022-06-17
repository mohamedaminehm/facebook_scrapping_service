# facebook_scrapping_service
Basic Python Fastapi app in Docker which scrape from facebook giving page name

### Build application
Build and run the Dockerized application by cloning the Git repo.
```
$ git clone https://github.com/mohamedaminehm/facebook_scrapping_service.git
$ docker-compose up --build
```

- visit http://localhost:5000 for demo


- visit http://localhost:5000/docs for documentation


### Run Tests
Enter bash commands into running server container
```
$ docker exec -it app_fastapi bash
```
Run the pytest command
```
$ pytest -v
```
