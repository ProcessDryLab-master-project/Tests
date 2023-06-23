from PositiveTests import Positive
from NegativeTests import Negative
import json
import os

class Main() :
    downloadsDir = "./Downloads"
    if not os.path.exists(downloadsDir):
        print("Creating Downloads dir since it does not exist")
        os.makedirs(downloadsDir)

    print("\nRUNNING POSITIVE TESTS\n")
    positive = Positive()
    SRTestDictPos, repoTestDictPos, minerTestDictPos = positive.positiveTestRun()

    print("\nRUNNING NEGATIVE TESTS\n")
    negative = Negative()
    repoTestDictNeg, minerTestDictNeg = negative.negativeTestRun()


    
# ------------------------ PRINT POSITIVE TEST RESULTS --------------------------

    print("\n\nPOSITIVE SERVICE REGISTRY TEST RESULTS: \n")
    SRTestDictPretty = json.dumps(SRTestDictPos, indent=2)
    print(SRTestDictPretty)

    print("\n\nPOSITIVE REPOSITORY TEST RESULTS: \n")
    repoTestDictPretty = json.dumps(repoTestDictPos, indent=2)
    print(repoTestDictPretty)

    print("\n\nPOSITIVE MINER TEST RESULTS: \n")
    minerTestDictPretty = json.dumps(minerTestDictPos, indent=2)
    print(minerTestDictPretty)


# ------------------------ PRINT TEST RESULTS --------------------------
    print("\n\nNEGATIVE REPOSITORY TEST RESULTS: \n")
    repoTestDictPretty = json.dumps(repoTestDictNeg, indent=2)
    print(repoTestDictPretty)

    print("\n\nNEGATIVE MINER TEST RESULTS: \n")
    minerTestDictPretty = json.dumps(minerTestDictNeg, indent=2)
    print(minerTestDictPretty)