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
    # SR PING
        success = testCases.testSRPing()
        SRTestDict["testSRPing"] = success

        
    # SR add miner
        success = testCases.testSRAddMiners()
        SRTestDict["testSRAddMiners"] = success

        
    # SR get list of miner URLs
        success = testCases.testSRGetMiner()
        SRTestDict["testSRGetMiners"] = success

        
    # SR delete miner
        success = testCases.testSRDeleteMiner()
        SRTestDict["testSRDeleteMiner"] = success

        
    # SR add repository
        success = testCases.testSRAddRepository()
        SRTestDict["testSRAddRepository"] = success

        
    # SR get list of repository URLs
        success = testCases.testSRGetRepositories()
        SRTestDict["testSRGetRepositories"] = success

        
    # SR delete repository
        success = testCases.testSRDeleteRepository()
        SRTestDict["testSRDeleteRepository"] = success

        
    # SR get filtered connection URLs
        success = testCases.testSRFilteredConnections()
        SRTestDict["testSRFilteredConnections"] = success

        
    # SR get filtered configs
        success = testCases.testSRFilteredConfigs()
        SRTestDict["testSRFilteredConfigs"] = success


    

    # ------------------------ REPOSITORY TEST RUNS --------------------------
    # Repository ping
        success = testCases.testRepoPing()
        SRTestDict["testRepoPing"] = success

    # Repository config
        success = testCases.testRepoConfig()
        SRTestDict["testRepoConfig"] = success

    # Upload file resource
        success, file_rid = testCases.testFileUpload('./Resources/ML4_log.xes', self.logMetadata)
        repoTestDict["testFileUpload"] = success

    # Update file resource
        success, file_rid = testCases.testFileUpdate('./Resources/ML4_log.xes', self.logMetadata)
        repoTestDict["testFileUpload"] = success

    # Get metadata for the file resource we uploaded
        success, file_mdo = testCases.testGetFileMDO(file_rid, self.logMetadata)
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
        success, mdo_rid = testCases.testUploadMetadata(self.streamMetadata)
        repoTestDict["testUploadMetadata"] = success

    # Update metadata for a stream
        success, mdo_rid = testCases.testUpdateMetadata(self.streamMetadataUpdate)
        repoTestDict["testUploadMetadata"] = success

    # Get the metadata object that we just uploaded info for
        success = testCases.testGetStreamMDO(mdo_rid, self.streamMetadataUpdate)
        repoTestDict["testGetStreamMDO"] = success

    # Test filtered list of metadata objects
        success = testCases.testFilteredMetadataList(self.filters)
        repoTestDict["testFilteredMetadataList"] = success

    # Test list of children metadata objects
        # success = testCases.testChildrenMetadataList(mdo_rid)
        # repoTestDict["testChildrenMetadataList"] = success
        

    # ------------------------ MINER TEST RUNS --------------------------
    # Miner ping
        success = testCases.testMinerPing()
        SRTestDict["testMinerPing"] = success


    # Test miner config list
        success = testCases.testGetMinerConfig()
        minerTestDict["testGetMinerConfig"] = success


    # Test file consuming miner start
        success, file_pid = testCases.testFileMinerStart(file_mdo)
        minerTestDict["testFileMinerStart"] = success


    # Test file miner status - unable to test since it would remove it. Is tested as part of "testFileMinerResult" instead
        # success = testCases.testFileMinerStatus(file_pid)
        # minerTestDict["testFileMinerStatus"] = success

        
    # Test miner status list
        success = testCases.testMinerStatusList(file_pid)
        minerTestDict["testMinerStatusList"] = success



    # Test file miner get result from repo
        success = testCases.testFileMinerResult(file_pid)
        minerTestDict["testFileMinerResult"] = success



    # Test file miner stop (start and stop a file miner)
        success = testCases.testFileMinerStartAndStop(file_mdo)
        minerTestDict["testFileMinerStop"] = success



    # Test publisher via a file consuming miner start
        success, stream_mdo, pub_pid = testCases.testPublisherStart()
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
        success = testCases.testStreamMinerStop(stream_pid, pub_pid)
        minerTestDict["testStreamMinerStop"] = success



    # Test get miner algorithm file
        success = testCases.testGetAlgorithmFile("1")
        minerTestDict["testGetAlgorithmFile"] = success



    # Test get miner algorithm requirements
        success = testCases.testGetRequirementsFile("1")
        minerTestDict["testGetRequirementsFile"] = success



    # Test run cloning action
        success, cid = testCases.testCloneStart(self.cloning_body)
        minerTestDict["testCloneStart"] = success



    # Test get cloning status
        success = testCases.testCloneStatus(cid)
        minerTestDict["testCloneStatus"] = success



    # Test run cloned miner algorithm
        success = testCases.testClonedAlgorithm(cid)
        minerTestDict["testClonedAlgorithm"] = success



    # ------------------------ PRINT TEST RESULTS --------------------------
        print("\n\nPOSITIVE REPOSITORY TEST RESULTS: \n")
        repoTestDictPretty = json.dumps(repoTestDict, indent=2)
        print(repoTestDictPretty)

        print("\n\nPOSITIVE MINER TEST RESULTS: \n")
        minerTestDictPretty = json.dumps(minerTestDict, indent=2)
        print(minerTestDictPretty)


# Consider if we should do additional cleanup afterwards?
