from django.utils.encoding import force_bytes, force_text
import json


def dump_json(data):

    json_kwargs = {
        "sort_keys": True,
        "indent": 4,
    }

    import rest_framework

    version = rest_framework.__version__.split(".")

    if int(version[0]) <= 3 and int(version[1]) < 1:
        from rest_framework.compat import (SHORT_SEPARATORS, LONG_SEPARATORS,
                                           INDENT_SEPARATORS)
        from rest_framework.settings import api_settings

        compact = api_settings.COMPACT_JSON

        if json_kwargs["indent"] is None:
            separators = SHORT_SEPARATORS if compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS
    else:
        separators = (', ', ': ')

    json_kwargs["separators"] = separators

    return force_bytes(json.dumps(data, **json_kwargs))


def parse_json(data):
    return json.loads(force_text(data))
