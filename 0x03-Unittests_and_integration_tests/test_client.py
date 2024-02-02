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

            self.assertEqual(
                org_client._public_repos_url,
                "https://api.github.com/users/google/repos",
            )
        
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 1, 
                    "name": "Hamza", 
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1,
                    },
                "fork": False,
                "url": "https://api.github.com/repos/google/hamza",
                "html_url": "https://github.com/google/hamza",
                "created_at": "2008-01-10T00:00:00Z",
                "updated_at": "2020-01-10T00:00:00Z",
                "has_issues": True,
                "forks": 10,
                "default_branch": "master",
                },
                {
                    "id": 2,
                    "name": "abc",
                    "private": False,
                    "owner": {
                        "login": "abc",
                        "id": 2,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/abc",
                    "html_url": "https://github.com/google/abc",
                    "created_at": "2008-01-10T00:00:00Z",
                    "updated_at": "2020-01-10T00:00:00Z",
                    "has_issues": True,
                    "forks": 10,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
    ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            result = GithubOrgClient("google").public_repos()
            self.assertEqual(result, ["Hamza", "abc"])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()