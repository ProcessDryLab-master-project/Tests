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
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success
    
# Get a histogram of the resource we uploaded
    def testGetHistogram(self, rid):
        filePath = "./Downloads/downloadedHistogram.json"
        self.testApi.getHistogramFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success
    
# Get a resource relation graph for the resource we uploaded
    def testGetGraph(self, rid):
        filePath = "./Downloads/downloadedGraph.dot"
        self.testApi.getGraphFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success

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
        if(stream_mdo.get("ResourceId") != rid):
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
        if("Error" in pid):
            return False
        if(pid == "Invalid request. No miner with that ID. Config may be out of date, consider refreshing the frontend."):
            return False
        
        return True, pid
        


# Test file miner status - Can't test because it will remove it.
    # def testFileMinerStatus(self, pid):
    #     status_obj = self.testApi.getMinerStatus(pid)
    #     status = status_obj["ProcessStatus"]
    #     if(status == "running"): # Should not be complete or crash already
    #         return True
        
    #     return False


# Test miner status list
    def testMinerStatusList(self, pid):
        status_list = self.testApi.getMinerStatusList()
        if any (status_obj["ProcessId"] == pid for status_obj in status_list):
            return True
        return False



# Test file miner get result from repo
    def testFileMinerResult(self, pid):
        rid = None # get from requesting status in a loop
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            rid = status_obj.get("ResourceId")

        filePath = "./Downloads/minerFileResult.pnml"
        self.testApi.getResourceFromRepo(rid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success



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
                "Overwrite": True
            }
        }
        pid = self.testApi.runMiner(body)
        success = not "Error" in pid
        if("Error" in pid):
            return False
        
        status_obj = self.testApi.getMinerStatus(pid)
        
        rid = None # get from requesting status in a loop
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            rid = status_obj.get("ResourceId")
            status = status_obj["ProcessStatus"]
            if(status == "crash" or status == "complete"):
                return False    # Publishing output should never be "complete"

        # rid = status_obj.get("ResourceId")
        
        stream_mdo = self.testApi.getMetadataFromRepo(rid)
        print("Publisher's stream MDO:")
        print(stream_mdo)
        return success, stream_mdo, pid



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
            rid = status_obj.get("ResourceId")

        return True

# Helper function to avoid repeating code
    def isStreamResultUpdating(self, rid):
        # Download result first time
        filePath1 = "./Downloads/minerStreamResult1.json"
        self.testApi.getResourceFromRepo(rid, filePath1)
        if(not os.path.isfile(filePath1)):
            return False
        with open(filePath1) as file1:
            data1 = json.load(file1)

        time.sleep(5)   # Wait to guarantee that the repository has received updates
        # Download result second time
        filePath2 = "./Downloads/minerStreamResult2.json"
        self.testApi.getResourceFromRepo(rid, filePath2)
        if(not os.path.isfile(filePath2)):
            return False
        with open(filePath2) as file2:
            data2 = json.load(file2)
        
        
        filesEmpty = os.path.getsize(filePath1) <= 0 or os.path.getsize(filePath2) <= 0 # Check if file actually has contents
        
        os.remove(filePath1)
        os.remove(filePath2)
        if(filesEmpty or data1 == data2): # The results should have received updates while we waited
            return False
        return True
    
# Test stream miner get result from repo
    def testStreamMinerResult(self, pid):
        rid = None # get from requesting status in a loop
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            rid = status_obj.get("ResourceId")

        return self.isStreamResultUpdating(rid)



# Test stream miner stop
    def testStreamMinerStop(self, stream_pid, pub_pid):
        rid = None
        while(not rid):
            status_obj = self.testApi.getMinerStatus(stream_pid)
            rid = status_obj.get("ResourceId")

        expStreamResp = "Killed process with ID: " + stream_pid
        stream_response = self.testApi.stopMinerAlgorithm(stream_pid)
        if(stream_response != expStreamResp):
            print("Unexpected stream_response: " + stream_response)
            return False
        expPubResp = "Killed process with ID: " + pub_pid
        pub_response = self.testApi.stopMinerAlgorithm(pub_pid)
        if(pub_response != expPubResp):
            print("Unexpected pub_response: " + pub_response)
            return False
        
        status_list = self.testApi.getMinerStatusList()
        if any (status_obj["ProcessId"] == stream_pid for status_obj in status_list):
            print("Process id still exist after deleting it")
            return False
        
        if (self.isStreamResultUpdating(rid)):
            print("Stream is still updating")
            return False
        
        return True



# Test get miner algorithm file
    def testGetAlgorithmFile(self, mid):
        filePath = "./Downloads/minerAlgorithm.py"
        self.testApi.getMinerAlgorithmFile(mid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success



# Test get miner algorithm requirements
    def testGetRequirementsFile(self, mid):
        filePath = "./Downloads/minerRequirements.txt"
        self.testApi.getMinerRequirementsFile(mid, filePath)
        if(not os.path.isfile(filePath)):
            return False
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success



# Test run cloning action
    def testCloneStart(self):
        body =   {
            "Host": "http://localhost:5000/shadow/",
            "Config": {
                "MinerId": "8",
                "MinerLabel": "Alphabet Stream Publisher",
                "Type": "Miner",
                "MinerPath": "Miners/MqttPublisher",
                "MinerFile": "MqttPublisher.py",
                "Access": "Public",
                "Shadow": False,
                "ResourceInput": [],
                "ResourceOutput": {
                    "ResourceType": "EventStream"
                },
                "MinerParameters": []
            }
        }
        cid = self.testApi.runMinerCloning(body)
        print("cloning id: " + cid)
        success = not "error" in cid
        return success, cid



# Test get cloning status
    def testCloneStatus(self, cid):
        status = self.testApi.getMinerCloningStatus(cid)
        if(status != "running"):
            print("cloning status test: " + status)
            return False
        return True


# Test run cloned miner algorithm
    def testClonedAlgorithm(self, cid):
        status = "running"
        while(status != "complete"):
            status = self.testApi.getMinerCloningStatus(cid)
            if("Invalid request" in status):
                return False

        body = {
            "MinerId": cid,
            "Input": {
                "Resources": {},
                "MinerParameters": {}
            },
            "Output": {
                "Host": "mqtt.eclipseprojects.io",
                "HostInit": "http://localhost:4001/resources/metadata/",
                "ResourceLabel": "Test Cloned Stream",
                "StreamTopic": "TestClonedStream",
                "Overwrite": True
            }
        }
        pid = self.testApi.runMiner(body)
        if("Error" in pid):
            return False
        
        rid = None # get from requesting status in a loop
        while(not rid):
            status_obj = self.testApi.getMinerStatus(pid)
            rid = status_obj.get("ResourceId")

        
        expResp = "Killed process with ID: " + pid
        response = self.testApi.stopMinerAlgorithm(pid)
        if(response != expResp):
            return False
        
        file_mdo = self.testApi.getMetadataFromRepo(rid)
        if(not file_mdo):
            return False

        return True