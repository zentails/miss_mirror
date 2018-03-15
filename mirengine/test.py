import json
from pycricbuzz import Cricbuzz
def cric():
    c = Cricbuzz()
    matches = c.matches()
    for match in matches:
        print("Match:"+match['mchdesc'])
        print("Match Description:"+match['srs'])
        print("Match Type:"+match['type'])
        print("Match Status:"+match['status'])
        print("\n")
cric()