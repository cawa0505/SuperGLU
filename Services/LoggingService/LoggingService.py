# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from Core.Messaging import Message
from Core.MessagingGateway import BaseService
from Services.Tables import IncomingMessage
from Util.Serialization import serializeObject, nativizeObject

class BaseLoggingService(BaseService):
    """ A service for logging messages """

    def receiveMessage(self, msg):
        if isinstance(msg, Message):
            self.logMessage(msg)

    def logMessage(self, msg):
        self._logMessage(msg)

    def _logMessage(self, msg):
        raise NotImplementedError
    


class DBLoggingService(BaseLoggingService):
    
    def __init__(self, anId=None):
        super(DBLoggingService, self).__init__(anId)
        
    def _logMessage(self, msg):
        #this code should be moved to a service when we re-organize.
        incomingMsg = IncomingMessage(rawMessage=serializeObject(msg))
        incomingMsg.save()
        copyOfincomingMsg = incomingMsg.find_one(incomingMsg.id);
        print("database results:");
        print(copyOfincomingMsg.to_data());
    
class CSVLoggingService(BaseLoggingService):
    SEP_CHAR = ','
    QUOTE_CHAR = '"'

    def __init__(self, fileName, sep=SEP_CHAR, quote=QUOTE_CHAR, anId=None):
        super(CSVLoggingService, self).__init__(anId)
        self._fileName = fileName
        self._sep = sep
        self._quote = quote

    def _logMessage(self, msg):
        with open(self._fileName, 'ab') as aFile:
            writer = csv.writer(aFile, delimiter=self._sep,
                                quotechar=self._quote)
            outrow = [datetime.now().isoformat()]
            outrow += msg.makeFlatMessage()
            writer.writerow(outrow)


class BadDialogLogger(BaseLoggingService):
    REPORT_BAD_UTTERANCE_VERB = "Has Bad Utterance"
    # Format: A=DialogId, V=Report Bad Utterance, O=Utterance (Speaker),
    #         R=Comments, Authentication=Username
    
    def logMessage(self, msg):
        if msg.getVerb() == self.REPORT_BAD_UTTERANCE_VERB:
            self._logMessage(msg)

class BadDialogCSVLogger(CSVLoggingService, BadDialogLogger):
    pass


if __name__ == '__main__':
    testFile = 'testFile.csv'
    testFile2 = 'badVoices.csv'
    logger = CSVLoggingService(testFile)
    logger2 = BadDialogCSVLogger(testFile2)
    logger.receiveMessage(Message("HE", "WROTE", "THIS"))
    logger2.receiveMessage(Message("HE", "WROTE", "THIS"))
    logger.receiveMessage(Message("HE", BadDialogLogger.REPORT_BAD_UTTERANCE_VERB, "THIS"))
    logger2.receiveMessage(Message("HE", BadDialogLogger.REPORT_BAD_UTTERANCE_VERB, "THIS"))
