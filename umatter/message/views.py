import logging
import traceback as tb

from django.http import (
    HttpResponseBadRequest, HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

from core.utils import get_env
from user.utils import auth_user, control_request_method
from .models import Phrase

import requests as req
import json


logger = logging.getLogger(__name__)
NLP_API_URL = get_env('NLP_API_URL', "")

@csrf_exempt
@auth_user
@control_request_method()
def get_phrase(request, event_id):

    use_cache = request.GET.get('useCache', 1)

    url = f"{NLP_API_URL}/phrase/{event_id}"
    params = {
        "use_cache": use_cache,
        "how": "asis"
    }
    data = req.get(
        url,
        params=params,
        timeout=60
    )
    data = data.json()

    logger.info("data: %s", data)

    return JsonResponse(
        data=data,
        status=200,
        safe=False,
    )


@csrf_exempt
@auth_user
@control_request_method(method=('POST'))
def post_phrase_converting(request):

    phrase = []
    how = "asis"
    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        phrase = body.get('phrase')
        how = body.get('how')

    except Exception as e:
        logger.error("Invalid body: %s, %s", e, body)
        return HttpResponseBadRequest('Invalid body')

    if not phrase:
        logger.error("no phrase: %s", phrase)
        return HttpResponseBadRequest('no phrase')

    if how not in ('asis', 'formal', 'informal'):
        logger.error("Invalid how: %s", how)
        return HttpResponseBadRequest('Invalid how')

    url = f"{NLP_API_URL}/converted/{how}"
    payload = {
        "content": phrase,
    }
    data = req.post(
        url,
        data=payload,
        timeout=60
    )
    logger.info("data: %s", data.__dict__)

    if data.status_code >= 500:
        logger.error("NLP server error")
        return HttpResponseServerError('NLP server error')

    data = data.json()

    return JsonResponse(
        data={"phrase": data["converted"]},
        status=200,
        safe=False,
    )
