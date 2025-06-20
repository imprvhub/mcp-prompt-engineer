import asyncio
import aiohttp
import json
import os
import platform
import hashlib
from typing import Dict, List, Optional, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Prompt Engineer Helper")

BASE_URL = "https://prompt-engineer-helper.vercel.app"
MCP_VERSION = "1.0.0"
CLIENT_ID = "mcp_prompt_engineer_official"

# Generate a simple machine ID for session tracking
def get_machine_id() -> str:
    machine_info = f"{platform.node()}-{platform.system()}-{platform.machine()}"
    return hashlib.md5(machine_info.encode()).hexdigest()[:16]

class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = None
        self.session_token = None
        self.token_expires_at = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def authenticate(self) -> bool:
        """Authenticate with the API and get session token"""
        try:
            session = await self._get_session()
            auth_data = {
                "client_id": CLIENT_ID,
                "version": MCP_VERSION,
                "user_agent": f"mcp-prompt-engineer/{MCP_VERSION}",
                "machine_id": get_machine_id()
            }
            
            async with session.post(f"{self.base_url}/auth/mcp", json=auth_data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("success"):
                        data = result.get("data", {})
                        self.session_token = data.get("session_token")
                        self.token_expires_at = data.get("expires_at")
                        return True
                return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    async def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid session token"""
        if not self.session_token:
            return await self.authenticate()
        
        # Check if token is still valid by trying a simple request
        try:
            session = await self._get_session()
            headers = {'Authorization': f'Bearer {self.session_token}'}
            async with session.get(f"{self.base_url}/auth/status", headers=headers) as response:
                if response.status == 401:
                    # Token expired, re-authenticate
                    return await self.authenticate()
                return response.status == 200
        except:
            return await self.authenticate()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        # Ensure we're authenticated
        if not await self._ensure_authenticated():
            return {"error": "Failed to authenticate with API"}
        
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.session_token}'
        kwargs['headers'] = headers
        
        try:
            async with session.request(method, url, **kwargs) as response:
                if response.status == 401:
                    # Token might have expired mid-request, try to re-authenticate
                    if await self.authenticate():
                        headers['Authorization'] = f'Bearer {self.session_token}'
                        kwargs['headers'] = headers
                        async with session.request(method, url, **kwargs) as retry_response:
                            if retry_response.content_type == 'application/json':
                                return await retry_response.json()
                            else:
                                text = await retry_response.text()
                                return {"raw_content": text, "status_code": retry_response.status}
                    else:
                        return {"error": "Authentication failed"}
                
                if response.content_type == 'application/json':
                    return await response.json()
                else:
                    text = await response.text()
                    return {"raw_content": text, "status_code": response.status}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self._request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint: str, json_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self._request("POST", endpoint, json=json_data, **kwargs)
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

api_client = APIClient()

@mcp.tool()
async def get_all_services() -> Dict[str, Any]:
    """
    Get all available AI services and their file statistics.
    
    Returns:
        Dict containing all services with file counts and types
    """
    return await api_client.get("/services")

@mcp.tool()
async def get_service_details(service: str, file_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information about a specific service.
    
    Args:
        service (str): Service name (e.g., 'cursor-prompts', 'windsurf', 'replit')
        file_type (str, optional): Filter by file type (e.g., '.txt', '.json', '.md')
        
    Returns:
        Dict containing service details and all files
    """
    params = {}
    if file_type:
        params["file_type"] = file_type
    
    return await api_client.get(f"/services/{service}", params=params)

@mcp.tool()
async def get_file_content(service: str, file_path: str) -> Dict[str, Any]:
    """
    Get the content of a specific file from a service.
    
    Args:
        service (str): Service name (e.g., 'cursor-prompts', 'windsurf')
        file_path (str): File path within the service (e.g., 'prompt.txt', 'tools.json')
        
    Returns:
        Dict containing file content and metadata
    """
    return await api_client.get(f"/services/{service}/files/{file_path}")

@mcp.tool()
async def search_content(query: str, file_type: Optional[str] = None, services: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Search for content across all files or specific services.
    
    Args:
        query (str): Search term to look for in file contents
        file_type (str, optional): Filter by file type (e.g., '.txt', '.json')
        services (List[str], optional): Limit search to specific services
        
    Returns:
        Dict containing search results with matches and file locations
    """
    search_data = {"query": query}
    if file_type:
        search_data["file_type"] = file_type
    if services:
        search_data["services"] = services
    
    return await api_client.post("/search", search_data)

@mcp.tool()
async def get_multiple_services(services: List[str], file_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about multiple services in a single request.
    
    Args:
        services (List[str]): List of service names to retrieve
        file_type (str, optional): Filter by file type
        
    Returns:
        Dict containing information for all requested services
    """
    request_data = {"services": services}
    if file_type:
        request_data["file_type"] = file_type
    
    return await api_client.post("/services/multiple", request_data)

@mcp.tool()
async def get_all_prompts() -> Dict[str, Any]:
    """
    Get all prompt files (.txt files with 'prompt' in the name) from all services.
    
    Returns:
        Dict containing all prompts organized by service
    """
    return await api_client.get("/prompts")

@mcp.tool()
async def get_all_tools() -> Dict[str, Any]:
    """
    Get all tool configuration files (.json files with 'tool' in the name) from all services.
    
    Returns:
        Dict containing all tools organized by service
    """
    return await api_client.get("/tools")

@mcp.tool()
async def get_file_types() -> Dict[str, Any]:
    """
    Get all available file types and their distribution across services.
    
    Returns:
        Dict containing file types, extensions, and distribution statistics
    """
    return await api_client.get("/files/types")

@mcp.tool()
async def compare_services(service1: str, service2: str) -> Dict[str, Any]:
    """
    Compare two services to see their differences and similarities.
    
    Args:
        service1 (str): First service to compare
        service2 (str): Second service to compare
        
    Returns:
        Dict containing comparison analysis between the two services
    """
    return await api_client.get(f"/compare/{service1}/{service2}")

@mcp.tool()
async def get_api_statistics() -> Dict[str, Any]:
    """
    Get comprehensive statistics about the API data.
    
    Returns:
        Dict containing total files, services, distributions, and statistics
    """
    return await api_client.get("/stats")

@mcp.tool()
async def verify_authentication() -> Dict[str, Any]:
    """
    Verify that the MCP can communicate with the API and show session status.
    
    Returns:
        Dict containing connection status and session information
    """
    try:
        # Force authentication check
        authenticated = await api_client._ensure_authenticated()
        
        if not authenticated:
            return {
                "connected": False,
                "error": "Failed to authenticate with the API",
                "session_token": bool(api_client.session_token)
            }
        
        # Get session status
        result = await api_client.get("/auth/status")
        
        if "success" in result:
            return {
                "connected": True,
                "message": "MCP is successfully connected to the Prompt Engineer Helper API",
                "session_info": result.get("data", {}),
                "token_expires_at": api_client.token_expires_at
            }
        else:
            return {
                "connected": False,
                "error": result.get("error", "Unknown authentication error"),
                "session_token": bool(api_client.session_token)
            }
    except Exception as e:
        return {
            "connected": False,
            "error": f"Connection verification failed: {str(e)}",
            "session_token": bool(api_client.session_token)
        }

@mcp.tool()
async def refresh_session() -> Dict[str, Any]:
    """
    Manually refresh the API session token.
    
    Returns:
        Dict containing refresh status and new token information
    """
    try:
        result = await api_client.post("/auth/refresh", {})
        
        if "success" in result:
            data = result.get("data", {})
            api_client.session_token = data.get("session_token")
            api_client.token_expires_at = data.get("expires_at")
            
            return {
                "refreshed": True,
                "message": "Session token refreshed successfully",
                "expires_at": api_client.token_expires_at,
                "expires_in_hours": data.get("expires_in_hours")
            }
        else:
            return {
                "refreshed": False,
                "error": result.get("error", "Failed to refresh session")
            }
    except Exception as e:
        return {
            "refreshed": False,
            "error": f"Session refresh failed: {str(e)}"
        }

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check if the API is healthy and operational.
    Note: Health check endpoint doesn't require authentication.
    
    Returns:
        Dict containing API health status and service information
    """
    session = await api_client._get_session()
    url = f"{api_client.base_url}/health"
    
    try:
        async with session.get(url) as response:
            if response.content_type == 'application/json':
                return await response.json()
            else:
                text = await response.text()
                return {"raw_content": text, "status_code": response.status}
    except Exception as e:
        return {"error": f"Health check failed: {str(e)}"}

@mcp.tool()
async def get_cursor_prompts() -> Dict[str, Any]:
    """
    Quick access to all Cursor prompts and tools.
    
    Returns:
        Dict containing all Cursor-related prompts and configurations
    """
    return await api_client.get("/services/cursor-prompts")

@mcp.tool()
async def get_windsurf_config() -> Dict[str, Any]:
    """
    Quick access to Windsurf prompts and tools configuration.
    
    Returns:
        Dict containing Windsurf prompts and tools
    """
    return await api_client.get("/services/windsurf")

@mcp.tool()
async def get_replit_config() -> Dict[str, Any]:
    """
    Quick access to Replit prompts and tools configuration.
    
    Returns:
        Dict containing Replit prompts and tools
    """
    return await api_client.get("/services/replit")

@mcp.tool()
async def get_open_source_prompts() -> Dict[str, Any]:
    """
    Quick access to all open source prompts (bolt, cline, codex-cli, roo-code).
    
    Returns:
        Dict containing all open source prompts
    """
    return await api_client.get("/services/open-source-prompts")

@mcp.tool()
async def search_prompts_only(query: str) -> Dict[str, Any]:
    """
    Search specifically in prompt files (.txt files) across all services.
    
    Args:
        query (str): Search term to look for in prompt files
        
    Returns:
        Dict containing search results from prompt files only
    """
    return await search_content(query, file_type=".txt")

@mcp.tool()
async def search_tools_only(query: str) -> Dict[str, Any]:
    """
    Search specifically in tool configuration files (.json files) across all services.
    
    Args:
        query (str): Search term to look for in tool files
        
    Returns:
        Dict containing search results from tool files only
    """
    return await search_content(query, file_type=".json")

@mcp.tool()
async def find_agent_prompts() -> Dict[str, Any]:
    """
    Find all prompts related to 'agent' functionality across all services.
    
    Returns:
        Dict containing all agent-related prompts and their locations
    """
    return await search_content("agent")

@mcp.tool()
async def find_chat_prompts() -> Dict[str, Any]:
    """
    Find all prompts related to 'chat' functionality across all services.
    
    Returns:
        Dict containing all chat-related prompts and their locations
    """
    return await search_content("chat")

@mcp.tool()
async def get_specific_prompt(service: str, prompt_name: str) -> Dict[str, Any]:
    """
    Get a specific prompt file from a service.
    
    Args:
        service (str): Service name (e.g., 'cursor-prompts', 'windsurf')
        prompt_name (str): Prompt file name (e.g., 'prompt.txt', 'agent-prompt.txt')
        
    Returns:
        Dict containing the specific prompt content
    """
    return await get_file_content(service, prompt_name)

@mcp.tool()
async def get_specific_tool_config(service: str, tool_name: str) -> Dict[str, Any]:
    """
    Get a specific tool configuration file from a service.
    
    Args:
        service (str): Service name (e.g., 'cursor-prompts', 'windsurf', 'replit')
        tool_name (str): Tool file name (e.g., 'tools.json', 'agent-tools-v1-0.json')
        
    Returns:
        Dict containing the specific tool configuration
    """
    return await get_file_content(service, tool_name)

@mcp.tool()
async def get_ai_services_overview() -> Dict[str, Any]:
    """
    Get a comprehensive overview of all AI services, their capabilities, and available resources.
    
    Returns:
        Dict containing overview of all services with statistics and file information
    """
    services_data = await get_all_services()
    stats_data = await get_api_statistics()
    
    return {
        "services": services_data,
        "statistics": stats_data,
        "overview": "Complete overview of all available AI services and their resources"
    }

async def cleanup():
    """Cleanup function to close HTTP session"""
    await api_client.close()

if __name__ == "__main__":
    import atexit
    atexit.register(lambda: asyncio.run(cleanup()))