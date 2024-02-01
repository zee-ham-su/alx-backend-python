#!/usr/bin/env python3
""" client testing module
"""

import unittest
from utils import get_json
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.GithubOrgClient.get_json', return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org method"""
        github_client = GithubOrgClient(org_name)
        result = github_client.org()

        self.assertEqual(result, [{"name": "repo1"}, {"name": "repo2"}])
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}/repos', True)
