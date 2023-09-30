import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Comments(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_comments = "https://api.todoist.com/rest/v2/comments"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects().json()[1]["id"]
        cls.section_id = TodoBase().get_all_sections().json()[1]["id"]
        cls.task_id = TodoBase().get_all_tasks().json()[1]["id"]

    def test_get_all_comments_with_task_id(self):
        response = self.get_comments_on_task()
        LOGGER.info("Number of comments returned: %s", len(response.json()))
        assert response.status_code == 200

    def test_get_all_comments_with_project_id(self):
        project_id = self.project_id
        url_comments_by_project = f"{self.url_comments}?project_id={project_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS, url=url_comments_by_project)
        LOGGER.info("Number of comments returned: %s", len(response.json()))
        assert response.status_code == 200

    def test_create_comment_on_task(self):
        data = {
            "task_id": self.task_id,
            "content": "New comment from API"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)
        LOGGER.info("Comment Id: %s", response.json()["id"])
        assert response.status_code == 200

    def test_create_comment_on_project(self):
        data = {
            "project_id": self.project_id,
            "content": "New comment from API"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)
        LOGGER.info("Comment Id: %s", response.json()["id"])
        assert response.status_code == 200

    def test_get_comment_on_task(self):
        comment_id = self.get_comments_on_task().json()[0]["id"]
        LOGGER.info("Comment Id: %s", comment_id)
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_comment)
        assert response.status_code == 200

    def test_update_comment_on_task(self):
        data = {
            "content": "Comment updated from API"
        }
        comment_id = self.get_comments_on_task().json()[0]["id"]
        LOGGER.info("Comment Id: %s", comment_id)
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_comment, data=data)
        assert response.status_code == 200

    def test_delete_comment_on_task(self):
        comment_id = self.get_comments_on_task().json()[0]["id"]
        LOGGER.info("Comment Id: %s", comment_id)
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_comment)
        assert response.status_code == 204

    def get_comments_on_task(self):
        task_id = self.task_id
        url_comments_by_task = f"{self.url_comments}?task_id={task_id}"
        response_comments_by_tasks = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                                               url=url_comments_by_task)
        return response_comments_by_tasks
