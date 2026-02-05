"""
End-to-end tests for Dashboard functionality.

Tests complete user workflows:
- Dashboard navigation
- Tab switching
- Pagination
- Filtering
- Search
- Bulk operations
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

User = get_user_model()


class DashboardE2ETestCase(TestCase):
    """E2E tests for dashboard workflows."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_dashboard_loads(self):
        """Test that dashboard page loads successfully."""
        url = reverse('documentation:dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Media Manager Dashboard')
        self.assertContains(response, 'Pages')
        self.assertContains(response, 'Endpoints')
        self.assertContains(response, 'Relationships')
        self.assertContains(response, 'Postman')
    
    def test_tab_switching(self):
        """Test switching between tabs."""
        base_url = reverse('documentation:dashboard')
        
        # Test pages tab
        response = self.client.get(base_url, {'tab': 'pages'})
        self.assertEqual(response.status_code, 200)
        
        # Test endpoints tab
        response = self.client.get(base_url, {'tab': 'endpoints'})
        self.assertEqual(response.status_code, 200)
        
        # Test relationships tab
        response = self.client.get(base_url, {'tab': 'relationships'})
        self.assertEqual(response.status_code, 200)
        
        # Test postman tab
        response = self.client.get(base_url, {'tab': 'postman'})
        self.assertEqual(response.status_code, 200)
    
    def test_pagination_workflow(self):
        """Test pagination workflow (API v1)."""
        url = '/api/v1/dashboard/pages/'
        response = self.client.get(url, {'page': 1, 'page_size': 10})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data.get('success'))
        self.assertIn('meta', data)
        self.assertEqual(data['meta']['pagination']['page'], 1)
        response = self.client.get(url, {'page': 2, 'page_size': 10})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['meta']['pagination']['page'], 2)
    
    def test_filtering_workflow(self):
        """Test filtering workflow (API v1)."""
        url = '/api/v1/dashboard/endpoints/'
        response = self.client.get(url, {'method': 'QUERY'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data.get('success'))
    
    def test_search_workflow(self):
        """Test search (API v1)."""
        url = '/api/v1/dashboard/pages/'
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data.get('success'))
    
    def test_health_tab(self):
        """Test dashboard with tab=health."""
        base_url = reverse('documentation:dashboard')
        response = self.client.get(base_url, {'tab': 'health'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('health', response.content.decode())
        self.assertEqual(response.status_code, 400)
    
    def test_url_state_persistence(self):
        """Test that URL state is preserved."""
        base_url = reverse('documentation:dashboard')
        
        # Navigate with tab and pagination params
        response = self.client.get(base_url, {
            'tab': 'pages',
            'page': 2,
            'page_size': 20
        })
        
        self.assertEqual(response.status_code, 200)
        # Verify page context includes these params
        self.assertIn('active_tab', response.context)
    
    def test_authentication_required(self):
        """Test that authentication is required."""
        self.client.logout()
        
        # Dashboard page
        url = reverse('documentation:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # API endpoint (dashboard list now served by /api/v1/dashboard/*)
        url = '/api/v1/dashboard/pages/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login


class DashboardIntegrationTestCase(TestCase):
    """Integration tests for dashboard components working together."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_dashboard_api_integration(self):
        """Test that dashboard view and API work together."""
        # Get dashboard page
        dashboard_url = reverse('documentation:dashboard')
        response = self.client.get(dashboard_url, {'tab': 'pages'})
        self.assertEqual(response.status_code, 200)
        
        # Get API data (dashboard list from /api/v1/dashboard/*)
        api_url = '/api/v1/dashboard/pages/'
        api_response = self.client.get(api_url, {'page': 1, 'page_size': 20})
        self.assertEqual(api_response.status_code, 200)
        
        # Verify both return successfully
        self.assertIn('active_tab', response.context)
        api_data = json.loads(api_response.content)
        self.assertTrue(api_data.get('success'))
    
    def test_filter_and_pagination_integration(self):
        """Test that filters and pagination work together."""
        url = '/api/v1/dashboard/endpoints/'
        
        # Apply filter and pagination together
        response = self.client.get(url, {
            'method': 'QUERY',
            'page': 2,
            'page_size': 10
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data.get('success'))
        pagination = data.get('meta', {}).get('pagination', {})
        self.assertEqual(pagination.get('page'), 2)
