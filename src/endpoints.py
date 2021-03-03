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
import thiscovery_lib.eb_utilities as eb
import thiscovery_lib.utilities as utils
from http import HTTPStatus


@utils.lambda_wrapper
@utils.api_error_handler
def post_event(event, context):
    allowed_detail_types = [
        'task_consent_accepted',
        'task_consent_declined',
        'survey_started',
        'survey_user_agent',
        'survey_completed',
    ]
    event_dict = json.loads(event['body'])
    detail_type = event_dict.get('detail-type')
    if detail_type not in allowed_detail_types:
        raise utils.DetailedValueError(f'Unsupported event type: {detail_type}', details={})
    thiscovery_event = eb.ThiscoveryEvent(event_dict)
    eb_client = eb.EventbridgeClient()
    eb_client.put_event(
        thiscovery_event=thiscovery_event
    )
    return {"statusCode": HTTPStatus.OK, "body": ''}
