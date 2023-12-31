from API import API
from Utils import Utils
import time
import json
import os


class TestCases() :
    testApi = API()
    utils = Utils()

    # logMetadata = dict()
    # streamMetadata = dict()
    # def __init__(self, logMetadata, streamMetadata):  
    #     self.logMetadata = logMetadata  
    #     self.streamMetadata = streamMetadata

# ------------------------ SERVICE REGISTRY TEST CASES --------------------------
# Ping service registry
    def testSRPing(self):
        response = self.testApi.pingSr()
        print("testSrPing response: " + str(response))
        if(response == "pong"):
            return True
        return False

# Add miner to service registry
    def testSRAddMiners(self):
        testUrl = "miner" # Not an actual URL, just a test
        expResp = "Node " + testUrl + " added"
        payload = {
            "Host": testUrl
        }
        response = self.testApi.addminerSr(payload)
        print("testSRAddMiners response: " + str(response))
        if(expResp in response):
            return True
        return False

# Get miner URLs from service registry
    def testSRGetMiners(self):
        expResp = "miner"
        response = self.testApi.getMinersSr()
        print("testSRGetMiner response: " + str(response))
        if(expResp in response):
            return True
        return False

# Delete miner from service registry
    def testSRDeleteMiner(self):
        testUrl = "miner" # Not an actual URL, just a test
        expResp = "Node " + testUrl + " successfully removed"
        payload = {
            "Host": testUrl
        }
        response = self.testApi.deleteMinerSr(payload)
        print("testSRDeleteMiner response: " + str(response))
        if(response == expResp):
            return True
        return False

# Add repository to service registry
    def testSRAddRepository(self):
        testUrl = "repository" # Not an actual URL, just a test
        expResp = "Node " + testUrl + " added"
        payload = {
            "Host": testUrl
        }
        response = self.testApi.addRepositorySr(payload)
        print("testSRAddRepository response: " + str(response))
        if(expResp in response):
            return True
        return False
    

# Get repository URLS from service registry
    def testSRGetRepositories(self):
        expResp = "repository"
        response = self.testApi.getRepositoriesSr()
        print("testSRGetRepositories response: " + str(response))
        if(expResp in response):
            return True
        return False

# Delete repository from service registry
    def testSRDeleteRepository(self):
        testUrl = "repository" # Not an actual URL, just a test
        expResp = "Node " + testUrl + " successfully removed"
        payload = {
            "Host": testUrl
        }
        response = self.testApi.deleteRepositorySr(payload)
        print("testSRDeleteRepository response: " + str(response))
        if(response == expResp):
            return True
        return False

# Get filtered connection URLS from service registry
    def testSRFilteredConnections(self):
        minerUrl = "http://localhost:5000"
        repositoryUrl = "http://localhost:4001"
        payload = [
            minerUrl,
            repositoryUrl
        ]
        response = self.testApi.getFilteredConnectionsSr(payload)
        print("testSRFilteredConnections response: " + str(response))
        if not any (status_obj["host"] == minerUrl for status_obj in response):
            return False
        if not any (status_obj["host"] == repositoryUrl for status_obj in response):
            return False
        return True

# Get filtered configs from service registry
    def testSRFilteredConfigs(self):
        minerUrl = "http://localhost:5000"
        repositoryUrl = "http://localhost:4001"
        payload = [
            minerUrl,
            repositoryUrl
        ]
        response = self.testApi.getFilteredConfigsSr(payload)
        # print("testSRFilteredConfigs response: " + str(response))
        if not any (status_obj["host"] == minerUrl for status_obj in response):
            return False
        if not any (status_obj["host"] == repositoryUrl for status_obj in response):
            return False
        return True

# ------------------------ REPOSITORY TEST CASES --------------------------
    # logMetadata = {
    #     'FileExtension': 'xes',
    #     'ResourceLabel': 'ML4_log',
    #     'ResourceType': 'EventLog',
    #     'Description': 'ML4 Test log'
    # }
    # streamMetadata = {
    #     'Host': 'mqtt.eclipseprojects.io',
    #     'StreamTopic': 'TestStream',
    #     'ResourceLabel': 'Test Stream',
    #     'ResourceType': 'EventStream',
    #     'Description': 'Stream for testing',
    #     'Overwrite': 'true'
    # }

# Repository ping
    def testRepoPing(self):
        response = self.testApi.pingRepo()
        if(response == "pong"):
            return True
        return False

# Repository config
    def testRepoConfig(self):
        response = self.testApi.getRepoConfig()
        if(response.get("Type") == "Repository"):
            return True
        return False

# Upload file resource
    def testFileUpload(self, filePath, logMetadata):
        print("Sending file at path: " + filePath)
        file_rid = self.testApi.uploadResourceToRepo(filePath, logMetadata)
        print("fileUpload rid: " + str(file_rid))
        success = self.utils.isValidGUID(file_rid)
        return success, file_rid

# Update file resource
    def testFileUpdate(self, rid, filePath):
        print("Updating file at path: " + filePath)
        file_rid = self.testApi.updateResourceOnRepo(rid, filePath)
        if not self.utils.isValidGUID(file_rid):
            return False
        return self.testGetFile(file_rid)
    
# Get metadata for the file resource we uploaded
    def testGetFileMDO(self, rid, logMetadata):
        file_mdo = self.testApi.getMetadataFromRepo(rid)
        # print("file_mdo: " + str(file_mdo))
        if not file_mdo:
            return False, {}
        if(file_mdo == "No resource with that ID" or file_mdo == "Invalid FormData keys"):
            return False, {}
        
        if(file_mdo.get("ResourceId") != rid):
            return False, {}
        
        mdo_ResourceInfo = file_mdo["ResourceInfo"]
        if(not mdo_ResourceInfo):
            return False
        if(mdo_ResourceInfo.get("ResourceLabel") != logMetadata.get("ResourceLabel")):
            return False
        if(mdo_ResourceInfo.get("ResourceType") != logMetadata.get("ResourceType")):
            return False
        if(mdo_ResourceInfo.get("FileExtension") != logMetadata.get("FileExtension")):
            return False
        if(mdo_ResourceInfo.get("Description") != logMetadata.get("Description")):
            return False
        if(mdo_ResourceInfo.get("Dynamic") != False):
            return False
        
        # If all checks went through, return True.
        return True, file_mdo

# Get the resource we just uploaded
    def testGetFile(self, rid):
        filePath = "./Downloads/downloadedResource.xes"
        fileSaved = self.testApi.getResourceFromRepo(rid, filePath)
        if not fileSaved:
            print("No resource with that ID")
            return False
        if(not os.path.isfile(filePath)):
            print("No file saved")
            return False
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        print("testGetFile success: " + str(success))
        os.remove(filePath)
        return success
    
# Get a histogram of the resource we uploaded
    def testGetHistogram(self, rid):
        filePath = "./Downloads/downloadedHistogram.json"
        fileSaved = self.testApi.getHistogramFromRepo(rid, filePath)
        if not fileSaved:
            return False
        if(not os.path.isfile(filePath)):
            return False
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success
    
# Get a resource relation graph for the resource we uploaded
    def testGetGraph(self, rid):
        filePath = "./Downloads/downloadedGraph.dot"
        fileSaved = self.testApi.getGraphFromRepo(rid, filePath)
        if not fileSaved:
            return False
        if(not os.path.isfile(filePath)):
            return False
        
        success = os.path.getsize(filePath) > 0 # Check if file actually has contents
        os.remove(filePath)
        return success

# Upload metadata for a stream
    def testUploadMetadata(self, streamMetadata):
        mdo_rid = self.testApi.uploadMetadataToRepo(streamMetadata)
        success = self.utils.isValidGUID(mdo_rid)
        return success, mdo_rid
            
        # if(mdo_rid == "An EventStream for that StreamTopic and Host already exist. Use the Overwrite key if you wish to change it."):
        #     print("Post EventStream MDO test failed")

# Update metadata for a stream
    def testUpdateMetadata(self, rid, streamMetadata):
        mdo_rid = self.testApi.updateMetadataOnRepo(rid, streamMetadata)
        if not self.utils.isValidGUID(mdo_rid):
            print("mdo_rid invalid: " + str(mdo_rid))
            return False
        return self.testGetStreamMDO(mdo_rid, streamMetadata)

# Get the metadata object that we just uploaded info for
    def testGetStreamMDO(self, rid, streamMetadata):
        stream_mdo = self.testApi.getMetadataFromRepo(rid)
        print("stream_mdo: " + str(stream_mdo))
        if not stream_mdo:
            return False
        if(stream_mdo == "No resource with that ID" or stream_mdo == "Invalid FormData keys"):
            return False
        
        if(stream_mdo.get("ResourceId") != rid):
            return False
        
        mdo_ResourceInfo = stream_mdo["ResourceInfo"]
        if(not mdo_ResourceInfo):
            return False
        if(mdo_ResourceInfo.get("ResourceLabel") != streamMetadata.get("ResourceLabel")):
            return False
        if(mdo_ResourceInfo.get("Description") != streamMetadata.get("Description")):
            return False
        if(mdo_ResourceInfo.get("Dynamic") != False):
            return False
        # Only verify the following if it's part of the formdata streamMetadata object
        if(streamMetadata.get("ResourceType") and mdo_ResourceInfo.get("ResourceType") != streamMetadata.get("ResourceType")):
            return False
        if(streamMetadata.get("Host") and mdo_ResourceInfo.get("Host") != streamMetadata.get("Host")):
            return False
        if(streamMetadata.get("StreamTopic") and mdo_ResourceInfo.get("StreamTopic") != streamMetadata.get("StreamTopic")):
            return False
        
        mdo_GenerationTree = stream_mdo.get("GenerationTree")
        mdo_parents = mdo_GenerationTree.get("Parents")
        mdi_parents = streamMetadata.get("Parents")
        if(mdo_parents and mdi_parents):
            print("\nParents exist, checking")
            print("mdo parents: " + str(mdo_parents))
            print("mdi parents: " + str(mdi_parents))

            if(mdo_parents != json.loads(mdi_parents)):
                print("They are not the same")
                return False
            print("Parents match")
        
        # If all checks went through, return True.
        return True


# Get filtered list of metadata objects without EventStream
    def testFilteredMetadataList(self, filters):
        mdo_list = self.testApi.getFilteredMDOList(filters)
        if any (mdo["ResourceInfo"]["ResourceType"] == "EventStream" for mdo in mdo_list):
            return False
        if not any (mdo["ResourceInfo"]["ResourceType"] == "EventLog" for mdo in mdo_list):
            return False
        if not any (mdo["ResourceInfo"]["ResourceType"] == "Histogram" for mdo in mdo_list):
            return False
        
        return True
    
# Test metadata children
    def testChildrenMetadataList(self, mdo_rid_parent, metadata_child):
        print("testChildrenMetadataList with parent rid: " + mdo_rid_parent)
        metadata_child["Parents"] = json.dumps([
            {
                "ResourceId": mdo_rid_parent,
                "UsedAs": "Test"
            }
        ])
        print("metadata_child:")
        print(metadata_child)
        ridValid, mdo_rid_child = self.testUploadMetadata(metadata_child)
        if not ridValid:
            print("ridValid: " + str(ridValid))
            return False
        upload_success = self.testGetStreamMDO(mdo_rid_child, metadata_child)
        if not upload_success:
            print("upload_success: " + str(upload_success))
            return False
        
        mdo_list = self.testApi.getChildrenMDOList(mdo_rid_parent)
        print("mdo_list: " + str(mdo_list))
        if not any (mdo.get("ResourceId") == mdo_rid_child for mdo in mdo_list):
            print("Found no expected resource IDs")
            return False
        
        return True
    
    
# ------------------------ MINER TEST CASES --------------------------
# Miner ping
    def testMinerPing(self):
        response = self.testApi.pingMiner()
        if(response == "pong"):
            return True
        return False
    

# Test miner config list
    def testGetMinerConfig(self):
        config_list = self.testApi.getMinerConfigList()
        if any (config.get("MinerId") == "1" for config in config_list):
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
            return False, pid
        if(pid == "Invalid request. No miner with that ID. Config may be out of date, consider refreshing the frontend."):
            return False, pid
        if("Resources defined by body does not match config for the miner" in pid):
            return False, pid
        
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
    def testFileMinerStop(self, pid):
        expResp = "Killed process with ID: " + pid
        response = self.testApi.stopMinerAlgorithm(pid)
        if(response != expResp):
            return False
        
        status_list = self.testApi.getMinerStatusList()
        if any (status_obj["ProcessId"] == pid for status_obj in status_list):
            return False
        
        return True


# Test file miner start and stop (start and stop a file miner)
    def testFileMinerStartAndStop(self, mdo):
        success, pid = self.testFileMinerStart(mdo)
        if(not success):
            return False
        
        return self.testFileMinerStop(pid)
        # expResp = "Killed process with ID: " + pid
        # response = self.testApi.stopMinerAlgorithm(pid)
        # if(response != expResp):
        #     return False
        
        # status_list = self.testApi.getMinerStatusList()
        # if any (status_obj["ProcessId"] == pid for status_obj in status_list):
        #     return False
        
        # return True



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
        if(not stream_mdo):
            return False
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
    def testCloneStart(self, body):
        cid = self.testApi.runMinerCloning(body)
        print("cloning id: " + cid)
        success = not "Error retrieving miner from external source: Invalid request" in cid
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