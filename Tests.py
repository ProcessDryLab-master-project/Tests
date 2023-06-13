from API import API
import time


class Tests() :
    testApi = API()

# Upload file resource
    file_rid = testApi.uploadResourceToRepo()
# SLEEP TO AVOID ERROR:
    # time.sleep(3)
# ERROR HERE! HAPPENS TOO FAST FOR REPOSITORY TO KEEP UP!
# Get metadata for the file resource we uploaded
    file_mdo = testApi.getMetadataFromRepo(file_rid)
    if(file_mdo == "No resource with that ID"):
        print("Get file mdo test failed")

# Get the resource we just uploaded
    testApi.getResourceFromRepo(file_rid)

# Get a histogram of the resource we uploaded
    testApi.getHistogramFromRepo(file_rid)

# Upload metadata for a stream
    mdo_rid = testApi.uploadMetadataToRepo()
    if(mdo_rid == "An EventStream for that StreamTopic and Host already exist. Use the Overwrite key if you wish to change it."):
        print("Post EventStream MDO test failed")

# Get the metadata object that we just uploaded info for
    testApi.getMetadataFromRepo(mdo_rid)
    if(file_mdo == "No resource with that ID"):
        print("Get stream mdo test failed")

