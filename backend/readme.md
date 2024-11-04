# Python Code Execution Service

A FastAPI-based service that executes Python code securely within a Docker container. This service provides a REST API endpoint for remote code execution with timeout capabilities and proper error handling.

## Features

- 🐳 Dockerized Python execution environment
- 🚀 FastAPI REST API interface
- ⏱️ Configurable execution timeouts
- 🛡️ Secure execution in isolated environments
- 🔍 Detailed execution results including output and errors
- 📈 Resource usage limits
- 🏥 Health check endpoint

## Prerequisites

- Docker
- Docker Compose
- Git (optional)

## Installation

1. Clone or create the project directory:

```bash
mkdir python-execution-service
cd python-execution-service
```

2. Create the following directory structure:

```
python-execution-service/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

3. Build and start the service:

```bash
docker-compose up --build
```

4. Install and run MongoDB server locally
```bash
brew tap mongodb/brew
brew install mongodb-community

sudo brew services start mongodb-community
```

The service will be available at `http://localhost:8000`.

## API Endpoints

### Execute Code

- **Endpoint**: `POST /execute`
- **Content-Type**: `application/json`
- **Request Body**:

```json
{
    "code": "string",
    "timeout": "integer (optional, default: 5)"
}
```

- **Response**:

```json
{
    "output": "string",
    "error": "string (optional)",
    "execution_time": "float"
}
```

### Health Check

- **Endpoint**: `GET /health`
- **Response**:

```json
{
    "status": "healthy"
}
```

## Code Formatting

The service automatically handles code formatting issues to make it easier to send requests:

- Converts tabs to spaces
- Normalizes indentation levels
- Handles different newline formats (\n, \r\n)
- Preserves empty lines
- Removes common leading indentation

This means you can send code in various formats and the service will normalize it properly. For example, all these will work:

```python
# Example 1: Normal indentation
code = """
def hello():
    print("Hello")
    if True:
        print("World")
hello()
"""

# Example 2: Extra indentation (will be normalized)
code = """
        def hello():
            print("Hello")
            if True:
                print("World")
        hello()
"""

# Example 3: Mixed tabs and spaces (will be converted to spaces)
code = """
def hello():
	print("Hello")
	if True:
		print("World")
hello()
"""
```

## Usage Examples

### Using cURL

```bash
# Execute a simple Python code
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{
           "code": "print(\"Hello, World!\")\nresult = sum(range(10))\nprint(f\"Sum: {result}\")",
           "timeout": 5
         }'

# Check service health
curl http://localhost:8000/health
```

### Using Python

```python
import requests

def execute_code(code: str, timeout: int = 5):
    url = "http://localhost:8000/execute"
    response = requests.post(
        url,
        json={"code": code, "timeout": timeout}
    )
    return response.json()

# Example usage
code = """
print("Hello, World!")
result = sum(range(10))
print(f"Sum: {result}")
"""

result = execute_code(code)
print(result)
```

## Security Considerations

- Code executes in isolated temporary directories
- Execution timeouts prevent infinite loops
- Docker resource limits prevent container abuse
- Files are cleaned up after execution
- Container has limited system access

## Configuration

### Resource Limits (docker-compose.yml)

- CPU: 1 core
- Memory: 512MB

These limits can be adjusted in the `docker-compose.yml` file:

```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
```

## API Documentation

FastAPI provides automatic interactive API documentation. After starting the service, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

To run the service in development mode:

```bash
docker-compose up --build
```

The service includes hot-reloading, so changes to the code will automatically restart the server.

## License

[Choose appropriate license]

## Contributing

[Add contribution guidelines if needed]
