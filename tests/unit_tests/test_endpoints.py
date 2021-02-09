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
import time

from http import HTTPStatus
from thiscovery_dev_tools import testing_tools as test_tools
from thiscovery_lib.dynamodb_utilities import Dynamodb
from thiscovery_lib.eb_utilities import EventbridgeClient

import src.common.constants as const
import src.endpoints as ep
from tests.test_data import test_event

class TestPostEvent(test_tools.BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ddb_client = Dynamodb(stack_name=const.STACK_NAME)
        cls.ddb_client.delete_all(
            table_name=const.AUDIT_TABLE,
            key_name=const.AUDIT_TABLE_HASH_KEY,
            sort_key_name=const.AUDIT_TABLE_SORT_KEY,
        )
        cls.eb_client = EventbridgeClient()

    def test_post_event_ok(self):
        result = test_tools.test_post(
            local_method=ep.post_event,
            aws_url='/v1/event',
            request_body=json.dumps(test_event),
        )
        self.assertEqual(HTTPStatus.OK, result['statusCode'])

        time.sleep(1)
        events = self.ddb_client.scan(
            table_name=const.AUDIT_TABLE
        )
        self.assertEqual(1, len(events))
        self.assertEqual('f2fac677-cb2c-42a0-9fa6-494059352569', events[0]['details']['user_id'])
