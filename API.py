import requests
import shutil
import json
import urllib.parse

# defining a params dict for the parameters to be sent to the API
# PARAMS = {'address':location}
# r = requests.get(url = repositoryResourceURL, params = PARAMS)

class API() :
  repositoryResourceURL = "http://localhost:4001/resources/"
  repositoryMetadataURL = "http://localhost:4001/resources/metadata/"
# ------------------------ POST RESOURCE --------------------------
  def uploadResourceToRepo(self):
    payload = {
      'FileExtension': 'xes',
      'ResourceLabel': 'ML4_log',
      'ResourceType': 'EventLog',
      'Description': 'ML4 Test log'
    }

    files=[
      ('file',('ML4_log.xes',open('./Resources/ML4_log.xes','rb'),'application/octet-stream'))
    ]

    response = requests.request("POST", url=self.repositoryResourceURL, data=payload, files=files)

    print("File Resource ID: " + response.text)
    return response.text
  
  # ------------------------ POST METADATA --------------------------
  def uploadMetadataToRepo(self):
    payload = {
      'Host': 'mqtt.eclipseprojects.io',
      'StreamTopic': 'TestStream',
      'ResourceLabel': 'Test Stream',
      'ResourceType': 'EventStream',
      'Description': 'Stream for testing',
      'Overwrite': 'false'
    }

    response = requests.request("POST", self.repositoryMetadataURL, data=payload)

    print("MDO Resource ID: " + response.text)
    return response.text

# ------------------------ GET RESOURCE --------------------------
  def getResourceFromRepo(self, rid):
    url = urllib.parse.urljoin(self.repositoryResourceURL, rid)
    response = requests.get(url=url, stream=True)

    with open('./Downloads/downloadedResource.xes', 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The file was saved successfully')

# ------------------------ GET HISTOGRAM --------------------------
  def getHistogramFromRepo(self, rid):
    url = urllib.parse.urljoin(self.repositoryResourceURL, rid)
    response = requests.get(url=url, stream=True)

    with open('./Downloads/downloadedHistogram.json', 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The file was saved successfully')
 


# ------------------------ GET METADATA OBJECT --------------------------
  def getMetadataFromRepo(self, rid):
    url = urllib.parse.urljoin(self.repositoryMetadataURL, rid)
    response = requests.get(url)

    # extracting data in json format
    mdo = json.loads(response.text)
    mdo_str = json.dumps(mdo, indent=2)
    print("Metadata object: " + str(mdo_str))
    return mdo



