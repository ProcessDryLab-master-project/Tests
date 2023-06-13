import requests
import shutil
import json
import urllib.parse
from Utils import Utils

# defining a params dict for the parameters to be sent to the API
# PARAMS = {'address':location}
# r = requests.get(url = repositoryResourceURL, params = PARAMS)

class API() :
# ------------------------ REPOSITORY STUFF --------------------------
  repositoryResourceURL = "http://localhost:4001/resources/"
  repositoryMetadataURL = "http://localhost:4001/resources/metadata/"
  repositoryGraphURL = "http://localhost:4001/resources/graphs/"
  repositoryHistogramURL = "http://localhost:4001/resources/histograms/"
  repositoryFilterURL = "http://localhost:4001/resources/metadata/filters"
# ------------------------ POST RESOURCE --------------------------
  def uploadResourceToRepo(self, payload):
    files=[
      ('file',('ML4_log.xes',open('./Resources/ML4_log.xes','rb'),'application/octet-stream'))
    ]

    response = requests.request("POST", url=self.repositoryResourceURL, data=payload, files=files)
    responseStr = response.text.strip('\"')
    print("File Resource ID: " + responseStr)
    return responseStr
  
  # ------------------------ POST METADATA --------------------------
  def uploadMetadataToRepo(self, payload):
    response = requests.request("POST", self.repositoryMetadataURL, data=payload)
    print("uploadMetadataToRepo: " + response.text)
    responseStr = response.text.strip('\"')
    print("MDO Resource ID: " + responseStr)
    return responseStr

# ------------------------ GET RESOURCE --------------------------
  def getResourceFromRepo(self, rid, path):
    url = urllib.parse.urljoin(self.repositoryResourceURL, rid)
    response = requests.get(url=url, stream=True)

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The log was saved successfully')

# ------------------------ GET HISTOGRAM --------------------------
  def getHistogramFromRepo(self, rid, path):
    url = urllib.parse.urljoin(self.repositoryHistogramURL, rid)
    response = requests.get(url=url, stream=True)

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The histogram was saved successfully')

# ------------------------ GET RESOURCE GRAPH --------------------------
  def getGraphFromRepo(self, rid, path):
    url = urllib.parse.urljoin(self.repositoryGraphURL, rid)
    response = requests.get(url=url, stream=True)

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The graph was saved successfully')
 


# ------------------------ GET METADATA OBJECT --------------------------
  def getMetadataFromRepo(self, rid):
    utils = Utils()
    if(not utils.isValidGUID(rid)):
      print("rid is not valid: " + rid)
      return False
    
    url = urllib.parse.urljoin(self.repositoryMetadataURL, rid)
    print("url: " + url)
    response = requests.get(url)
    mdo = json.loads(response.text)
    # mdo_str = json.dumps(mdo, indent=2)
    # print("Metadata object: " + str(mdo_str))
    return mdo
  
# ------------------------ GET FILTERED LIST OF METADATA OBJECTS --------------------------
  def getFilteredMDOList(self, filters):
    payload = json.dumps(filters)
    response = requests.request("POST", self.repositoryFilterURL, data=payload)
    mdo_list = json.loads(response.text)
    # mdo_list_str = json.dumps(mdo_list, indent=2)
    # print("Metadata list: " + str(mdo_list_str))
    return mdo_list
  
# ------------------------ GET CHILDREN METADATA OBJECT LIST --------------------------
  def getChildrenMDOList(self, rid):
    url = urllib.parse.urljoin(self.repositoryGraphURL, rid)
    url = urllib.parse.urljoin(url, "children")
    response = requests.request("GET", url)
    mdo_list = json.loads(response.text)
    # mdo_list_str = json.dumps(mdo_list, indent=2)
    # print("Metadata list: " + str(mdo_list_str))
    return mdo_list
  
# ------------------------ MINER STUFF --------------------------
  minerConfigURL = "http://localhost:5000/configurations/"
  minerRunURL = "http://localhost:5000/miner/"
  minerStatusURL = "http://localhost:5000/status/"
  minerStopURL = "http://localhost:5000/stop/"
  minerShadowURL = "http://localhost:5000/shadow/"
  minerShadowRequirementsURL = "http://localhost:5000/shadow/requirements/"
  minerShadowStatusURL = "http://localhost:5000/shaodw/status"
# ------------------------ GET MINER CONFIG --------------------------
  def getMinerConfigList(self):
    # url = urllib.parse.urljoin(self.minerConfig)
    response = requests.get(self.minerConfigURL)
    config_list = json.loads(response.text)
    return config_list
  
# ------------------------ RUN MINER ALGORITHM --------------------------
# ------------------------ RUN FILE CONSUMING MINER --------------------------
# ------------------------ RUN STREAM CONSUMING MINER --------------------------
  def runMiner(self, body):
    payload = json.dumps(body)
    print("Run miner with payload: ")
    print(payload)
    response = requests.post(self.minerRunURL, data=payload)
    responseStr = response.text.strip('\"')
    print("runMiner pid: " + responseStr)
    return responseStr # PID

  
# ------------------------ GET LIST OF MINER ALGORITHM STATUS --------------------------
  def getMinerStatusList(self):
    response = requests.get(self.minerStatusURL)
    status_list = json.loads(response.text)
    return status_list
  
# ------------------------ GET SPECIFIC MINER ALGORITHM STATUS --------------------------
  def getMinerStatus(self, pid):
    url = urllib.parse.urljoin(self.minerStatusURL, pid)
    print("Status URL: " + url)
    response = requests.get(url)
    print("Status response: " + response)
    status_obj = json.loads(response.text)
    return status_obj
  
# ------------------------ STOP MINER ALGORITHM --------------------------
  def stopMinerAlgorithm(self, pid):
    url = urllib.parse.urljoin(self.minerStopURL, pid)
    response = requests.delete(url)
    responseStr = response.text.strip('\"')
    return responseStr

# ------------------------ GET ALGORITHM FILE --------------------------
  def getMinerAlgorithmFile(self, mid, path):
    url = urllib.parse.urljoin(self.minerShadowURL, mid)
    response = requests.get(url=url, stream=True)

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The algorithm file was saved successfully')

# ------------------------ GET REQUIREMENTS FILE --------------------------
  def getMinerRequirementsFile(self, mid, path):
    url = urllib.parse.urljoin(self.minerShadowRequirementsURL, mid)
    response = requests.get(url=url, stream=True)

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The requirements file was saved successfully')

# ------------------------ RUN CLONING ACTION --------------------------
  def runMinerCloning(self, body):
    payload = json.dumps(body)
    response = requests.post(self.minerShadowURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr # PID

# ------------------------ GET CLONING STATUS --------------------------
  def getMinerCloningStatus(self, pid):
    url = urllib.parse.urljoin(self.minerShadowStatusURL, pid)
    response = requests.get(url)
    # status_obj = json.loads(response.text)
    status = response.text
    return status


