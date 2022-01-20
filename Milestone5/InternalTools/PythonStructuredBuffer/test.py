from StructuredBuffer import StructuredBuffer
import json
import requests

oSafeNestTObject = StructuredBuffer()
oSafeNestTObject.PutString("TNest", "Stock")

oSafeNestObject = StructuredBuffer()
oSafeNestObject.PutString("Nest", "Stock")
oSafeNestObject.PutFloat64("Float", 200)
oSafeNestObject.PutBoolean("Bool", True)
oSafeNestObject.PutStructuredBuffer("SafeNest", oSafeNestTObject)

oSafeObject = StructuredBuffer()
oSafeObject.PutString("Payload", "lol")
oSafeObject.PutStructuredBuffer("Nest", oSafeNestObject)

print(oSafeObject.ToString())
# print(oSafeObject.GetDescriptionOfElements())
print(oSafeObject.ToJson())

print (json.dumps(oSafeObject.ToJson()))

print ("Reversing the json to string")
oReverse = StructuredBuffer(strJson=json.dumps(oSafeObject.ToJson()))
print(oReverse.ToString())

print(len(oReverse.GetSerializedStructuredBuffer()))

oSb = StructuredBuffer(serializedBuffer=oReverse.GetSerializedStructuredBuffer())

jsonString = "{\"TopNest\":{\"BoolValue\":true,\"FloatValue\":200.0,\"StringValue\":\"Stock\",\"DoubleNest\":{\"DNest\":\"Stock\", \"DnextInt\":123}},\"Payload\":\"testload\"}"
print("Original Json String:\n", jsonString)

print("\nConverting JsonToStructuredBuffer...")
url = "http://127.0.0.1:5000/JsonToStructuredBuffer"
payload = jsonString
headers = {'Content-Type': 'application/json'}
response = requests.request("GET", url, headers=headers, data=payload)

oSb = StructuredBuffer(serializedBuffer=response.content)
print("StructuredBufferResponse:\n", oSb.ToString())

print("\nConverting StructuredBufferToJson...")
url = "http://127.0.0.1:5000/StructuredBufferToJson"
payload = response.content
headers = {'Content-Type': 'application/octet-stream'}
response = requests.request("GET", url, headers=headers, data=payload)
print("Json string is:\n", response.text)

