#!/usr/bin/env python3
""" client testing module
"""

import unittest
from typing import Dict
from unittest.mock import patch, MagicMock, PropertyMock, Mock
from requests import HTTPError
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD

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
                    "created_at": "2024-01-10T00:00:00Z",
                    "updated_at": "2024-02-10T00:00:00Z",
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
                    "created_at": "2024-01-10T00:00:00Z",
                    "updated_at": "2024-02-10T00:00:00Z",
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expct_result) -> None:
        """Tests the `has_license` method."""
        org_client = GithubOrgClient("google")
        result = org_client.has_license(repo, license_key)
        self.assertEqual(result, expct_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the `GithubOrgClient` class."""
    get_patcher = patch("requests.get")

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the class fixtures."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/users/google/repos': cls.repos_payload,
        }

        def get_payload(url: str) -> Dict:
            """Returns the payload for a given URL."""
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            response = Mock()
            response.status_code = 404
            response.json.return_value = {}
            return response
        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

        def test_public_repos(self) -> None:
            """Tests the `public_repos` method."""
            actual_result = GithubOrgClient("google").public_repos()
            expected_result = [
                'episodes.dart',
                'cpp-netlib', 'dagger', 'ios-webkit-debug-proxy',
                'google.github.io', 'kratu', 'build-debian-cloud',
                'traceur-compiler', 'firmata.py']
            print("Actual Result:", actual_result)
            print("Expected Result:", expected_result)
            self.assertEqual(actual_result, expected_result)

        def test_public_repos_with_license(self) -> None:
            """Tests the `public_repos` method with a license."""
            actual_result = GithubOrgClient(
                "google").public_repos(license="apache-2.0")
            expected_result = [
                'dagger',
                'kratu',
                'traceur-compiler',
                'firmata.py']
            print("Actual Result:", actual_result)
            print("Expected Result:", expected_result)
            self.assertEqual(actual_result, expected_result)

    @classmethod
    def tearDownClass(cls) -> None:
        """Tears down the class fixtures."""
        cls.get_patcher.stop()
