from API import API


class Tests() :
    testApi = API()

# Upload file resource
    file_rid = testApi.uploadResourceToRepo()

# ERROR HERE! HAPPENS TO FAST FOR REPOSITORY TO KEEP UP!
# Get metadata for the file resource we uploaded
    testApi.getMetadataFromRepo(file_rid)

# Get the resource we just uploaded
    testApi.getResourceFromRepo(file_rid)

# Get a histogram of the resource we uploaded
    testApi.getHistogramFromRepo(file_rid)

# Upload metadata for a stream
    mdo_rid = testApi.uploadMetadataToRepo()
    
# Get the metadata object that we just uploaded info for
    testApi.getMetadataFromRepo(mdo_rid)

