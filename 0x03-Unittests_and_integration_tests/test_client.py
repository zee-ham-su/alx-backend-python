#!/usr/bin/env python3
""" client testing module
"""

import unittest
from typing import Dict
from unittest.mock import patch, MagicMock, PropertyMock
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

    def test_public_repos_url(self) -> None:
        """Tests the `_public_repos_url` property."""
        with patch(
                "client.GithubOrgClient.org",
                new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            org_client = GithubOrgClient("google")

        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                return_value="https://api.github.com/users/google/repos",
        ) as mock_public_repos_url:
            self.assertEqual(
                org_client._public_repos_url,
                "https://api.github.com/users/google/repos",
            )
