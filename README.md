# AI Mock Coding Interview Agent

## Running on Docker

Before you run the docker compose file, please fill in the environment variable in backend/.env file.

After you have the environment variables set, you can run the docker compose file.

```bash
docker compose up --build -d
```
If you want to see the full running logs, remove the `-d` flag.

To stop the services, run:

```bash
docker compose down
```

or `Ctrl + C` in the terminal where docker compose is running.

## HotFix

I have encountered an issue that frontend is telling me that `jwt-decode` is not found. However, it is installed. I have no idea why it is not being detected. So for now, you can run `npm install jwt-decode` to fix the issue.

```bash
docker compose exec frontend npm install jwt-decode
```

`frontend` is the name of the service in the docker compose file.

## Accessing the App

After the services are running, you can access the app at `http://localhost:3001`.
Since the local files are mounted into the container, any changes you make to the files will be reflected in the app.

## Contributing

If you want to add more questions, you can do so by adding the question to the `leetcode.json` file.
Make sure to add the question to the correct category.
