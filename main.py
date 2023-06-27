import json, unittest, datetime

# datetime is fo convert the timestamp from ISO string to epoch format (data 2)
# we need to split the data for correct location for data 1


with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):

    # IMPLEMENT: Conversion From Type 1
  result = {}
  location_parts = jsonObject.get('location').split('/')

  result = {
        "deviceID": jsonObject.get('deviceID'),
        "deviceType": jsonObject.get('deviceType'),
        "timestamp": jsonObject.get('timestamp'),
        "location": {  # the split is then inserted based on the index into the dictionary
            "country": location_parts[0],
            "city": location_parts[1],
            "area": location_parts[2],
            "factory": location_parts[3],
            "section": location_parts[4]
        },
        "data": { # here we are adding the operationStatus and temp fields to the dictionary
            "status": jsonObject.get('operationStatus'),
            "temperature": jsonObject.get('temp')
        }
    }

  return result

    


def convertFromFormat2 (jsonObject):

    #timestamp conversion
  timestamp = jsonObject.get('timestamp')
  timestamp = int(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)

  result = {
        "deviceID": jsonObject.get('device')['id'], #repopulating dictionary with combined deviceID
        "deviceType": jsonObject.get('device')['type'], #repopulating with combined devicetype
        "timestamp": timestamp,
        "location": {
            "country": jsonObject.get('country'),
            "city": jsonObject.get('city'),
            "area": jsonObject.get('area'),
            "factory": jsonObject.get('factory'),
            "section": jsonObject.get('section')
        },
        "data": jsonObject.get('data')
    }

  return result
    


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
