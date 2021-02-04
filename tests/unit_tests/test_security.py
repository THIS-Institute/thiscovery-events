#
#   Thiscovery API - THIS Institute’s citizen science platform
#   Copyright (C) 2019 THIS Institute
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   A copy of the GNU Affero General Public License is available in the
#   docs folder of this project.  It is also available www.gnu.org/licenses/
#
import local.dev_config
import local.secrets
import json
import os
from http import HTTPStatus
from thiscovery_dev_tools.testing_tools import TestApiEndpoints, TestSecurityOfEndpointsDefinedInTemplateYaml

from tests.test_data import test_event, BASE_FOLDER


class TestEventsApiEndpoints(TestApiEndpoints):

    def test_post_event_requires_valid_key(self):
        body = json.dumps(test_event)
        self.check_api_is_restricted(
            request_verb='POST',
            aws_url='/v1/event',
            request_body=body,
        )


class TestTemplate(TestSecurityOfEndpointsDefinedInTemplateYaml):
    public_endpoints = list()

    @classmethod
    def setUpClass(cls):
        super().setUpClass(
            template_file_path=os.path.join(BASE_FOLDER, 'template.yaml'),
            api_resource_name='EventsApi',
        )

    def test_defined_endpoints_are_secure(self):
        self.check_defined_endpoints_are_secure()
