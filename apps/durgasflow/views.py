"""
Durgasflow Views - Workflow Automation UI

Template views for the workflow automation interface.
"""

import json
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.core.paginator import Paginator

from apps.core.decorators.auth import require_super_admin
from .services.workflow_service import WorkflowService
from .services.execution_engine import ExecutionEngine
from .services.workflow_storage_service import (
    WorkflowStorageService,
    CredentialStorageService,
    WorkflowTemplateStorageService
)
from .services.n8n_library_service import N8nWorkflowLibraryService

logger = logging.getLogger(__name__)

# Status choices (moved from models)
class WorkflowStatus:
    DRAFT = 'draft'
    ACTIVE = 'active'
    PAUSED = 'paused'
    ARCHIVED = 'archived'
    choices = [
        (DRAFT, 'Draft'),
        (ACTIVE, 'Active'),
        (PAUSED, 'Paused'),
        (ARCHIVED, 'Archived'),
    ]

class ExecutionStatus:
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    choices = [
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (CANCELLED, 'Cancelled'),
    ]


@require_super_admin
def workflow_hub(request):
    """Unified workflow hub with tabs: My Workflows, n8n Library, Templates, Executions."""
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')

    tab = request.GET.get('tab', 'my_workflows')
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    trigger_filter = request.GET.get('trigger', '')
    category_filter = request.GET.get('category', '')

    workflow_storage = WorkflowStorageService()
    template_storage = WorkflowTemplateStorageService()

    # My Workflows tab
    filters = {'created_by': user_uuid}
    if status_filter:
        filters['status'] = status_filter
    if trigger_filter:
        filters['trigger_type'] = trigger_filter
    workflows_result = workflow_storage.list(filters=filters, limit=None, offset=0)
    my_workflows = workflows_result.get('items', [])
    if search:
        search_lower = search.lower()
        my_workflows = [w for w in my_workflows if search_lower in w.get('name', '').lower() or search_lower in w.get('description', '').lower()]

    # n8n Library tab
    n8n_workflows = N8nWorkflowLibraryService.list_workflows()
    if search:
        search_lower = search.lower()
        n8n_workflows = [w for w in n8n_workflows if search_lower in w.get('name', '').lower() or search_lower in (w.get('description') or '').lower()]
    if category_filter:
        n8n_workflows = [w for w in n8n_workflows if w.get('category') == category_filter]
    n8n_categories = N8nWorkflowLibraryService.get_categories(n8n_workflows)

    # n8n pagination
    n8n_per_page = 24
    try:
        n8n_page = max(1, int(request.GET.get('n8n_page', 1)))
    except (ValueError, TypeError):
        n8n_page = 1
    n8n_total = len(n8n_workflows)
    n8n_num_pages = max(1, (n8n_total + n8n_per_page - 1) // n8n_per_page)
    n8n_page = min(n8n_page, n8n_num_pages)
    n8n_offset = (n8n_page - 1) * n8n_per_page
    n8n_workflows_page = n8n_workflows[n8n_offset : n8n_offset + n8n_per_page]

    # Templates tab
    template_filters = {}
    if category_filter:
        template_filters['category'] = category_filter
    templates_result = template_storage.list(filters=template_filters, limit=None, offset=0)
    templates = templates_result.get('items', [])
    if search:
        search_lower = search.lower()
        templates = [t for t in templates if search_lower in t.get('name', '').lower() or search_lower in (t.get('description') or '').lower()]
    template_categories = list(set([t.get('category', 'other') for t in templates]))

    # Executions tab
    all_workflows_for_user = workflow_storage.list(filters={'created_by': user_uuid}, limit=None, offset=0).get('items', [])
    all_executions = []
    for wf in all_workflows_for_user:
        for exec_data in wf.get('executions', []):
            exec_data = dict(exec_data)
            exec_data['workflow'] = wf
            all_executions.append(exec_data)
    all_executions.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    # Stats
    all_my_workflows = workflow_storage.list(filters={'created_by': user_uuid}, limit=None, offset=0).get('items', [])
    total_executions = sum(len(w.get('executions', [])) for w in all_my_workflows)
    successful_executions = sum(len([e for e in w.get('executions', []) if e.get('status') == 'completed']) for w in all_my_workflows)

    context = {
        'tab': tab,
        'my_workflows': my_workflows,
        'n8n_workflows': n8n_workflows,
        'n8n_workflows_page': n8n_workflows_page,
        'n8n_categories': n8n_categories,
        'n8n_page': n8n_page,
        'n8n_num_pages': n8n_num_pages,
        'n8n_total': n8n_total,
        'n8n_per_page': n8n_per_page,
        'templates': templates,
        'template_categories': template_categories,
        'executions': all_executions[:50],
        'search': search,
        'status_filter': status_filter,
        'trigger_filter': trigger_filter,
        'category_filter': category_filter,
        'status_choices': WorkflowStatus.choices,
        'execution_status_choices': ExecutionStatus.choices,
        'search_or_status_or_trigger': bool(search or status_filter or trigger_filter),
        'search_or_category': bool(search or category_filter),
        'stats': {
            'total_workflows': len(all_my_workflows),
            'active_workflows': len([w for w in all_my_workflows if w.get('is_active')]),
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'n8n_total': len(n8n_workflows),
            'n8n_categories_count': len(n8n_categories),
            'templates_count': len(templates),
        },
    }
    return render(request, 'durgasflow/hub.html', context)


@require_super_admin
def dashboard(request):
    """Main durgasflow dashboard"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    template_storage = WorkflowTemplateStorageService()
    
    # Get user's workflows
    workflows_result = workflow_storage.list(
        filters={'created_by': user_uuid},
        limit=5,
        offset=0,
        order_by='created_at',
        reverse=True
    )
    workflows = workflows_result.get('items', [])
    
    # Get recent executions from all workflows
    recent_executions = []
    for workflow in workflows:
        executions = workflow.get('executions', [])
        for exec_data in executions[:2]:  # Get 2 most recent per workflow
            exec_data['workflow'] = workflow
            recent_executions.append(exec_data)
    
    # Sort by created_at descending and limit to 10
    recent_executions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    recent_executions = recent_executions[:10]
    
    # Statistics
    all_workflows_result = workflow_storage.list(
        filters={'created_by': user_uuid},
        limit=None,
        offset=0
    )
    all_workflows = all_workflows_result.get('items', [])
    
    total_executions = sum(len(w.get('executions', [])) for w in all_workflows)
    successful_executions = sum(
        len([e for e in w.get('executions', []) if e.get('status') == ExecutionStatus.COMPLETED])
        for w in all_workflows
    )
    failed_executions = sum(
        len([e for e in w.get('executions', []) if e.get('status') == ExecutionStatus.FAILED])
        for w in all_workflows
    )
    
    success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
    stats = {
        'total_workflows': len(all_workflows),
        'active_workflows': len([w for w in all_workflows if w.get('is_active')]),
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'success_rate': success_rate,
    }
    
    # Featured templates
    templates_result = template_storage.list(
        filters={'is_featured': True},
        limit=4,
        offset=0
    )
    templates = templates_result.get('items', [])

    # Featured n8n workflows (supported, high conversion confidence)
    featured_n8n = N8nWorkflowLibraryService.get_featured(limit=4)
    
    context = {
        'workflows': workflows,
        'recent_executions': recent_executions,
        'stats': stats,
        'templates': templates,
        'featured_n8n': featured_n8n,
    }
    return render(request, 'durgasflow/dashboard.html', context)


@require_super_admin
def workflow_list(request):
    """List all workflows"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    
    # Filtering
    status = request.GET.get('status', '')
    trigger = request.GET.get('trigger', '')
    search = request.GET.get('search', '')
    
    filters = {'created_by': user_uuid}
    if status:
        filters['status'] = status
    if trigger:
        filters['trigger_type'] = trigger
    
    # Get all workflows for filtering/searching
    workflows_result = workflow_storage.list(
        filters=filters,
        limit=None,
        offset=0
    )
    workflows = workflows_result.get('items', [])
    
    # Apply search filter
    if search:
        search_lower = search.lower()
        workflows = [
            w for w in workflows
            if search_lower in w.get('name', '').lower() or search_lower in w.get('description', '').lower()
        ]
    
    # Pagination
    paginator = Paginator(workflows, 12)
    page = request.GET.get('page', 1)
    workflows_page = paginator.get_page(page)
    
    context = {
        'workflows': workflows_page,
        'status_filter': status,
        'trigger_filter': trigger,
        'search': search,
        'status_choices': WorkflowStatus.choices,
    }
    return render(request, 'durgasflow/workflow_list.html', context)


@require_super_admin
def workflow_create(request):
    """Create a new workflow"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    if request.method == 'POST':
        name = request.POST.get('name', 'Untitled Workflow')
        description = request.POST.get('description', '')
        trigger_type = request.POST.get('trigger_type', 'manual')
        
        workflow = WorkflowService.create_workflow(
            name=name,
            description=description,
            trigger_type=trigger_type,
            user_uuid=user_uuid
        )
        
        messages.success(request, f'Workflow "{workflow.get("name")}" created successfully.')
        return redirect('durgasflow:editor', workflow_id=workflow.get('id'))
    
    return render(request, 'durgasflow/workflow_form.html', {
        'is_create': True,
    })


@require_super_admin
def workflow_detail(request, workflow_id):
    """View workflow details"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    # Get recent executions for this workflow
    executions = workflow.get('executions', [])[:10]
    
    context = {
        'workflow': workflow,
        'executions': executions,
    }
    return render(request, 'durgasflow/workflow_detail.html', context)


@require_super_admin
def workflow_edit(request, workflow_id):
    """Edit workflow settings"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    if request.method == 'POST':
        workflow_storage.update_workflow(
            workflow_id,
            name=request.POST.get('name', workflow.get('name')),
            description=request.POST.get('description', workflow.get('description')),
            trigger_type=request.POST.get('trigger_type', workflow.get('trigger_type'))
        )
        
        messages.success(request, f'Workflow "{request.POST.get("name", workflow.get("name"))}" updated successfully.')
        return redirect('durgasflow:workflow_detail', workflow_id=workflow_id)
    
    context = {
        'workflow': workflow,
        'is_create': False,
    }
    return render(request, 'durgasflow/workflow_form.html', context)


@require_super_admin
@require_POST
def workflow_delete(request, workflow_id):
    """Delete a workflow"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    name = workflow.get('name')
    workflow_storage.delete_workflow(workflow_id)
    
    messages.success(request, f'Workflow "{name}" deleted successfully.')
    return redirect('durgasflow:workflow_list')


@require_super_admin
def editor(request, workflow_id):
    """Visual workflow editor"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    # Get available node types for the palette
    from .services.node_registry import NodeRegistry
    node_types = NodeRegistry.get_all_node_types()
    
    context = {
        'workflow': workflow,
        'graph_data': json.dumps(workflow.get('graph_data', {})),
        'node_types': node_types,
    }
    return render(request, 'durgasflow/editor.html', context)


@require_super_admin
def editor_new(request):
    """Create and open a new workflow in the editor"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow = WorkflowService.create_workflow(
        name='Untitled Workflow',
        user_uuid=user_uuid
    )
    return redirect('durgasflow:editor', workflow_id=workflow.get('id'))


@require_super_admin
def execution_list(request):
    """List all executions"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    
    # Filtering
    status = request.GET.get('status', '')
    workflow_id = request.GET.get('workflow', '')
    
    # Get all workflows for this user
    workflows_result = workflow_storage.list(
        filters={'created_by': user_uuid},
        limit=None,
        offset=0
    )
    workflows = workflows_result.get('items', [])
    
    # Collect executions from all workflows
    all_executions = []
    for workflow in workflows:
        if workflow_id and workflow.get('id') != workflow_id:
            continue
        
        executions = workflow.get('executions', [])
        for exec_data in executions:
            exec_data['workflow'] = workflow
            if status and exec_data.get('status') != status:
                continue
            all_executions.append(exec_data)
    
    # Sort by created_at descending
    all_executions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Pagination
    paginator = Paginator(all_executions, 20)
    page = request.GET.get('page', 1)
    executions_page = paginator.get_page(page)
    
    context = {
        'executions': executions_page,
        'workflows': workflows,
        'status_filter': status,
        'workflow_filter': workflow_id,
        'status_choices': ExecutionStatus.choices,
    }
    return render(request, 'durgasflow/execution_list.html', context)


@require_super_admin
def execution_detail(request, execution_id):
    """View execution details and logs"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    
    # Find execution in workflows
    workflows_result = workflow_storage.list(
        filters={'created_by': user_uuid},
        limit=None,
        offset=0
    )
    
    execution = None
    workflow = None
    for wf in workflows_result.get('items', []):
        executions = wf.get('executions', [])
        for exec_data in executions:
            if exec_data.get('execution_id') == execution_id or exec_data.get('id') == execution_id:
                execution = exec_data
                workflow = wf
                break
        if execution:
            break
    
    if not execution:
        messages.error(request, 'Execution not found or unauthorized.')
        return redirect('durgasflow:execution_list')
    
    # Get logs from execution
    logs = execution.get('logs', [])
    
    context = {
        'execution': execution,
        'workflow': workflow,
        'logs': logs,
    }
    return render(request, 'durgasflow/execution_detail.html', context)


@require_super_admin
@require_POST
def workflow_execute(request, workflow_id):
    """Manually execute a workflow"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Workflow not found or unauthorized'}, status=404)
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    try:
        # Parse trigger data from request
        trigger_data = {}
        if request.content_type == 'application/json':
            trigger_data = json.loads(request.body) if request.body else {}
        
        execution = ExecutionEngine.execute_workflow(
            workflow=workflow,
            trigger_type='manual',
            trigger_data=trigger_data,
            user_uuid=user_uuid
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'execution_id': execution.get('execution_id') or execution.get('id'),
                'status': execution.get('status'),
            })
        
        messages.success(request, 'Workflow execution started.')
        execution_id = execution.get('execution_id') or execution.get('id')
        return redirect('durgasflow:execution_detail', execution_id=execution_id)
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e),
            }, status=500)
        
        messages.error(request, f'Failed to execute workflow: {str(e)}')
        return redirect('durgasflow:workflow_detail', workflow_id=workflow.get('id') or workflow_id)


@require_super_admin
@require_POST
def workflow_activate(request, workflow_id):
    """Activate a workflow"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    workflow_storage.update_workflow(workflow_id, is_active=True, status='active')
    messages.success(request, f'Workflow "{workflow.get("name")}" activated.')
    
    return redirect('durgasflow:workflow_detail', workflow_id=workflow_id)


@require_super_admin
@require_POST
def workflow_deactivate(request, workflow_id):
    """Deactivate a workflow"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow or workflow.get('created_by') != user_uuid:
        messages.error(request, 'Workflow not found or unauthorized.')
        return redirect('durgasflow:workflow_list')
    
    workflow_storage.update_workflow(workflow_id, is_active=False, status='paused')
    messages.success(request, f'Workflow "{workflow.get("name")}" deactivated.')
    
    return redirect('durgasflow:workflow_detail', workflow_id=workflow_id)


@require_super_admin
def credential_list(request):
    """List all credentials"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    credential_storage = CredentialStorageService()
    credentials_result = credential_storage.list(
        filters={'created_by': user_uuid},
        limit=None,
        offset=0
    )
    credentials = credentials_result.get('items', [])
    
    context = {
        'credentials': credentials,
    }
    return render(request, 'durgasflow/credential_list.html', context)


@require_super_admin
def credential_create(request):
    """Create a new credential"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    credential_storage = CredentialStorageService()
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        credential_type = request.POST.get('credential_type', 'api_key')
        service_name = request.POST.get('service_name', '')
        description = request.POST.get('description', '')
        
        # Build credential data based on type
        data = {}
        if credential_type == 'api_key':
            data['api_key'] = request.POST.get('api_key', '')
        elif credential_type == 'basic_auth':
            data['username'] = request.POST.get('username', '')
            data['password'] = request.POST.get('password', '')
        elif credential_type == 'bearer_token':
            data['token'] = request.POST.get('token', '')
        elif credential_type == 'oauth2':
            data['client_id'] = request.POST.get('client_id', '')
            data['client_secret'] = request.POST.get('client_secret', '')
            data['access_token'] = request.POST.get('access_token', '')
            data['refresh_token'] = request.POST.get('refresh_token', '')
        
        credential = credential_storage.create_credential(
            name=name,
            credential_type=credential_type,
            service_name=service_name,
            description=description,
            data=data,
            created_by=user_uuid
        )
        
        messages.success(request, f'Credential "{credential.get("name")}" created successfully.')
        return redirect('durgasflow:credential_list')
    
    return render(request, 'durgasflow/credential_form.html', {
        'is_create': True,
    })


@require_super_admin
def credential_detail(request, credential_id):
    """View/edit credential details"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    credential_storage = CredentialStorageService()
    credential = credential_storage.get_credential(credential_id)
    
    if not credential or credential.get('created_by') != user_uuid:
        messages.error(request, 'Credential not found or unauthorized.')
        return redirect('durgasflow:credential_list')
    
    if request.method == 'POST':
        updated = credential_storage.update_credential(
            credential_id,
            name=request.POST.get('name', credential.get('name')),
            description=request.POST.get('description', credential.get('description', '')),
            service_name=request.POST.get('service_name', credential.get('service_name'))
        )
        
        if updated:
            messages.success(request, f'Credential "{updated.get("name")}" updated successfully.')
        else:
            messages.error(request, 'Failed to update credential.')
        return redirect('durgasflow:credential_list')
    
    context = {
        'credential': credential,
        'is_create': False,
    }
    return render(request, 'durgasflow/credential_form.html', context)


@require_super_admin
@require_POST
def credential_delete(request, credential_id):
    """Delete a credential"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    credential_storage = CredentialStorageService()
    credential = credential_storage.get_credential(credential_id)
    
    if not credential or credential.get('created_by') != user_uuid:
        messages.error(request, 'Credential not found or unauthorized.')
        return redirect('durgasflow:credential_list')
    
    name = credential.get('name')
    credential_storage.delete_credential(credential_id)
    
    messages.success(request, f'Credential "{name}" deleted successfully.')
    return redirect('durgasflow:credential_list')


@require_super_admin
def template_list(request):
    """List available workflow templates"""
    from .services.workflow_template_storage_service import WorkflowTemplateStorageService
    
    category = request.GET.get('category', '')
    
    template_storage = WorkflowTemplateStorageService()
    filters = {}
    if category:
        filters['category'] = category
    
    templates_result = template_storage.list(filters=filters, limit=None, offset=0)
    templates = templates_result.get('items', [])
    
    # Get categories from first template or define default
    categories = ['automation', 'integration', 'data-processing', 'notification', 'other']
    if templates:
        # Extract unique categories from templates
        categories = list(set([t.get('category', 'other') for t in templates]))
    
    context = {
        'templates': templates,
        'category_filter': category,
        'categories': categories,
    }
    return render(request, 'durgasflow/template_list.html', context)


@require_super_admin
@require_POST
def template_use(request, template_id):
    """Create a workflow from a template"""
    # Get user UUID from token
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')
    
    template_storage = WorkflowTemplateStorageService()
    template = template_storage.get_template(template_id)
    
    if not template:
        messages.error(request, 'Template not found.')
        return redirect('durgasflow:template_list')

    # Create workflow from template
    workflow = WorkflowService.create_workflow(
        name=f"{template.get('name')} (Copy)",
        description=template.get('description', ''),
        graph_data=template.get('graph_data', {}),
        user_uuid=user_uuid
    )

    # Increment template usage
    use_count = template.get('use_count', 0) + 1
    template_storage.update_template(template_id, use_count=use_count)

    messages.success(request, f'Workflow created from template "{template.get("name")}".')
    return redirect('durgasflow:editor', workflow_id=workflow.get('id'))


def _do_import_n8n_single(workflow_path: str, user_uuid: str):
    """
    Import a single n8n workflow by path. Used by both single and bulk import.

    Args:
        workflow_path: Path relative to media/n8n/ (with or without .json).
        user_uuid: User UUID for workflow ownership.

    Returns:
        Tuple (success: bool, data: dict).
        On success: (True, {'workflow_id': uuid, 'name': str, 'workflow_path': str}).
        On failure: (False, {'workflow_path': str, 'error': str}).
    """
    from pathlib import Path
    from django.conf import settings

    base_dir = Path(settings.BASE_DIR).resolve()
    n8n_dir = (base_dir / 'media' / 'n8n').resolve()

    path_for_lookup = workflow_path.rstrip('/')
    if not path_for_lookup.endswith('.json'):
        path_for_lookup = f"{path_for_lookup}.json"

    workflow_file = (n8n_dir / path_for_lookup).resolve()
    if not str(workflow_file).startswith(str(n8n_dir)):
        return False, {'workflow_path': workflow_path, 'error': 'Invalid workflow path'}

    resolved = N8nWorkflowLibraryService.resolve_workflow_path(workflow_file)
    if resolved is not None:
        workflow_file = resolved
    elif not workflow_file.exists() or not workflow_file.is_file():
        return False, {'workflow_path': workflow_path, 'error': f'File not found: {workflow_path}'}

    n8n_data = N8nWorkflowLibraryService.load_workflow_file(workflow_file)
    if n8n_data is None:
        return False, {'workflow_path': workflow_path, 'error': 'Failed to parse workflow JSON'}

    try:
        workflow = WorkflowService.import_n8n_workflow(n8n_data, user_uuid)
        return True, {
            'workflow_path': workflow_path,
            'workflow_id': str(workflow.get('id')),
            'name': workflow.get('name', ''),
        }
    except Exception as e:
        logger.warning(f"Bulk import single failed for {workflow_path}: {e}")
        return False, {'workflow_path': workflow_path, 'error': str(e)}


@require_super_admin
@require_POST
def import_n8n_workflow(request, workflow_path):
    """
    Import an n8n workflow from the media directory.

    Args:
        workflow_path: Path to the n8n workflow file relative to media/n8n/
    """
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')

    success, data = _do_import_n8n_single(workflow_path, user_uuid)
    if success:
        messages.success(
            request,
            f'Successfully imported n8n workflow "{data.get("name")}". '
            f'Converted to durgasflow format.'
        )
        return redirect('durgasflow:editor', workflow_id=data.get('workflow_id'))
    else:
        messages.error(request, data.get('error', 'Import failed'))
        return redirect('durgasflow:workflow_hub')


@csrf_exempt
@require_super_admin
@require_http_methods(['POST'])
def import_n8n_bulk(request):
    """
    Bulk import n8n workflows. Expects JSON body:
    - workflow_ids: list of paths (relative to media/n8n, with or without .json)
    - scope: "all" to import entire library (up to limit), optional

    Returns JSON: { ok, results: [{ success, workflow_path, workflow_id?, name?, error? }], summary: { total, success, failed } }
    """
    # #region agent log
    try:
        import time as _t
        open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H3", "location": "durgasflow.views:import_n8n_bulk:entry", "message": "view reached", "data": {"path": getattr(request, "path", "")}, "timestamp": int(_t.time() * 1000)}) + "\n")
    except Exception:
        pass
    # #endregion
    user_uuid = None
    if hasattr(request, 'appointment360_user'):
        user_uuid = request.appointment360_user.get('uuid')

    try:
        body = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)

    workflow_ids = body.get('workflow_ids')
    scope = body.get('scope')
    limit = min(int(body.get('limit', 100)), 200)

    if scope == 'all':
        workflows = N8nWorkflowLibraryService.list_workflows()
        workflow_ids = [(w.get('n8n_path') or w.get('id', '')).replace('\\', '/') for w in workflows[:limit]]
    if not workflow_ids:
        return JsonResponse({'ok': False, 'error': 'Provide workflow_ids or scope: "all"'}, status=400)

    results = []
    try:
        for path in workflow_ids:
            success, data = _do_import_n8n_single(path, user_uuid)
            if success:
                results.append({'success': True, 'workflow_path': path, 'workflow_id': data.get('workflow_id'), 'name': data.get('name')})
            else:
                results.append({'success': False, 'workflow_path': path, 'error': data.get('error', 'Unknown error')})

        total = len(results)
        success_count = sum(1 for r in results if r.get('success'))
        # #region agent log
        try:
            import time as _t
            open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H3", "location": "durgasflow.views:import_n8n_bulk:return_json", "message": "returning 200 JSON", "data": {"total": total}, "timestamp": int(_t.time() * 1000)}) + "\n")
        except Exception:
            pass
        # #endregion
        return JsonResponse({
            'ok': True,
            'results': results,
            'summary': {'total': total, 'success': success_count, 'failed': total - success_count},
        })
    except Exception as e:
        logger.exception("import_n8n_bulk failed: %s", e)
        return JsonResponse({
            'ok': False,
            'error': str(e),
            'results': [],
            'summary': {'total': 0, 'success': 0, 'failed': 0},
        }, status=500)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def webhook_handler(request, workflow_id, webhook_path):
    """Handle incoming webhooks for workflow triggers"""
    workflow_storage = WorkflowStorageService()
    workflow = workflow_storage.get_workflow(workflow_id)
    
    if not workflow:
        return JsonResponse({'error': 'Workflow not found or inactive'}, status=404)
    
    # Check webhook path, active status, and trigger type
    if (workflow.get('webhook_path') != webhook_path or
        not workflow.get('is_active') or
        workflow.get('trigger_type') != 'webhook'):
        return JsonResponse({'error': 'Workflow not found or inactive'}, status=404)
    
    # Validate webhook secret if set
    webhook_secret = workflow.get('webhook_secret')
    if webhook_secret:
        provided_secret = request.headers.get('X-Webhook-Secret', '')
        if provided_secret != webhook_secret:
            return JsonResponse({'error': 'Invalid webhook secret'}, status=403)
    
    # Build trigger data from request
    trigger_data = {
        'method': request.method,
        'headers': dict(request.headers),
        'query_params': dict(request.GET),
    }
    
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                trigger_data['body'] = json.loads(request.body)
            else:
                trigger_data['body'] = dict(request.POST)
        except json.JSONDecodeError:
            trigger_data['body'] = request.body.decode('utf-8', errors='replace')
    
    # Execute the workflow
    try:
        execution = ExecutionEngine.execute_workflow(
            workflow=workflow,
            trigger_type='webhook',
            trigger_data=trigger_data,
            user_uuid=None  # Webhook executions don't have a user
        )
        
        return JsonResponse({
            'success': True,
            'execution_id': execution.get('execution_id') or execution.get('id'),
            'status': execution.get('status'),
        })
    except Exception as e:
        logger.error(f"Webhook execution failed: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=500)
