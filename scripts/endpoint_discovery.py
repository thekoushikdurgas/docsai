"""Discover all API endpoints by parsing router files using AST."""

import ast
import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from endpoint_test_config import (
    API_ENDPOINTS_DIR,
    API_V1_PREFIX,
    API_V2_PREFIX,
    API_V3_PREFIX,
    API_V4_PREFIX,
    BACKEND_DIR,
)


@dataclass
class EndpointInfo:
    """Information about a discovered API endpoint."""
    method: str  # GET, POST, PUT, DELETE, PATCH, WEBSOCKET
    path: str  # Route path (e.g., "/login/")
    full_path: str  # Full path with API prefix (e.g., "/api/v2/auth/login/")
    description: str  # Docstring or brief description
    api_version: str  # v1, v2, v3, v4, or global
    category: str  # Category/service name (e.g., "Authentication", "Contacts")
    file_path: str  # Source file path
    function_name: str  # Function name
    requires_auth: bool = False  # Will be determined during testing
    requires_admin: bool = False  # Will be determined during testing


class EndpointDiscovery:
    """Discovers all API endpoints from router files."""
    
    def __init__(self):
        self.endpoints: List[EndpointInfo] = []
        self.router_prefixes: Dict[str, Dict[str, str]] = {}
        
    def discover_all(self) -> List[EndpointInfo]:
        """Discover all endpoints across all API versions."""
        # Discover global endpoints from main.py
        self._discover_global_endpoints()
        
        # Discover v1 endpoints
        self._discover_version_endpoints("v1", API_V1_PREFIX)
        
        # Discover v2 endpoints
        self._discover_version_endpoints("v2", API_V2_PREFIX)
        
        # Discover v3 endpoints
        self._discover_version_endpoints("v3", API_V3_PREFIX)
        
        # Discover v4 endpoints
        self._discover_version_endpoints("v4", API_V4_PREFIX)
        
        return self.endpoints
    
    def _discover_global_endpoints(self):
        """Discover global endpoints from main.py."""
        main_py = Path(BACKEND_DIR) / "app" / "main.py"
        if not main_py.exists():
            return
        
        try:
            tree = ast.parse(main_py.read_text(encoding="utf-8"))
            visitor = RouterVisitor("global", "/", "Global", str(main_py))
            visitor.visit(tree)
            
            for endpoint in visitor.endpoints:
                endpoint.api_version = "global"
                endpoint.category = "Global"
                self.endpoints.append(endpoint)
        except Exception as e:
            print(f"Warning: Could not parse {main_py}: {e}")
    
    def _discover_version_endpoints(self, version: str, api_prefix: str):
        """Discover endpoints for a specific API version."""
        version_dir = Path(API_ENDPOINTS_DIR) / version / "endpoints"
        if not version_dir.exists():
            print(f"Warning: {version_dir} does not exist")
            return
        
        # Parse the version's api.py to understand router structure
        api_py = Path(API_ENDPOINTS_DIR) / version / "api.py"
        router_map = self._parse_router_includes(api_py, version)
        
        # Discover endpoints from each endpoint file
        endpoint_files = list(version_dir.glob("*.py"))
        if not endpoint_files:
            print(f"Warning: No Python files found in {version_dir}")
            return
        
        for endpoint_file in sorted(endpoint_files):
            if endpoint_file.name.startswith("__"):
                continue
            
            # Determine category from filename
            category = endpoint_file.stem.replace("_", " ").title()
            
            # Get router prefix from router_map
            router_prefix = router_map.get(endpoint_file.stem, "")
            
            try:
                content = endpoint_file.read_text(encoding="utf-8")
                tree = ast.parse(content)
                visitor = RouterVisitor(
                    version, 
                    api_prefix, 
                    category, 
                    str(endpoint_file),
                    router_prefix
                )
                visitor.visit(tree)
                
                for endpoint in visitor.endpoints:
                    endpoint.api_version = version
                    endpoint.category = category
                    self.endpoints.append(endpoint)
            except Exception as e:
                print(f"Warning: Could not parse {endpoint_file}: {e}")
                import traceback
                traceback.print_exc()
    
    def _parse_router_includes(self, api_py: Path, version: str) -> Dict[str, str]:
        """Parse api.py to extract router prefixes."""
        router_map = {}
        
        if not api_py.exists():
            return router_map
        
        try:
            tree = ast.parse(api_py.read_text(encoding="utf-8"))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Look for include_router calls
                    if (isinstance(node.func, ast.Attribute) and 
                        node.func.attr == "include_router"):
                        
                        # Get router name (first arg)
                        if node.args:
                            router_arg = node.args[0]
                            router_name = None
                            
                            if isinstance(router_arg, ast.Attribute):
                                router_name = router_arg.attr
                            elif isinstance(router_arg, ast.Name):
                                router_name = router_arg.id
                            
                            # Get prefix from keyword args
                            prefix = ""
                            for keyword in node.keywords:
                                if keyword.arg == "prefix":
                                    if isinstance(keyword.value, ast.Constant):
                                        prefix = keyword.value.value
                            
                            if router_name:
                                router_map[router_name] = prefix
        except Exception as e:
            print(f"Warning: Could not parse router includes from {api_py}: {e}")
        
        return router_map


class RouterVisitor(ast.NodeVisitor):
    """AST visitor to extract route decorators and endpoints."""
    
    def __init__(self, version: str, api_prefix: str, category: str, 
                 file_path: str, router_prefix: str = ""):
        self.version = version
        self.api_prefix = api_prefix
        self.category = category
        self.file_path = file_path
        self.router_prefix = router_prefix
        self.endpoints: List[EndpointInfo] = []
        self.current_router_prefix = ""
        
    def visit_Assign(self, node):
        """Extract router prefix from router = APIRouter(prefix=...) assignments."""
        if isinstance(node.value, ast.Call):
            if (isinstance(node.value.func, ast.Name) and 
                node.value.func.id == "APIRouter"):
                # Check for prefix in keyword args
                for keyword in node.value.keywords:
                    if keyword.arg == "prefix":
                        if isinstance(keyword.value, ast.Constant):
                            self.current_router_prefix = keyword.value.value
        self.generic_visit(node)
    
    def _process_function(self, node):
        """Extract route decorators from function definitions (both sync and async)."""
        method = None
        route_path = None
        description = ""
        
        # Extract docstring
        if ast.get_docstring(node):
            description = ast.get_docstring(node).strip().split("\n")[0]
        
        # Look for route decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    # Check for @router.get, @router.post, etc.
                    # Also check if the attribute name is "router" or similar
                    attr_name = decorator.func.attr
                    if attr_name in ("get", "post", "put", "delete", "patch", "websocket"):
                        method = attr_name.upper()
                        if attr_name == "websocket":
                            method = "WEBSOCKET"
                        
                        # Extract path from decorator args
                        if decorator.args:
                            path_arg = decorator.args[0]
                            if isinstance(path_arg, ast.Constant):
                                route_path = path_arg.value
                            elif isinstance(path_arg, ast.Str):  # Python < 3.8
                                route_path = path_arg.s
                        
                        # If no path in args, check for default "/"
                        if not route_path:
                            route_path = "/"
        
        if method and route_path:
            # Build full path
            full_path = self.api_prefix
            if self.router_prefix:
                full_path += self.router_prefix
            if self.current_router_prefix:
                full_path += self.current_router_prefix
            
            # Ensure route_path starts with /
            if not route_path.startswith("/"):
                route_path = "/" + route_path
            
            full_path += route_path
            
            # Normalize path (remove double slashes, ensure trailing slash consistency)
            full_path = full_path.replace("//", "/")
            
            endpoint = EndpointInfo(
                method=method,
                path=route_path,
                full_path=full_path,
                description=description or f"{method} {route_path}",
                api_version=self.version,
                category=self.category,
                file_path=self.file_path,
                function_name=node.name
            )
            self.endpoints.append(endpoint)
    
    def visit_FunctionDef(self, node):
        """Handle synchronous function definitions."""
        self._process_function(node)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Handle asynchronous function definitions."""
        self._process_function(node)
        self.generic_visit(node)


def discover_endpoints() -> List[EndpointInfo]:
    """Main function to discover all endpoints."""
    discovery = EndpointDiscovery()
    return discovery.discover_all()


if __name__ == "__main__":
    # Test the discovery
    import sys
    print(f"API_ENDPOINTS_DIR: {API_ENDPOINTS_DIR}")
    print(f"BACKEND_DIR: {BACKEND_DIR}")
    print(f"Checking v2 endpoints dir: {Path(API_ENDPOINTS_DIR) / 'v2' / 'endpoints'}")
    print(f"Exists: {(Path(API_ENDPOINTS_DIR) / 'v2' / 'endpoints').exists()}")
    
    endpoints = discover_endpoints()
    print(f"\nDiscovered {len(endpoints)} endpoints:")
    for endpoint in endpoints[:20]:  # Print first 20
        print(f"  {endpoint.method} {endpoint.full_path} - {endpoint.description}")
    if len(endpoints) > 20:
        print(f"... and {len(endpoints) - 20} more")
