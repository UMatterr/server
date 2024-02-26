import json
import logging

from django.conf import settings
from django.http import (
    HttpResponseBadRequest, HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

import requests as req

from user.utils import auth_user, control_request_method
from event.utils import is_valid_event_type


logger = logging.getLogger(__name__)

@csrf_exempt
@auth_user
@control_request_method()
def get_phrase(request, event_type_id):

    use_cache = request.GET.get('useCache', 1)

    url = f"{settings.NLP_API_HOST}/phrase/{event_type_id}"
    params = {
        "use_cache": use_cache,
        "how": "asis"
    }

    if not is_valid_event_type(event_type_id):
        logger.error("Invalid event type id")
        return HttpResponseBadRequest('Invalid event type id')

    try:
        rsp = req.get(
            url,
            params=params,
            timeout=60
        )
        logger.info("data: %s", rsp.__dict__)

        data = rsp.json()
        logger.info("data: %s", data)

        return JsonResponse(
            data=data,
            status=200,
            safe=False,
        )

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return HttpResponseServerError('Error')


@csrf_exempt
@auth_user
@control_request_method(method=('POST'))
def post_converted_phrase(request):

    phrase = []
    how = "asis"
    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        phrase = body.get('phrase')
        how = body.get('how')

    except Exception as e:
        logger.error("Invalid body: %s, %s", e, body, exc_info=True)
        return HttpResponseBadRequest('Invalid body')

    if not phrase:
        logger.error("no phrase: %s", phrase)
        return HttpResponseBadRequest('no phrase')

    if how not in ('asis', 'formal', 'informal'):
        logger.error("Invalid how: %s", how)
        return HttpResponseBadRequest('Invalid how')

    url = f"{settings.NLP_API_HOST}/converted/{how}"
    payload = {
        "content": phrase,
    }
    try:
        rsp = req.post(
            url,
            json=payload,
            timeout=60
        )
        logger.info("rsp: %s", rsp.__dict__)

        if rsp.status_code != 200:
            logger.error("NLP server error")
            return HttpResponseServerError('NLP server error')

        data = rsp.json()
        logger.info("data: %s", data)

        return JsonResponse(
            data={"phrase": data["converted"]},
            status=200,
            safe=False,
        )

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return HttpResponseServerError('Error')


@csrf_exempt
@auth_user
@control_request_method(method=('PUT'))
def put_message(request):

    phrase = []
    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        msg = body.get('message')
        event_type_id = body.get('eventType')
        phrase.append(msg)
        logger.info("phrase: %s, %s", str(event_type_id), phrase)

    except Exception as e:
        logger.error("Invalid body: %s, %s", e, body, exc_info=True)
        return HttpResponseBadRequest('Invalid body')

    if not phrase:
        logger.error("no phrase: %s", phrase)
        return HttpResponseBadRequest('no phrase')

    url = f"{settings.NLP_API_HOST}/phrase/{event_type_id}"
    payload = {
        "content": phrase,
    }

    if not is_valid_event_type(event_type_id):
        logger.error("Invalid event type id")
        return HttpResponseBadRequest('Invalid event type id')

    try:
        rsp = req.post(
            url,
            json=payload,
            timeout=60
        )
        logger.info("data: %s", rsp.__dict__)

        data = rsp.json()
        logger.info("data: %s", data)

        return JsonResponse(
            data=data,
            status=204,
            safe=False,
        )

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return HttpResponseServerError('Error')

