from API import API
from TestCases import TestCases
import time
from uuid import UUID
import json


class Negative() :
    logMetadataValid = {
        'FileExtension': 'pnml',
        'ResourceLabel': 'ML4_model',
        'ResourceType': 'PetriNet',
        'Description': 'ML4 Test Petri Net'
    }
    logMetadataInvalid = {  # No ResourceType, Repository should not accept it.
        'FileExtension': 'xes',
        'ResourceLabel': 'ML4_log',
        'Description': 'ML4 Test log'
    }
    streamMetadataValid = {
        'Host': 'mqtt.eclipseprojects.io',
        'StreamTopic': 'TestStream',
        'ResourceLabel': 'Test Stream',
        'ResourceType': 'EventStream',
        'Description': 'Stream for testing',
        'Overwrite': 'true'
    }
    streamMetadataInvalid = {       # An EventStream without a topic should be blocked
        'Host': 'mqtt.eclipseprojects.io',
        'ResourceLabel': 'Test Stream',
        'ResourceType': 'EventStream',
        'Description': 'Stream for testing',
        'Overwrite': 'true'
    }
    invalidFilters = [
        "IN",
        "VALID"
    ]
    cloning_body =   {
        "Host": "http://localhost:5000/shadow/",
        "Config":   {
            "MinerId": "3",
            "MinerLabel": "Inductive Miner",
            "Type": "Miner",
            "MinerPath": "Miners/MinerInductiveBpmnPy",
            "MinerFile": "MinerInductiveBpmn.py",
            "Access": "Public",
            "Shadow": False,    # Shadow is false, so it should be rejected
            "ResourceInput": [
            {
                "Name": "LogToRun",
                "FileExtension": "xes",
                "ResourceType": "EventLog"
            }
            ],
            "ResourceOutput": {
            "FileExtension": "bpmn",
            "ResourceType": "ProcessModel"
            },
            "MinerParameters": []
        }
    }

    def negativeTestRun(self):
        testCases = TestCases()
        repoTestDict = dict()
        minerTestDict = dict()

    # # ------------------------ REPOSITORY TEST RUNS --------------------------
    # # Upload file with invalid metadata
    #     success, file_rid = testCases.testFileUpload('./Resources/ML4_log.xes', self.logMetadataInvalid)
    #     repoTestDict["testFileUpload"] = not success

    # # Request metadata with invalid RID
    #     success, error = testCases.testGetFileMDO("18752fc4-a019-4266-8ad7-ff1d6e47b7e4", self.logMetadataValid)
    #     repoTestDict["testGetFileMDO"] = not success

    # # Request file with invalid RID
    #     success = testCases.testGetFile("18752fc4-a019-4266-8ad7-ff1d6e47b7e4")
    #     repoTestDict["testGetFile"] = not success

    # # Request graph with invalid RID
    #     success = testCases.testGetGraph("18752fc4-a019-4266-8ad7-ff1d6e47b7e4")
    #     repoTestDict["testGetGraph"] = not success

    # Upload valid pnml file to use later
        success, file_rid = testCases.testFileUpload('./Resources/ML4_model.pnml', self.logMetadataValid)
        success, file_mdo = testCases.testGetFileMDO(file_rid, self.logMetadataValid)
        print("valid file_mdo: " + str(file_mdo))
        # repoTestDict["testFileUpload"] = success # Has to work for later tests to make sense

    # # Request histogram for the PNML, which should not be possible.
    #     success = testCases.testGetHistogram(file_rid)
    #     repoTestDict["testGetHistogram"] = not success

    # # Upload invalid metadata for a stream
    #     success, mdo_rid = testCases.testUploadMetadata(self.streamMetadataInvalid)
    #     repoTestDict["testUploadMetadata"] = not success

    # # Request metadata object with invalid RID
    #     success = testCases.testGetStreamMDO("18752fc4-a019-4266-8ad7-ff1d6e47b7e4", self.streamMetadataValid)
    #     repoTestDict["testGetStreamMDO"] = not success

    # # Request list of metadata objects with invalid filters
    #     success = testCases.testFilteredMetadataList(self.invalidFilters)
    #     repoTestDict["testFilteredMetadataList"] = not success
        

    # ------------------------ MINER TEST RUNS --------------------------
    # # Test miner config list
    #     success = testCases.testGetMinerConfig()
    #     minerTestDict["testGetMinerConfig"] = success


    # Test file consuming miner start with invalid metadata input (PNML instead of XES)
        success, file_pid = testCases.testFileMinerStart(file_mdo)
        minerTestDict["testFileMinerStart"] = not success


    # Test file miner status - unable to test since it would remove it. Is tested as part of "testFileMinerResult" instead
        # success = testCases.testFileMinerStatus(file_pid)
        # minerTestDict["testFileMinerStatus"] = success

        
    # Test that miner has no active processes
        success = testCases.testMinerStatusList(file_pid)
        minerTestDict["testMinerStatusList"] = not success



    # # Test file miner get result from repo
    #     success = testCases.testFileMinerResult(file_pid)
    #     minerTestDict["testFileMinerResult"] = success



    # # Try to stop a process that doesn't exist
    #     success = testCases.testFileMinerStop("InvalidPid")
    #     minerTestDict["testFileMinerStop"] = not success



    # # Test publisher via a file consuming miner start
    #     success, stream_mdo, pub_pid = testCases.testPublisherStart()
    #     minerTestDict["testPublisherStart"] = success

        # Start and stop a publisher immediately to have an inactive stream
    #     success, stream_mdo, pub_pid = testCases.testPublisherStart()
    #     success = testCases.testFileMinerStop(pub_pid)

    # # Test stream consuming miner on inactive stream_mdo
    #     success, stream_pid = testCases.testStreamMinerStart(stream_mdo)
    #     minerTestDict["testStreamMinerStart"] = success



    # # Test stream miner status
    #     success = testCases.testStreamMinerStatus(stream_pid)
    #     minerTestDict["testStreamMinerStatus"] = success



    # # Test stream miner get result from repo
    #     success = testCases.testStreamMinerResult(stream_pid)
    #     minerTestDict["testStreamMinerResult"] = success



    # # Test stream miner stop
    #     success = testCases.testStreamMinerStop(stream_pid, pub_pid)
    #     minerTestDict["testStreamMinerStop"] = success



    # Test get miner algorithm file for unshadowable miner
        success = testCases.testGetAlgorithmFile("2")
        minerTestDict["testGetAlgorithmFile"] = not success



    # Test get miner algorithm requirements unshadowable miner
        success = testCases.testGetRequirementsFile("2")
        minerTestDict["testGetRequirementsFile"] = not success



    # Test run cloning action
        success, cid = testCases.testCloneStart(self.cloning_body)
        print("negative cid")
        minerTestDict["testCloneStart"] = not success



    # # Test that there is no cloning status
    #     success = testCases.testCloneStatus(cid)
    #     minerTestDict["testCloneStatus"] = not success



    # # Test run cloned miner algorithm
    #     success = testCases.testClonedAlgorithm(cid)
    #     minerTestDict["testClonedAlgorithm"] = success



    # ------------------------ PRINT TEST RESULTS --------------------------
        print("\n\nNEGATIVE REPOSITORY TEST RESULTS: \n")
        repoTestDictPretty = json.dumps(repoTestDict, indent=2)
        print(repoTestDictPretty)

        print("\n\nNEGATIVE MINER TEST RESULTS: \n")
        minerTestDictPretty = json.dumps(minerTestDict, indent=2)
        print(minerTestDictPretty)


# Consider if we should do additional cleanup afterwards?
