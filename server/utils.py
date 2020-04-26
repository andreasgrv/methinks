from flask import Response

from methinks.utils import data_to_json


def response(status, msg=None, **kwargs):
    d = dict(status=status,
             message=msg or '',
             **kwargs)
    json_response = data_to_json(d)
    return Response(status=200,
                    response=json_response,
                    mimetype='application/json')
