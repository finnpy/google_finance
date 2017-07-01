import json
import urllib
from collections import namedtuple

import requests

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
    return _get_all("/finance/info", {"client":"ig", "q":query_list}, shape=Price)


# ---------------------------------------------------------------

def _rename_fields(d):
    # print(d.keys())
    for k in d.keys():
        # print(k, "->", field_map[k])
        d[field_map[k]] = d.pop(k)
    return d


def _get(resource, params):
    query = "?" + urllib.urlencode(params)

    uri = "http://finance.google.com{}{}".format(resource, query)
    r = requests.get(uri)
    # print(r.status_code, len(r.content))
    return json.loads(r.content.replace("//", ""))


def _get_all(resource, params, shape):
    results = []
    f = open("raw.text", "w")
    js = _get(resource, params)
    f.write(json.dumps(js) + "\n")
    results.extend(map(lambda s: shape(**_rename_fields(s)), js))
    return results


if __name__ == "__main__":
    print(quotes("TSLA"))
    print(quotes(["TSLA"]))
    print(quotes(["AAPL","IBM","CSCO"]))
