import json
import sys

from collections import namedtuple
import requests
import dateutil.parser
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


field_map = {
    "id": "id",
    "s": "s",
    "t": "ticker",
    "e": "exchange",
    "l": "last_price",
    "l_fix": "l_fix",  # clarify
    "l_cur": "l_cur",  # clarify
    "lt": "last_trade_time_fmt",
    "ltt": "ltt",  # clarify
    "lt_dts": "last_trade_time",
    "c": "change",
    "c_fix": "c_fix",  # clarify
    "cp": "change_percent",
    "cp_fix": "cp_fix",  # clarify
    "ccol": "ccol",  # clarify
    "pcls_fix": "pcls_fix"  # clarify

    # "el": "last_price_after_hours",
    # "el_fix": "el_fix",  # clarify
    # "el_cur": "el_cur",  # clarify
    # "elt": "last_trade_time_after_hours",
    # "ec": "ec",  # clarify
    # "ec_fix": "ec_fix",  # clarify
    # "ecp": "ecp",  # clarify
    # "ecp_fix": "ecp_fix",  # clarify
    # "eccol": "eccol",  # clarify
    # "div": "dividend",
    # "yld": "dividend_yield"
}

Price = namedtuple("Price", field_map.values())


def quotes(symbols):
    if isinstance(symbols, str):
        symbols = [symbols]
    query_list = ",".join(symbols)
    return _get_all("/finance/info", {"client": "ig", "q": query_list}, _convert_price)


def _convert_price(js):
    d = _rename_fields(js)
    print(d)
    try:
        d['last_trade_time'] = dateutil.parser.parse(d['last_trade_time'])  # TODO: improve
    except ValueError as err:
        print("================", err, ":")
    return Price(**d)


def _rename_fields(d):
    # print("Before:", d.keys())
    # for k in field_map.keys():
    #     print(k, "->", field_map[k])
    for k in field_map.keys():
        d[field_map[k]] = d.pop(k)
    # print("After:", d.keys())
    return d


# ---------------------------------------------------------------


def _get(resource, params):
    query = "?" + urlencode(params)

    uri = "http://finance.google.com{}{}".format(resource, query)
    r = requests.get(uri)
    # print(r.status_code, len(r.content))
    print(r.content)
    return json.loads(r.content.replace(b"//", b""))


def _get_all(resource, params, convert_f):
    results = []
    f = open("raw.text", "w")
    js = _get(resource, params)
    f.write(json.dumps(js) + "\n")
    results.extend(map(convert_f, js))
    return results


if __name__ == "__main__":
    print(quotes("TSLA"))
    print(quotes(["TSLA"]))
    print(quotes(["AAPL", "IBM", "CSCO"]))
