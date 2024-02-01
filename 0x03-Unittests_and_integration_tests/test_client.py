#!/usr/bin/env python3
""" client testing module
"""

import unittest
from typing import Dict
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str,
                 expct_result: Dict, magic_mock: MagicMock) -> None:
        """Tests the `org` method."""

        magic_mock.return_value = MagicMock(return_value=expct_result)
        org_client = GithubOrgClient(org)

        result = org_client.org()

        magic_mock.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org))

        self.assertEqual(result, expct_result)

    @patch("client.GithubOrgClient.org")
    def test_public_repos_url(self, mock_org_method):
        known_payload = {
            'repos_url': 'https://api.github.com/users/google/repos'}
        mock_org_method.return_value = known_payload

        org_client = GithubOrgClient("google")

        result = org_client._public_repos_url()
        actual_result = result.get('repos_url', None)

        self.assertEqual(actual_result, known_payload['repos_url'])
