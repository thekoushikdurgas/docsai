### About

For use in agentic ReAct pattern (reasoning and acting), generates JSON definition and Python/JavaScript/TypeScript implementation of tool to invoke public Postman collection request. Supported agent frameworks include: OpenAI, Anthropic, Gemini, Mistral, AutoGen, and LangChain.

### Prerequisites

- Postman Account
    
- OpenAI Account: [https://platform.openai.com/](https://platform.openai.com/)
    

### Usage

1. Create a fork
    
2. Update collection variables
    
3. Go to tool generation request and run
    
4. Go to function calling request, update function value with JSON definition, and run
    

### Example

This collection, tool generation request, language Python, agent framework OpenAI:

``` python
import requests
def generate_tool(collection_id, request_id, language="python", agent_framework="openai"):
    """
    Function to generate a tool using the Postman API.
    :param collection_id: The ID of the collection to which the tool belongs.
    :param request_id: The ID of the request for which the tool is generated.
    :param language: The programming language for the generated tool (default: "python").
    :param agent_framework: The agent framework to be used (default: "openai").
    :return: The response from the tool generation request as a dictionary.
    """
    base_url = "https://api.getpostman.com/postbot/generations/tool"
    api_key = ""  # will be provided by the user
    payload = {
        "collectionId": collection_id,
        "requestId": request_id,
        "config": {
            "language": language,
            "agentFramework": agent_framework
        }
    }
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(base_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating tool: {e}")
        return {"error": "An error occurred while generating the tool."}
api_tool = {
    "function": generate_tool,
    "definition": {
        "name": "generate_tool",
        "description": "Generate a tool using the Postman API.",
        "parameters": {
            "type": "object",
            "properties": {
                "collection_id": {
                    "type": "string",
                    "description": "The ID of the collection to which the tool belongs."
                },
                "request_id": {
                    "type": "string",
                    "description": "The ID of the request for which the tool is generated."
                },
                "language": {
                    "type": "string",
                    "description": "The programming language for the generated tool."
                },
                "agent_framework": {
                    "type": "string",
                    "description": "The agent framework to be used."
                }
            },
            "required": ["collection_id", "request_id"]
        }
    }
}
# If this script is imported as a module, we expose `api_tool`
__all__ = ["api_tool"]

 ```