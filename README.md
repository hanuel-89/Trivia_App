# API Reference
## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, while the React frontend is hosted at http://127.0.0.1:3000/
- Authentication: This version of the application does not require authentication or API keys.
## Error Handling
Errors are returned as JSON objects in the following format:
```bash
pip install -r requirements.txt
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 422: Not processable

## Endpoints