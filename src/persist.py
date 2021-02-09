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
import thiscovery_lib.notification_send as notif_send
from thiscovery_lib.core_api_utilities import CoreApiClient
from thiscovery_lib.dynamodb_utilities import Dynamodb

import common.constants as const


@utils.lambda_wrapper
def persist_thiscovery_event(event, context):
    event_id = event['id']  # note that event id will be used as correlation id for subsequent processing
    ddb_client = Dynamodb(stack_name=const.STACK_NAME, correlation_id=event_id)
    detail_type = event['detail-type']
    event_time = event['time']
    event_detail = event['detail']
    ddb_client.put_item(
        table_name=const.AUDIT_TABLE,
        key=detail_type,
        item_type=event_detail.get('event_type', 'thiscovery_event'),
        item_details=event_detail,
        item=dict(),
        key_name='detail_type',
        sort_key={'event_time': event_time},
    )
    return {"statusCode": HTTPStatus.OK, "body": json.dumps('')}
