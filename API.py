import requests
import shutil
import json
import urllib.parse
from Utils import Utils

# defining a params dict for the parameters to be sent to the API
# PARAMS = {'address':location}
# r = requests.get(url = repositoryResourceURL, params = PARAMS)

class API() :

# ------------------------ SERVICE REGISTRY STUFF --------------------------
  srPingURL = "https://localhost:3000/ping/"
  srMinersURL = "https://localhost:3000/miners/"
  srRepositoriesURL = "https://localhost:3000/repositories/"
  srConnectionsURL = "https://localhost:3000/connections/filters/"
  srConfigsURL = "https://localhost:3000/config/filters/"
  # Ping
  def pingSr(self):
    response = requests.get(self.srPingURL)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Add miner
  def addminerSr(self, payload):
    response = requests.post(self.srMinersURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Get registered miner URLs
  def getMinersSr(self):
    response = requests.get(self.srMinersURL)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Delete miner
  def deleteMinerSr(self, payload):
    response = requests.delete(self.srMinersURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Add repository
  def addRepositorySr(self, payload):
    response = requests.post(self.srRepositoriesURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Get registered repository URLs
  def getRepositoriesSr(self):
    response = requests.get(self.srRepositoriesURL)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Delete repository
  def deleteRepositorySr(self, payload):
    response = requests.delete(self.srRepositoriesURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Get filtered connection URLs
  def getFilteredConnectionsSr(self, payload):
    response = requests.post(self.srConnectionsURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Get filtered configs
  def getFilteredConfigsSr(self, payload):
    response = requests.post(self.srConfigsURL, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr

# ------------------------ REPOSITORY STUFF --------------------------
  repositoryPingURL = "http://localhost:4001/ping"
  repositoryConfigURL = "http://localhost:4001/configurations"
  repositoryResourceURL = "http://localhost:4001/resources/"
  repositoryMetadataURL = "http://localhost:4001/resources/metadata/"
  repositoryGraphURL = "http://localhost:4001/resources/graphs/"
  repositoryHistogramURL = "http://localhost:4001/resources/histograms/"
  repositoryFilterURL = "http://localhost:4001/resources/metadata/filters"
  # Ping
  def pingRepo(self):
    response = requests.get(self.repositoryPingURL)
    responseStr = response.text.strip('\"')
    return responseStr
  
  
  # Config
  def getRepoConfig(self):
    response = requests.get(self.repositoryConfigURL)
    responseStr = response.text.strip('\"')
    return responseStr
  
  # POST resource
  def uploadResourceToRepo(self, filePath, payload):
    files=[
      ('file',('ML4_log.xes',open(filePath,'rb'),'application/octet-stream'))
    ]

    response = requests.post(url=self.repositoryResourceURL, data=payload, files=files)
    responseStr = response.text.strip('\"')
    print("File Resource ID: " + responseStr)
    return responseStr
  
  # POST Metadata
  def uploadMetadataToRepo(self, payload):
    response = requests.post(self.repositoryMetadataURL, data=payload)
    print("uploadMetadataToRepo: " + response.text)
    responseStr = response.text.strip('\"')
    print("MDO Resource ID: " + responseStr)
    return responseStr
  
  # PUT resource
  def updateResourceOnRepo(self, filePath, payload):
    files=[
      ('file',('ML4_log.xes',open(filePath,'rb'),'application/octet-stream'))
    ]

    response = requests.put(url=self.repositoryResourceURL, data=payload, files=files)
    responseStr = response.text.strip('\"')
    print("File Resource ID: " + responseStr)
    return responseStr
  
  # PUT Metadata
  def updateMetadataOnRepo(self, payload):
    response = requests.put(self.repositoryMetadataURL, data=payload)
    print("uploadMetadataToRepo: " + response.text)
    responseStr = response.text.strip('\"')
    print("MDO Resource ID: " + responseStr)
    return responseStr

# ------------------------ GET RESOURCE --------------------------
  def getResourceFromRepo(self, rid, path):
    url = urllib.parse.urljoin(self.repositoryResourceURL, rid)
    response = requests.get(url=url, stream=True)
    if(response.text == "No resource with that ID"):
      return False

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The file with rid ' + rid + ' was saved successfully')
    return True

# ------------------------ GET HISTOGRAM --------------------------
  def getHistogramFromRepo(self, rid, path):
    url = urllib.parse.urljoin(self.repositoryHistogramURL, rid)
    print("Requesting histogram from: " + url)
    response = requests.post(url=url, stream=True)
    if(response.text == "No resource with that ID"):
      return False

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The histogram for rid ' + rid + ' was saved successfully')
    return True

# ------------------------ GET RESOURCE GRAPH --------------------------
  def getGraphFromRepo(self, rid, path):
    url = urllib.parse.urljoin(self.repositoryGraphURL, rid)
    response = requests.get(url=url, stream=True)
    if(response.text == "No resource with that ID"):
      return False

    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)

    print('The graph for rid ' + rid + ' was saved successfully')
    return True
 


# ------------------------ GET METADATA OBJECT --------------------------
  def getMetadataFromRepo(self, rid):
    utils = Utils()
    if(not utils.isValidGUID(rid)):
      print("rid is not valid: " + rid)
      return False
    
    url = urllib.parse.urljoin(self.repositoryMetadataURL, rid)
    print("url: " + url)
    response = requests.get(url)
    if(response.text == "No resource with that ID"):
      return False
    mdo = json.loads(response.text)
    # mdo_str = json.dumps(mdo, indent=2)
    # print("Metadata object: " + str(mdo_str))
    return mdo
  
# ------------------------ GET FILTERED LIST OF METADATA OBJECTS --------------------------
  def getFilteredMDOList(self, filters):
    payload = json.dumps(filters)
    response = requests.post(self.repositoryFilterURL, data=payload)
    mdo_list = json.loads(response.text)
    # mdo_list_str = json.dumps(mdo_list, indent=2)
    # print("Metadata list: " + str(mdo_list_str))
    return mdo_list
  
# ------------------------ GET CHILDREN METADATA OBJECT LIST --------------------------
  def getChildrenMDOList(self, rid):
    url = urllib.parse.urljoin(self.repositoryGraphURL, rid)
    url = urllib.parse.urljoin(url, "children")
    response = requests.get(url)
    mdo_list = json.loads(response.text)
    # mdo_list_str = json.dumps(mdo_list, indent=2)
    # print("Metadata list: " + str(mdo_list_str))
    return mdo_list
  
# ------------------------ MINER STUFF --------------------------
  minerPingURL = "http://localhost:5000/ping/"
  minerConfigURL = "http://localhost:5000/configurations/"
  minerRunURL = "http://localhost:5000/miner/"
  minerStatusURL = "http://localhost:5000/status/"
  minerStopURL = "http://localhost:5000/stop/"
  minerShadowURL = "http://localhost:5000/shadow/"
  minerShadowRequirementsURL = "http://localhost:5000/shadow/requirements/"
  minerShadowStatusURL = "http://localhost:5000/shadow/status/"

  # Ping
  def pingMiner(self):
    response = requests.get(self.minerPingURL)
    responseStr = response.text.strip('\"')
    return responseStr

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
    # print("Run miner on " + self.minerRunURL + " with payload: ")
    # print(payload)

    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.post(self.minerRunURL, headers=headers, data=payload)

    # response = requests.post(self.minerRunURL, data=payload)
    responseStr = response.text.strip('\"')
    print("runMiner pid: " + responseStr)
    return responseStr # PID
  
# ------------------------ GET SPECIFIC MINER ALGORITHM STATUS --------------------------
  def getMinerStatus(self, pid):
    url = urllib.parse.urljoin(self.minerStatusURL, pid)
    response = requests.get(url)
    status_obj = json.loads(response.text)
    return status_obj

  
# ------------------------ GET LIST OF MINER ALGORITHM STATUS --------------------------
  def getMinerStatusList(self):
    response = requests.get(self.minerStatusURL)
    status_list = json.loads(response.text)
    return status_list
  
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
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.post(self.minerShadowURL, headers=headers, data=payload)
    responseStr = response.text.strip('\"')
    return responseStr # PID

# ------------------------ GET CLONING STATUS --------------------------
  def getMinerCloningStatus(self, cid):
    url = urllib.parse.urljoin(self.minerShadowStatusURL, cid)
    response = requests.get(url)
    # response = requests.get(url)
    # status_obj = json.loads(response.text)
    status = response.text
    return status


