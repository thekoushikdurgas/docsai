"""
N8n JSON models for parsing workflow files from contact360/docsai/media/n8n and index.json.

These TypedDicts and helpers describe the shape of:
- Single workflow JSON files under media/n8n/
- media/n8n/index.json (catalog of workflows)

Used by N8nParser and N8nWorkflowLibraryService for type-safe access and validation.
"""

from typing import Any, Dict, List, Optional, TypedDict, Union


# ---------------------------------------------------------------------------
# Workflow file (single .json under media/n8n/)
# ---------------------------------------------------------------------------


class N8nWorkflowMeta(TypedDict, total=False):
    """Optional meta block at workflow root."""
    instanceId: str
    templateCredsSetupCompleted: bool


class N8nCredentialRef(TypedDict, total=False):
    """Per-credential reference on a node: credentials.pipedriveApi = { id, name }."""
    id: str
    name: str


# Node.credentials: dict of credential type name -> N8nCredentialRef
N8nNodeCredentials = Dict[str, N8nCredentialRef]


class N8nNode(TypedDict, total=False):
    """Single node in n8n workflow nodes[]. Required: id, name, type, position, parameters, typeVersion."""
    id: str
    name: str
    type: str
    position: List[Union[int, float]]
    parameters: Dict[str, Any]
    typeVersion: Union[int, float]
    credentials: N8nNodeCredentials
    webhookId: str
    retryOnFail: bool
    maxTries: int
    waitBetweenTries: int
    alwaysOutputData: bool


class N8nConnectionLink(TypedDict):
    """One link in connections: { node: targetNodeName, type: str, index: int }."""
    node: str
    type: str
    index: int


# connections[sourceNodeName][outputType] = list of list of N8nConnectionLink
# e.g. connections["Merge1"]["main"] = [[{ "node": "Globals2", "type": "main", "index": 0 }]]
N8nConnections = Dict[str, Dict[str, List[List[N8nConnectionLink]]]]


class N8nWorkflow(TypedDict, total=False):
    """Root workflow JSON. Required: nodes (list). connections usually present."""
    meta: Optional[N8nWorkflowMeta]
    name: str
    nodes: List[N8nNode]
    connections: N8nConnections
    pinData: Dict[str, Any]
    settings: Dict[str, Any]


# ---------------------------------------------------------------------------
# index.json (media/n8n/index.json)
# ---------------------------------------------------------------------------


class ConversionStats(TypedDict, total=False):
    """conversion_stats per workflow in index.json."""
    total_nodes: int
    supported_nodes: int
    partially_supported_nodes: int
    unsupported_nodes: int
    supported_types: List[str]
    unsupported_types: List[str]
    conversion_confidence: float


class IndexWorkflowEntry(TypedDict, total=False):
    """Single entry in index.json workflows[]."""
    id: str
    name: str
    description: str
    category: str
    n8n_path: str
    node_count: int
    conversion_stats: ConversionStats
    is_supported: bool
    size: int
    last_modified: Union[int, float]


class N8nIndex(TypedDict):
    """Root of media/n8n/index.json."""
    version: str
    last_updated: str
    total: int
    workflows: List[IndexWorkflowEntry]


# ---------------------------------------------------------------------------
# Parsing / validation layer: raw dict -> validated workflow or index
# ---------------------------------------------------------------------------


def parse_workflow(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate and normalize raw dict from a workflow JSON file.
    Returns the same dict if it has required keys (nodes); None otherwise.
    Handles meta: null, missing name, optional fields.
    """
    if not isinstance(raw, dict):
        return None
    if 'nodes' not in raw or not isinstance(raw.get('nodes'), list):
        return None
    # Normalize optional fields so consumers can assume structure
    if 'connections' not in raw:
        raw = {**raw, 'connections': {}}
    if not isinstance(raw.get('connections'), dict):
        raw = {**raw, 'connections': {}}
    return raw


def parse_index(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate and normalize raw dict from media/n8n/index.json.
    Returns the same dict if it has workflows list; None otherwise.
    """
    if not isinstance(raw, dict):
        return None
    workflows = raw.get('workflows')
    if not isinstance(workflows, list) or len(workflows) == 0:
        return None
    return raw
