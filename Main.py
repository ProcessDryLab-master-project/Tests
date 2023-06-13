from API import API
from TestCases import TestCases
import time
from uuid import UUID
import json


class Main() :
    testCases = TestCases()
    testApi = API()
    repoTestDict = dict()
    minerTestDict = dict()

# ------------------------ REPOSITORY TEST RUNS --------------------------
# Upload file resource
    success, file_rid = testCases.testFileUpload()
    repoTestDict["testFileUpload"] = success

# Get metadata for the file resource we uploaded
    success, file_mdo = testCases.testGetFileMDO(file_rid)
    repoTestDict["testGetFileMDO"] = success

# Get the resource we just uploaded
    success = testCases.testGetFile(file_rid)
    repoTestDict["testGetFile"] = success

# Get a histogram of the resource we uploaded
    success = testCases.testGetHistogram(file_rid)
    repoTestDict["testGetHistogram"] = success

# Get a graph of the resource we uploaded
    success = testCases.testGetGraph(file_rid)
    repoTestDict["testGetGraph"] = success

# Upload metadata for a stream
    success, mdo_rid = testCases.testUploadMetadata()
    repoTestDict["testUploadMetadata"] = success

# Get the metadata object that we just uploaded info for
    success = testCases.testGetStreamMDO(mdo_rid)
    repoTestDict["testGetStreamMDO"] = success

# Test filtered list of metadata objects
    success = testCases.testFilteredMetadataList()
    repoTestDict["testFilteredMetadataList"] = success
    

# ------------------------ MINER TEST RUNS --------------------------
# Test miner config list
    success = testCases.testGetMinerConfig()
    minerTestDict["testGetMinerConfig"] = success


# Test file consuming miner start
    success, file_pid = testCases.testFileMinerStart(file_mdo)
    minerTestDict["testFileMinerStart"] = success

    
# Test miner status list
    success = testCases.testMinerStatusList(file_pid)
    minerTestDict["testMinerStatusList"] = success


# Test file miner status
    success = testCases.testFileMinerStatus(file_pid)
    minerTestDict["testFileMinerStatus"] = success



# Test file miner get result from repo
    success = testCases.testFileMinerResult(file_pid)
    minerTestDict["testFileMinerResult"] = success



# Test file miner stop (start and stop a file miner)
    success = testCases.testFileMinerStop(file_mdo)
    minerTestDict["testFileMinerStop"] = success



# Test publisher via a file consuming miner start
    success, stream_mdo = testCases.testPublisherStart()
    minerTestDict["testPublisherStart"] = success



# Test stream consuming miner start
    success, stream_pid = testCases.testStreamMinerStart(stream_mdo)
    minerTestDict["testStreamMinerStart"] = success



# Test stream miner status
    success = testCases.testStreamMinerStatus(stream_pid)
    minerTestDict["testStreamMinerStatus"] = success



# Test stream miner get result from repo
    success = testCases.testStreamMinerResult(stream_pid)
    minerTestDict["testStreamMinerResult"] = success



# Test stream miner stop
    success = testCases.testStreamMinerStop(stream_pid)
    minerTestDict["testStreamMinerStop"] = success



# Test get miner algorithm file
    success = testCases.testGetAlgorithmFile()
    minerTestDict["testGetAlgorithmFile"] = success



# Test get miner algorithm requirements
    success = testCases.testGetRequirementsFile()
    minerTestDict["testGetRequirementsFile"] = success



# Test run cloning action
    success, cid = testCases.testCloneStart()
    minerTestDict["testCloneStart"] = success



# Test get cloning status
    success = testCases.testCloneStatus(cid)
    minerTestDict["testCloneStatus"] = success



# Test run cloned miner algorithm
    success = testCases.testClonedAlgorithm(cid, file_mdo)
    minerTestDict["testClonedAlgorithm"] = success



# ------------------------ PRINT TEST RESULTS --------------------------
    print("\n\nREPOSITORY TEST RESULTS: \n")
    repoTestDictPretty = json.dumps(repoTestDict, indent=2)
    print(repoTestDictPretty)

    print("\n\MINER TEST RESULTS: \n")
    minerTestDictPretty = json.dumps(minerTestDict, indent=2)
    print(minerTestDictPretty)

