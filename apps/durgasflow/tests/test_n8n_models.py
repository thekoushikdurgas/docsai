"""
Tests for n8n_models: parse_workflow and parse_index.

Validates that workflow and index JSON from media/n8n and media/n8n/index.json
are correctly validated and normalized.
"""

from django.test import TestCase

from apps.durgasflow.services.n8n_models import parse_workflow, parse_index


class ParseWorkflowTestCase(TestCase):
    """Test parse_workflow validates and normalizes workflow dicts."""

    def test_returns_none_for_non_dict(self):
        self.assertIsNone(parse_workflow(None))
        self.assertIsNone(parse_workflow([]))
        self.assertIsNone(parse_workflow(""))

    def test_returns_none_when_nodes_missing(self):
        self.assertIsNone(parse_workflow({}))
        self.assertIsNone(parse_workflow({"connections": {}}))

    def test_returns_none_when_nodes_not_list(self):
        self.assertIsNone(parse_workflow({"nodes": "x"}))
        self.assertIsNone(parse_workflow({"nodes": None}))

    def test_returns_normalized_dict_when_valid(self):
        raw = {"nodes": [{"id": "a", "name": "N1", "type": "n8n-nodes-base.manualTrigger"}]}
        out = parse_workflow(raw)
        self.assertIsNotNone(out)
        self.assertIn("nodes", out)
        self.assertIn("connections", out)
        self.assertEqual(len(out["nodes"]), 1)
        self.assertEqual(out["connections"], {})

    def test_adds_connections_if_missing(self):
        raw = {"nodes": []}
        out = parse_workflow(raw)
        self.assertIsNotNone(out)
        self.assertEqual(out["connections"], {})

    def test_preserves_existing_connections(self):
        raw = {"nodes": [], "connections": {"A": {"main": [[{"node": "B", "type": "main", "index": 0}]]}}}
        out = parse_workflow(raw)
        self.assertIsNotNone(out)
        self.assertIn("A", out["connections"])
        self.assertEqual(out["connections"]["A"]["main"][0][0]["node"], "B")


class ParseIndexTestCase(TestCase):
    """Test parse_index validates index.json-like dicts."""

    def test_returns_none_for_non_dict(self):
        self.assertIsNone(parse_index(None))
        self.assertIsNone(parse_index([]))

    def test_returns_none_when_workflows_missing_or_empty(self):
        self.assertIsNone(parse_index({}))
        self.assertIsNone(parse_index({"workflows": []}))
        self.assertIsNone(parse_index({"workflows": None}))

    def test_returns_none_when_workflows_not_list(self):
        self.assertIsNone(parse_index({"workflows": {}}))

    def test_returns_dict_when_valid(self):
        raw = {"version": "2.0", "total": 1, "workflows": [{"id": "w1", "n8n_path": "w1.json"}]}
        out = parse_index(raw)
        self.assertIsNotNone(out)
        self.assertEqual(out["version"], "2.0")
        self.assertEqual(len(out["workflows"]), 1)
        self.assertEqual(out["workflows"][0]["n8n_path"], "w1.json")
