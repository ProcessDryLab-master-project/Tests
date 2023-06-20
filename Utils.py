from uuid import UUID
import re

class Utils() :
    def isValidGUID(self, id):
        print("Checking if string is GUID: " + str(id))
        # Regex to check valid
        # GUID (Globally Unique Identifier)
        regex = "^[{]?[0-9a-fA-F]{8}" + "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$"

        # Compile the ReGex
        p = re.compile(regex)
    
        # If the string is empty
        # return false
        if (id == None):
            return False
    
        # Return if the string
        # matched the ReGex
        if(re.search(p, id)):
            return True
        else:
            return False
        