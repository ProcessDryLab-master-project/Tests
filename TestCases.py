from API import API
from Utils import Utils
import time
import json
import os


class TestCases() :
    testApi = API()
    utils = Utils()
    
# ------------------------ REPOSITORY TEST CASES --------------------------
    logMetadata = {
        'FileExtension': 'xes',
        'ResourceLabel': 'ML4_log',
        'ResourceType': 'EventLog',
        'Description': 'ML4 Test log'
    }
    streamMetadata = {
        'Host': 'mqtt.eclipseprojects.io',
        'StreamTopic': 'TestStream',
        'ResourceLabel': 'Test Stream',
        'ResourceType': 'EventStream',
        'Description': 'Stream for testing',
        'Overwrite': 'true'
    }

# Upload file resource
    def testFileUpload(self):
        file_rid = self.testApi.uploadResourceToRepo(self.logMetadata)
        success = self.utils.isValidGUID(file_rid)
        return success, file_rid
    
# Get metadata for the file resource we uploaded
    def testGetFileMDO(self, rid):
        file_mdo = self.testApi.getMetadataFromRepo(rid)
        # if(file_mdo == "No resource with that ID"):
        #     return False
        
        if(file_mdo["ResourceId"] != rid):
            return False
        
        mdo_ResourceInfo = file_mdo["ResourceInfo"]
        if(not mdo_ResourceInfo):
            return False
        if(mdo_ResourceInfo["ResourceLabel"] != self.logMetadata["ResourceLabel"]):
            return False
        if(mdo_ResourceInfo["ResourceType"] != self.logMetadata["ResourceType"]):
            return False
        if(mdo_ResourceInfo["FileExtension"] != self.logMetadata["FileExtension"]):
            return False
        if(mdo_ResourceInfo["Description"] != self.logMetadata["Description"]):
            return False
        if(mdo_ResourceInfo["Dynamic"] != False):
            return False
        
        # If all checks went through, return True.
        return True, file_mdo

# Get the resource we just uploaded
    def testGetFile(self, rid):
        filePath = "./Downloads/downloadedResource.xes"
        self.testApi.getResourceFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        os.remove(filePath)
        return True
    
# Get a histogram of the resource we uploaded
    def testGetHistogram(self, rid):
        filePath = "./Downloads/downloadedHistogram.json"
        self.testApi.getHistogramFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        os.remove(filePath)
        return True
    
# Get a resource relation graph for the resource we uploaded
    def testGetGraph(self, rid):
        filePath = "./Downloads/downloadedGraph.dot"
        self.testApi.getGraphFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        os.remove(filePath)
        return True

# Upload metadata for a stream
    def testUploadMetadata(self):
        mdo_rid = self.testApi.uploadMetadataToRepo(self.streamMetadata)
        success = self.utils.isValidGUID(mdo_rid)
        return success, mdo_rid
            
        # if(mdo_rid == "An EventStream for that StreamTopic and Host already exist. Use the Overwrite key if you wish to change it."):
        #     print("Post EventStream MDO test failed")

# Get the metadata object that we just uploaded info for
    def testGetStreamMDO(self, rid):
        stream_mdo = self.testApi.getMetadataFromRepo(rid)
        if(stream_mdo["ResourceId"] != rid):
            return False
        
        mdo_ResourceInfo = stream_mdo["ResourceInfo"]
        if(not mdo_ResourceInfo):
            return False
        if(mdo_ResourceInfo["ResourceLabel"] != self.streamMetadata["ResourceLabel"]):
            return False
        if(mdo_ResourceInfo["ResourceType"] != self.streamMetadata["ResourceType"]):
            return False
        if(mdo_ResourceInfo["Host"] != self.streamMetadata["Host"]):
            return False
        if(mdo_ResourceInfo["StreamTopic"] != self.streamMetadata["StreamTopic"]):
            return False
        if(mdo_ResourceInfo["Description"] != self.streamMetadata["Description"]):
            return False
        if(mdo_ResourceInfo["Dynamic"] != False):
            return False
        
        # If all checks went through, return True.
        return True


# Get filtered list of metadata objects without EventStream
    def testFilteredMetadataList(self):
        filters = [
            "EventLog",
            "Histogram"
        ]
        mdo_list = self.testApi.getFilteredMDOList(filters)
        if any (mdo["ResourceInfo"]["ResourceType"] == "EventStream" for mdo in mdo_list):
            return False
        if not any (mdo["ResourceInfo"]["ResourceType"] == "EventLog" for mdo in mdo_list):
            return False
        if not any (mdo["ResourceInfo"]["ResourceType"] == "Histogram" for mdo in mdo_list):
            return False
        
        return True
    
    
# ------------------------ MINER TEST CASES --------------------------
# Test miner config list
    def testGetMinerConfig(self):
        config_list = self.testApi.getMinerConfigList()
        if any (config["MinerId"] == "1" for config in config_list):
            return True
        
        return False


# Test file consuming miner start
    def testFileMinerStart(self, file_mdo):
        # file_mdo = self.testApi.getMetadataFromRepo(rid)
        body = {
            "MinerId": "1", # Take from config?
            "Input": {
                "Resources": {
                    "LogToRun": file_mdo # Take key from config?
                },
                "MinerParameters": {}
            },
            "Output": {
                "Host": "http://localhost:4001/resources/",
                "HostInit": "http://localhost:4001/resources/metadata/",
                "ResourceLabel": "Test Alpha PNML",
                "FileExtension": "pnml" # Take from config?
            }
        }
        pid = self.testApi.runMiner(body)
        success = not "Error" in pid
        return success, pid


# Test file miner status
    def testMinerStatusList(self, pid):
        status_list = self.testApi.getMinerStatusList()
        if any (status_obj["ProcessId"] == pid for status_obj in status_list):
            return True
        return False
        


# Test file miner status
    def testFileMinerStatus(self, pid):
        status_obj = self.testApi.getMinerStatus(pid)
        status = status_obj["ProcessStatus"]
        if(status == "complete" or status == "running"):
            return True
        
        return False



# Test file miner get result from repo
    def testFileMinerResult(self, pid):
        rid = None # get from requesting status in a loop
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            rid = status_obj["ResourceId"]

        filePath = "./Downloads/minerFileResult.xes"
        self.testApi.getResourceFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        os.remove(filePath)
        return True



# Test file miner stop (start and stop a file miner)
    def testFileMinerStop(self, mdo):
        success, pid = self.testFileMinerStart(mdo)
        if(not success):
            return False
        
        expResp = "Killed process with ID: " + pid
        response = self.testApi.stopMinerAlgorithm(pid)
        if(response != expResp):
            return False
        
        status_list = self.testApi.getMinerStatusList()
        if any (status_obj["ProcessId"] == pid for status_obj in status_list):
            return False
        
        return True



# Test publisher via file consuming miner
    def testPublisherStart(self):
        body = {
            "MinerId": "8",
            "Input":{
                "Resources":{},
                "MinerParameters": {}
            },
            "Output": {
                "Host": "mqtt.eclipseprojects.io",
                "HostInit": "http://localhost:4001/resources/metadata/",
                "ResourceLabel": "Test Alphabet Stream",
                "StreamTopic": "TestAlphabetStream",
                "Overwrite": False
            }
        }
        pid = self.testApi.runMiner(body)
        success = not "Error" in pid
        if("Error" in pid):
            return False
        
        status_obj = self.testApi.getMinerStatus(pid)
        rid = status_obj["ResourceId"]
        status = status_obj["ProcessStatus"]
        if(status == "crash" or status == "complete"):
            return False    # Publishing output should never be "complete"
        
        stream_mdo = self.testApi.getMetadataFromRepo(rid)
        return success, stream_mdo



# Test stream consuming miner start
    def testStreamMinerStart(self, stream_mdo):
        body = {
            "MinerId": "6",
            "Input":{
                "Resources":{
                    "InputStream": stream_mdo
                },
                "MinerParams": {}
            },
            "Output": {
                "Host": "http://localhost:4001/resources/",
                "HostInit": "http://localhost:4001/resources/metadata/",
                "ResourceLabel": "Alphabet Stream Histogram",
                "FileExtension": "json"
            }
        }
        pid = self.testApi.runMiner(body)
        success = not "Error" in pid
        return success, pid



# Test stream miner status
    def testStreamMinerStatus(self, pid):
        rid = None # get from requesting status in a loop
        status = None
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            status = status_obj["ProcessStatus"]
            if(status == "crash" or status == "complete"):
                return False    # Dynamic output should never be "complete"
            rid = status_obj["ResourceId"]

        return True



# Test stream miner get result from repo
    def testStreamMinerResult(self, pid):
        rid = None # get from requesting status in a loop
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            rid = status_obj["ResourceId"]

        # Download result first time
        filePath1 = "./Downloads/minerStreamResult1.xes"
        self.testApi.getResourceFromRepo(rid, filePath1)
        if(not os.path.isfile(filePath1)):
            return False
        file1 = open(filePath1)
        data1 = json.load(file1)

        time.sleep(5)   # Wait to guarantee that the repository has received updates
        # Download result second time
        filePath2 = "./Downloads/minerStreamResult2.xes"
        self.testApi.getResourceFromRepo(rid, filePath2)
        if(not os.path.isfile(filePath2)):
            return False
        file2 = open(filePath2)
        data2 = json.load(file2)
        
        if(data1 == data2): # The results should have received updates while we waited
            return False
        
        os.remove(filePath1)
        os.remove(filePath2)
        return True



# Test stream miner stop
    def testStreamMinerStop(self, pid):
        expResp = "Killed process with ID: " + pid
        response = self.testApi.stopMinerAlgorithm(pid)
        if(response != expResp):
            return False
        
        status_list = self.testApi.getMinerStatusList()
        if any (status_obj["ProcessId"] == pid for status_obj in status_list):
            return False
        
        fileStillUpdating = self.testStreamMinerResult()
        if (fileStillUpdating):
            return False
        
        return True



# Test get miner algorithm file
    def testGetAlgorithmFile(self, mid):
        config_list = self.testApi.getMinerAlgorithmFile()



# Test get miner algorithm requirements
    def testGetRequirementsFile(self, mid):
        config_list = self.testApi.getMinerRequirementsFile()



# Test run cloning action
    def testCloneStart(self):
        body = {
            "Host": "http://localhost:5000/shadow/",
            "Config": {
                "MinerId": "1",
                "MinerLabel": "Shadowed Alpha Miner",
                "Type": "Miner",
                "MinerPath": "Miners/MinerAlphaPy",
                "MinerFile": "MinerAlpha.py",
                "Access": "Public",
                "Shadow": True,
                "ResourceInput": [
                {
                    "Name": "LogToRun",
                    "FileExtension": "xes",
                    "ResourceType": "EventLog"
                }
                ],
                "ResourceOutput": {
                "FileExtension": "pnml",
                "ResourceType": "PetriNet"
                },
                "MinerParameters":[]
            }
        }
        pid = self.testApi.runMinerCloning(body)
        success = not "error" in pid
        return success, pid



# Test get cloning status
    def testCloneStatus(self, cid):
        status = self.testApi.getMinerCloningStatus(cid)
        if(status != "running"):
            print(status)
            return False



# Test run cloned miner algorithm
    def testClonedAlgorithm(self, cid, file_mdo):
        body = {
            "MinerId": cid,
            "Input": {
                "Resources": {
                    "LogToRun": file_mdo # Take key from config?
                },
                "MinerParameters": {}
            },
            "Output": {
                "Host": "http://localhost:4001/resources/",
                "HostInit": "http://localhost:4001/resources/metadata/",
                "ResourceLabel": "Test Cloned Alpha PNML",
                "FileExtension": "pnml" # Take from config?
            }
        }
        pid = self.testApi.runMiner(body)
        success = not "Error" in pid
        return success, pid