#  ServiceError represents a base error result
class ServiceError():
    code: str
    message: str
    status: int
    cause: Exception

    def __init__(self, cd="", mesg="", stat=-1, root: Exception=None):
        self.code = cd
        self.message = mesg
        self.status = stat
        self.cause = root
    # end def: __init__

    def isError(self):
        return (self.code != None and len(self.code) > 0)
    # end def: isError

    def hasStatus(self):
        return self.status > -1
    # end def: hasStatus

    def withCause(self, src: Exception):
        return ServiceError(self.code, self.message, self.status, src)
    # end def: withCause

    def withMesg(self, mesg: str):
        return ServiceError(self.code, mesg, self.status, self.cause)
    # end def: withMesg

    def toString(self):
        if self.cause == None:
            return f"{self.code=}: {self.message=}"
        else:
            return f"{self.code=}: {self.message=}\n{self.cause=}"
    # end def: toString
# end class: ServiceError

NoError = ServiceError()

ClientRequestError   = ServiceError("A01", "Error sending function request.")
ClientReadError      = ServiceError("A02", "Error reading function response.")
ClientInputError     = ServiceError("A03", "Error reading input file.")
ClientOutputError    = ServiceError("A04", "Error writing to output file.")
ClientProtocolError  = ServiceError("A05", "Error in service communication.")
ClientError          = ServiceError("A06", "An internal client error has occurred.")

SyncIntervalError    = ServiceError("V01", "Invalid sync interval configuration.")

DbQueryError         = ServiceError("D01", "Error querying weather info.", 500)
DbScanError          = ServiceError("D02", "Error scanning weather info.", 500)
DbResultsError       = ServiceError("D03", "Got unknown results error.", 500)
DbInsertError        = ServiceError("D04", "Error inserting weather info.", 500)
DbPrepareError       = ServiceError("D05", "Error preparing statement.", 500)
DbExecuteError       = ServiceError("D06", "Error executing statement.", 500)
DbClientError        = ServiceError("D07", "Error getting weather DB client.", 500)
DbOpenError          = ServiceError("D08", "Error opening weather DB.", 500)
DbPKeyError          = ServiceError("D09", "Primary key already exists.", 409)
DbPKeyMissingError   = ServiceError("D10", "Primary key not found.", 404)
DbUpdateError        = ServiceError("D11", "Error updating weather info.", 500)
DbInvalidError       = ServiceError("D12", "Policy information invalid.", 502)

SystemError          = ServiceError("S00", "An internal error has occurred.", 500)
DatetimeError        = ServiceError("S01", "A datetime error has occurred.", 500)
IOError              = ServiceError("S02", "An input/output error has occurred.", 500)
PolicyError          = ServiceError("S03", "Error response received from Policy Manager.")
