from API import API
from TestCases import TestCases
import time
from uuid import UUID
import json


class Positive() :
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
    streamMetadataUpdate = {
        'Host': 'mqtt.eclipseprojects.io',
        'StreamTopic': 'TestStream',
        'ResourceLabel': 'Updated Test Stream',
        'ResourceType': 'EventStream',
        'Description': 'Updated Stream for testing',
        'Overwrite': 'true'
    }
    streamMetadataChild = {
        'Host': 'mqtt.eclipseprojects.io',
        'StreamTopic': 'TestStreamChild',
        'ResourceLabel': 'Test Stream Child',
        'ResourceType': 'EventStream',
        'Description': 'Child of stream for testing',
        'Overwrite': 'true'
    }
    filters = [
        "EventLog",
        "Histogram"
    ]
    cloning_body =   {
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

    def positiveTestRun(self):
        testCases = TestCases()
        SRTestDict = dict()
        repoTestDict = dict()
        minerTestDict = dict()

        
    # ------------------------ SERVICE REGISTRY TEST RUNS --------------------------
        print("\n\n\nRUNNING POSITIVE SERVICE REGISTRY TESTS")

    # SR PING
        print("\nRunning testSRPing")
        success = testCases.testSRPing()
        print("testSRPing: " + str(success))
        SRTestDict["testSRPing"] = success

        
    # SR add miner
        print("\nRunning testSRAddMiners")
        success = testCases.testSRAddMiners()
        print("testSRAddMiners: " + str(success))
        SRTestDict["testSRAddMiners"] = success

        
    # SR get list of miner URLs
        print("\nRunning testSRGetMiner")
        success = testCases.testSRGetMiners()
        print("testSRGetMiners: " + str(success))
        SRTestDict["testSRGetMiners"] = success

        
    # SR delete miner
        print("\nRunning testSRDeleteMiner")
        success = testCases.testSRDeleteMiner()
        print("testSRDeleteMiner: " + str(success))
        SRTestDict["testSRDeleteMiner"] = success

        
    # SR add repository
        print("\nRunning testSRAddRepository")
        success = testCases.testSRAddRepository()
        print("testSRAddRepository: " + str(success))
        SRTestDict["testSRAddRepository"] = success

        
    # SR get list of repository URLs
        print("\nRunning testSRGetRepositories")
        success = testCases.testSRGetRepositories()
        print("testSRGetRepositories: " + str(success))
        SRTestDict["testSRGetRepositories"] = success

        
    # SR delete repository
        print("\nRunning testSRDeleteRepository")
        success = testCases.testSRDeleteRepository()
        print("testSRDeleteRepository: " + str(success))
        SRTestDict["testSRDeleteRepository"] = success

        
    # SR get filtered connection URLs
        print("\nRunning testSRFilteredConnections")
        success = testCases.testSRFilteredConnections()
        print("testSRFilteredConnections: " + str(success))
        SRTestDict["testSRFilteredConnections"] = success

        
    # SR get filtered configs
        print("\nRunning testSRFilteredConfigs")
        success = testCases.testSRFilteredConfigs()
        print("testSRFilteredConfigs: " + str(success))
        SRTestDict["testSRFilteredConfigs"] = success


    

    # ------------------------ REPOSITORY TEST RUNS --------------------------
        print("\n\n\nRUNNING POSITIVE REPOSITORY TESTS")

    # Repository ping
        print("\nRunning testRepoPing")
        success = testCases.testRepoPing()
        print("testRepoPing: " + str(success))
        repoTestDict["testRepoPing"] = success

    # Repository config
        print("\nRunning testRepoConfig")
        success = testCases.testRepoConfig()
        print("testRepoConfig: " + str(success))
        repoTestDict["testRepoConfig"] = success

    # Upload file resource
        print("\nRunning testFileUpload")
        success, file_rid = testCases.testFileUpload('./Resources/ML4_log.xes', self.logMetadata)
        print("testFileUpload: " + str(success))
        repoTestDict["testFileUpload"] = success

    # Get metadata for the file resource we uploaded
        print("\nRunning testGetFileMDO")
        success, file_mdo = testCases.testGetFileMDO(file_rid, self.logMetadata)
        print("testGetFileMDO: " + str(success))
        repoTestDict["testGetFileMDO"] = success

    # Get the resource we just uploaded
        print("\nRunning testGetFile")
        success = testCases.testGetFile(file_rid)
        print("testGetFile: " + str(success))
        repoTestDict["testGetFile"] = success

    # Update file resource
        print("\nRunning testFileUpdate")
        success = testCases.testFileUpdate('./Resources/ML4_log.xes', self.logMetadata)
        print("testFileUpdate: " + str(success))
        repoTestDict["testFileUpdate"] = success

    # Get a histogram of the resource we uploaded
        print("\nRunning testGetHistogram")
        success = testCases.testGetHistogram(file_rid)
        print("testGetHistogram: " + str(success))
        repoTestDict["testGetHistogram"] = success

    # Get a graph of the resource we uploaded
        print("\nRunning testGetGraph")
        success = testCases.testGetGraph(file_rid)
        print("testGetGraph: " + str(success))
        repoTestDict["testGetGraph"] = success

    # Upload metadata for a stream
        print("\nRunning testUploadMetadata")
        success, mdo_rid = testCases.testUploadMetadata(self.streamMetadata)
        print("testUploadMetadata: " + str(success))
        repoTestDict["testUploadMetadata"] = success

    # Get the metadata object that we just uploaded info for
        print("\nRunning testGetStreamMDO")
        success = testCases.testGetStreamMDO(mdo_rid, self.streamMetadataUpdate)
        print("testGetStreamMDO: " + str(success))
        repoTestDict["testGetStreamMDO"] = success

    # Update metadata for a stream
        print("\nRunning testUpdateMetadata")
        success = testCases.testUpdateMetadata(self.streamMetadataUpdate)
        print("testUploadMetadata: " + str(success))
        repoTestDict["testUploadMetadata"] = success

    # Test filtered list of metadata objects
        print("\nRunning testFilteredMetadataList")
        success = testCases.testFilteredMetadataList(self.filters)
        print("testFilteredMetadataList: " + str(success))
        repoTestDict["testFilteredMetadataList"] = success

    # Test list of children metadata objects
        print("\nRunning testChildrenMetadataList")
        success = testCases.testChildrenMetadataList(mdo_rid, self.streamMetadataChild)
        print("testChildrenMetadataList: " + str(success))
        repoTestDict["testChildrenMetadataList"] = success
        

    # # ------------------------ MINER TEST RUNS --------------------------
    # # Miner ping
    #     success = testCases.testMinerPing()
    #     print("testMinerPing: " + str(success))
    #     minerTestDict["testMinerPing"] = success


    # # Test miner config list
    #     success = testCases.testGetMinerConfig()
    #     print("testGetMinerConfig: " + str(success))
    #     minerTestDict["testGetMinerConfig"] = success


    # # Test file consuming miner start
    #     success, file_pid = testCases.testFileMinerStart(file_mdo)
    #     print("testFileMinerStart: " + str(success))
    #     minerTestDict["testFileMinerStart"] = success


    # # Test file miner status - unable to test since it would remove it. Is tested as part of "testFileMinerResult" instead
    #     # success = testCases.testFileMinerStatus(file_pid)
    #     # minerTestDict["testFileMinerStatus"] = success

        
    # # Test miner status list
    #     success = testCases.testMinerStatusList(file_pid)
    #     print("testMinerStatusList: " + str(success))
    #     minerTestDict["testMinerStatusList"] = success



    # # Test file miner get result from repo
    #     success = testCases.testFileMinerResult(file_pid)
    #     print("testFileMinerResult: " + str(success))
    #     minerTestDict["testFileMinerResult"] = success



    # # Test file miner stop (start and stop a file miner)
    #     success = testCases.testFileMinerStartAndStop(file_mdo)
    #     print("testFileMinerStop: " + str(success))
    #     minerTestDict["testFileMinerStop"] = success



    # # Test publisher via a file consuming miner start
    #     success, stream_mdo, pub_pid = testCases.testPublisherStart()
    #     print("testPublisherStart: " + str(success))
    #     minerTestDict["testPublisherStart"] = success



    # # Test stream consuming miner start
    #     success, stream_pid = testCases.testStreamMinerStart(stream_mdo)
    #     print("testStreamMinerStart: " + str(success))
    #     minerTestDict["testStreamMinerStart"] = success



    # # Test stream miner status
    #     success = testCases.testStreamMinerStatus(stream_pid)
    #     print("testStreamMinerStatus: " + str(success))
    #     minerTestDict["testStreamMinerStatus"] = success



    # # Test stream miner get result from repo
    #     success = testCases.testStreamMinerResult(stream_pid)
    #     print("testStreamMinerResult: " + str(success))
    #     minerTestDict["testStreamMinerResult"] = success



    # # Test stream miner stop
    #     success = testCases.testStreamMinerStop(stream_pid, pub_pid)
    #     print("testStreamMinerStop: " + str(success))
    #     minerTestDict["testStreamMinerStop"] = success



    # # Test get miner algorithm file
    #     success = testCases.testGetAlgorithmFile("1")
    #     print("testGetAlgorithmFile: " + str(success))
    #     minerTestDict["testGetAlgorithmFile"] = success



    # # Test get miner algorithm requirements
    #     success = testCases.testGetRequirementsFile("1")
    #     print("testGetRequirementsFile: " + str(success))
    #     minerTestDict["testGetRequirementsFile"] = success



    # # Test run cloning action
    #     success, cid = testCases.testCloneStart(self.cloning_body)
    #     print("testCloneStart: " + str(success))
    #     minerTestDict["testCloneStart"] = success



    # # Test get cloning status
    #     success = testCases.testCloneStatus(cid)
    #     print("testCloneStatus: " + str(success))
    #     minerTestDict["testCloneStatus"] = success



    # # Test run cloned miner algorithm
    #     success = testCases.testClonedAlgorithm(cid)
    #     print("testClonedAlgorithm: " + str(success))
    #     minerTestDict["testClonedAlgorithm"] = success



    # ------------------------ PRINT TEST RESULTS --------------------------

        print("\n\nPOSITIVE SERVICE REGISTRY TEST RESULTS: \n")
        SRTestDictPretty = json.dumps(SRTestDict, indent=2)
        print(SRTestDictPretty)

        print("\n\nPOSITIVE REPOSITORY TEST RESULTS: \n")
        repoTestDictPretty = json.dumps(repoTestDict, indent=2)
        print(repoTestDictPretty)

        print("\n\nPOSITIVE MINER TEST RESULTS: \n")
        minerTestDictPretty = json.dumps(minerTestDict, indent=2)
        print(minerTestDictPretty)


# Consider if we should do additional cleanup afterwards?
