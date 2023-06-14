from uuid import UUID
import re

class Utils() :
    def isValidGUID(self, str):
 
        # Regex to check valid
        # GUID (Globally Unique Identifier)
        regex = "^[{]?[0-9a-fA-F]{8}" + "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$"

        # Compile the ReGex
        p = re.compile(regex)
    
        # If the string is empty
        # return false
        if (str == None):
            return False
    
        # Return if the string
        # matched the ReGex
        if(re.search(p, str)):
            return True
        else:
            return False
        