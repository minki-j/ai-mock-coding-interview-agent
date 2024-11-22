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

### Option 1. Using Docker
```bash
cd backend
docker-compose up --build
```

### Option 2.

Start FastAPI server
```bash
cd backend
python main.py
```

Start MongoDB server (macOS)
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

### Get All Interview Questions

- **Endpoint**: `GET /get_interview_questions`
- **Response**: List of LeetcodeQuestion objects
```json
[
    {
        "id": "string",
        "title": "string",
        "difficulty": "string",
        "question": "string",
        "solution": "string"
        // ... other LeetcodeQuestion fields
    }
]
```

### Alternative: Get Specific Interview Question

```markdown
## API Documentation

### Get Interview Questions
Retrieves a list of available LeetCode questions filtered by the Grind 75 question set.

```http
GET /get_interview_questions
```

#### Response
Returns an array of `LeetcodeQuestion` objects.

```typescript
{
  id: string;
  title: string;
  difficulty: string;
  category: string;
  // ... other LeetcodeQuestion properties
}[]
```

#### Error Handling
- If `leetcode.json` is not found, returns `404 Not Found`
- If file is corrupted/invalid JSON, returns `500 Internal Server Error`

### Get Test File
Retrieves the test file for a specific LeetCode problem.

```http
GET /prep/{leetcode_number}_test.py
```

#### Parameters
- `leetcode_number` (path): The LeetCode question identifier

#### Error Handling
- If test file is not found, returns `404 Not Found` with message:
  ```json
  {
    "detail": "Test file for {leetcode_number} not found"
  }
  ```

#### Notes
- Questions are filtered based on the Grind 75 question set
- Test files should be placed in the `db/prep/` directory
- File naming convention: `{leetcode_number}_test.py`


### Get Specific Interview Question

- **Endpoint**: `GET /get_interview_question/{id}`
- **Parameters**:
  - `id`: string (path parameter)
- **Response**: Single LeetcodeQuestion object
```json
{
    "id": "string",
    "title": "string",
    "difficulty": "string",
    "question": "string",
    "solution": "string"
    // ... other LeetcodeQuestion fields
}
```
- **Error Response** (404):
```json
{
    "detail": "Question with id {id} not found"
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

### Get Single Interview Question
endpoint: GET /get_interview_question/{id}

### Get Single Interview Question
Retrieves detailed information about a specific LeetCode question, including its preparation code.

```http
GET /get_interview_question/{id}
```

#### Parameters
- `id` (path): The LeetCode question identifier (string)

#### Response
Returns a `LeetcodeQuestion` object enhanced with preparation code:

```typescript
{
  id: string;
  title: string;
  difficulty: string;
  category: string;
  prep_code: string[];  // Array of code lines from the preparation file
  // ... other LeetcodeQuestion properties
}
```

#### Error Handling
- If question ID is not found in the question set:
  ```json
  {
    "detail": "Question with id {id} not found"
    "status_code": 404
  }
  ```

#### Notes
- Automatically loads associated preparation code from `db/prep/{id}.py` if available
- If prep file is not found, `prep_code` will be an empty array
- Question must exist in the Grind 75 question set to be retrievable


### Debug LeetCode Solution
Debugs and attempts to fix a user's LeetCode solution using AI assistance.

```http
POST /debug_code
```

#### Request Body
```json
{
  "leetcode_number": string,  // LeetCode question identifier
  "user_solution": string     // User's code solution attempt
}
```

#### Response
On Success (200):
```json
{
  "status": "success",
  "solution": string,     // Working solution code
  "explanation": string   // Explanation of fixes made
}
```

On Failure (400):
```json
{
  "detail": "Code is not working",
  "debug_result": object,
  "debug_explanation": string,
  "debug_solution": string
}
```

#### Error Handling
- If test file is not found (404):
  ```json
  {
    "detail": "Test file for {leetcode_number} not found"
  }
  ```

#### Process
1. Loads test file from `db/prep/{leetcode_number}_test.py`
2. Makes up to 3 attempts to fix the code:
   - Combines user solution with test code
   - Executes combined code with 5-second timeout
   - If execution fails, uses AI to analyze and fix the code
3. Returns either:
   - Successfully fixed solution with explanation
   - Final debugging attempt results if unsuccessful

#### Notes
- Test files must exist in `db/prep/` directory
- Uses AI-powered debugging for intelligent fix suggestions
- Maximum execution time of 5 seconds per attempt
- Maximum of 3 debugging attempts before failing


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
