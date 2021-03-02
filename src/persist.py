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
import json
from http import HTTPStatus
import thiscovery_lib.utilities as utils
from thiscovery_lib.dynamodb_utilities import Dynamodb

import common.constants as const


@utils.lambda_wrapper
def persist_thiscovery_event(event, context):
    ddb_client = Dynamodb(stack_name=const.STACK_NAME, correlation_id=event['id'])
    table = ddb_client.get_table(table_name=const.AUDIT_TABLE)
    result = table.put_item(Item=event)
    assert result['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.OK
    return {"statusCode": HTTPStatus.OK, "body": json.dumps('')}
