import google_finance
import json
import os.path
import unittest

local = True


def inject_response(name):
    name = os.path.join(os.path.dirname(__file__), name)
    with open(name, "r") as f:
        payload = json.load(f)
    google_finance._get = lambda rsrc, params: payload


class TestAPI(unittest.TestCase):

    def test_quotes(self):
        if local:
            inject_response("quotes_aapl.json")
        r = google_finance.quotes("AAPL")
        if local:
            self.assertEqual(r[0].ticker, "AAPL")

    def test_quotes_from_list(self):
        if local:
            inject_response("quotes_aapl_ibm.json")
        r = google_finance.quotes(["AAPL", "IBM"])
        if local:
            self.assertEqual(r[0].ticker, "AAPL")
            self.assertEqual(r[1].ticker, "IBM")


if __name__ == "__main__":
    unittest.main(verbosity=2)
