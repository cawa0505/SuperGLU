from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.LoggingService.Base_Learn_Logger import BaseLearnLogger
from SuperGLU.Services.LoggingService.Constants import *
import json
import time
from tincan import (
    Statement,
    Agent,
    Verb,
    Result,
    Activity,
    ActivityList,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
    Extensions,
    AgentAccount
)
import uuid
from context_activities import ContextActivities
import context_activities
from tincan.typed_list import TypedList
from representation.ActivityTree import ActivityTree


class xAPILearnLogger(BaseLearnLogger):

   

    URIBase = "https://github.com/GeneralizedLearningUtilities/SuperGLU"

    def __init__(self, gateway=None, userId=None, name=None, classroomId=None, taskId=None, url=None, activityType='', context={}, anId=None):
        #self.ActivityTree = ActivityTree()
        super(xAPILearnLogger, self).__init__(gateway, userId, name, classroomId, taskId, url, activityType, context, anId)

       
    '''Send the loaded message, for when the task is ready to start.
        Message Data: <frameName> | Loaded | <url> | true
        @param frameName: The name for the current window
        @type frameName: string
    '''

    def sendStartSession(self, timestamp = None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Session'}), description=LanguageMap({'en-US':'User Started a new Session'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + AppStart, display=LanguageMap({'en-US': 'started'}))
        result = Result(response = 'User started a new Session',)
        
        #self.ActivityTree.EnterActivity(label = "Session", activity = "User started a new Session")

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartTopic(self, timestamp = None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Topic'}), description=LanguageMap({'en-US':'User Started a new Topic'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + AppStart, display=LanguageMap({'en-US': 'started'}))
        result = Result(response = 'User started a new Topic',)
        
        #self.ActivityTree.EnterActivity(label = "Topic", activity = "User started a new Topic", parentLabel="Session")
        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartLesson(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Lesson'}),
            description=LanguageMap({'en-US':'User Started Lesson'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        
        #self.ActivityTree.EnterActivity(label = "Lesson", activity = "User started a new Lesson", parentLabel= "Session")
        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartSubLesson(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'SubLesson'}),
            description=LanguageMap({'en-US':'User Started SubLesson'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        
        #self.ActivityTree.EnterActivity(label = "SubLesson", activity = "User started a new SubLesson", parentLabel= "Lesson")        
        parentLabel = "Lesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendNewTask(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Task'}),
            description=LanguageMap({'en-US':'User Started new Task'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
       
        parentLabel = "Sublesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendNewStep(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Step'}),
            description=LanguageMap({'en-US':'User Started new Step'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Task"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendLoadedVideoLesson(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Video Lesson'}),
            description=LanguageMap({'en-US':'User Launched Video Lesson'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendLoadedVideoSubLesson(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Video SubLesson'}),
            description=LanguageMap({'en-US':'User Launched Video SubLesson'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Video Lesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartScenario(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Scenario'}),
            description=LanguageMap({'en-US':'User Started a Scenario'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        
        #self.ActivityTree.EnterActivity(label = "Scenario", activity = "User started a new Scenario", parentLabel= "Session")
        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartDialogue(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Dialogue'}),
            description=LanguageMap({'en-US':'User Started dialogue'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Scenario"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartDecision(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Decision'}),
            description=LanguageMap({'en-US':'User Started decision'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Dialogue"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartChoice(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Choice'}),
            description=LanguageMap({'en-US':'User Started Choice'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Decision"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartAAR(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'AAR'}),
            description=LanguageMap({'en-US':'User launched AAR'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Scenario"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartQuestion(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Question'}),
            description=LanguageMap({'en-US':'User started Question'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "AAR"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartAnswer(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Answer'}),
            description=LanguageMap({'en-US':'User started Answer'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Question"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendLoadedTask(self, frameName, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', name = frameName, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url,
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}),
            description=LanguageMap({'en-US':description})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        #self.ActivityTree.EnterActivity(label = "Video Lesson", activity = "User started Video", parentLabel="Session")
        parentLabel = "Sublesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)



    '''
    Send the task completed message
        Message Data: <userId> | Completed | <taskId> | <score>
        @param score: A score between 0 and 1. Scores outside this range will be clipped to fit. If score None, task presumed incomplete/invalid.
        @type score: float
    '''
    def sendTerminatedSession(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Session'}), description=LanguageMap({'en-US':'User Stopped Session'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + Exiting, display=LanguageMap({'en-US': Exiting}))
        result = Result(response = '',)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedLesson(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Lesson'}), description=LanguageMap({'en-US':'User Completed Lesson'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedSubLesson(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'SubLesson'}), description=LanguageMap({'en-US':'User Completed SubLesson'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Lesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedVideoLesson(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Video Lesson'}), description=LanguageMap({'en-US':'User Completed Video Lesson'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedVideoSubLesson(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Video SubLesson'}), description=LanguageMap({'en-US':'User Completed Video SubLesson'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Video Lesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedScenario(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Scenario'}), description=LanguageMap({'en-US':'User Completed Scenario'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Session"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedDialogue(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Dialogue'}), description=LanguageMap({'en-US':'User Completed Dialogue'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Scenario"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedDecision(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Decision'}), description=LanguageMap({'en-US':'User Completed Decision'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Dialogue"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedChoice(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Choice'}), description=LanguageMap({'en-US':'User Completed Choice'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Decision"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedAAR(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'AAR'}), description=LanguageMap({'en-US':'User Completed AAR'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Scenario"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedQuestion(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Question'}), description=LanguageMap({'en-US':'User Completed Question'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "AAR"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendCompletedAnswer(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Answer'}), description=LanguageMap({'en-US':'User Completed Answer'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Question"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTheTask(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Task'}), description=LanguageMap({'en-US':'User Completed Task'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Sublesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTask(self, score, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}),
            description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(score = self.clampToUnitValue(score),)
        parentLabel = "Sublesson"
        context = self.addContext(parentLabel)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send if all steps completed message (or % complete, if unfinished)
        Message Data: <userId> | CompletedAllSteps | <taskId> | <percentComplete>
        @param percentComplete: The percentage of steps that were completed. In [0,1]. If None, assumed 100%.
        @param percentComplete: float
    '''
    def sendCompletedAllSteps(self, percentComplete, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_ALL_STEPS_VERB , display=LanguageMap({'en-US': COMPLETED_ALL_STEPS_VERB}))

        if percentComplete == None:
            percentComplete = 1.0
        percentComplete = self.clampToUnitValue(percentComplete)
        result = Result(score = percentComplete*1.0,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send a message that a step was completed (or marked incomplete, alternatively).
        Message Data: <userId> | CompletedStep | <stepId> | <percentComplete>
        @param stepId: An id that represents the task situation (e.g., decision point) that the user completed or failed to complete. Uniquely represents some decision point in the current task.
        @type stepId: string
        @param isComplete: The amount of the step that was completed, from 0 (nothing completed) to 1 (fully complete).
        @type isComplete: float
    '''

    def sendCompletedTheStep(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Step'}), description=LanguageMap({'en-US':'User Completed Step'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)



    def sendCompletedStep(self, stepId, isComplete, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = stepId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_STEP_VERB, display=LanguageMap({'en-US': COMPLETED_STEP_VERB}))

        if isComplete == None:
            isComplete = 1.0
        isComplete = self.clampToUnitValue(isComplete);
        result = Result(score = isComplete*1.0,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendTerminatedMessage(self, anId, response, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + Exiting, display=LanguageMap({'en-US': Exiting}))
        result = Result(response = response,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendStartMessage(self, anId, response, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + AppStart, display=LanguageMap({'en-US': AppStart}))
        result = Result(response = response,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendResponse(self, anId, score, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + SendResponse, display=LanguageMap({'en-US': SendResponse}))
        result = Result(score = score,)
        
        #self.ActivityTree.EnterActivity(label = "Decision", activity = "User started a new Decision", parentLabel="Session")

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendSelectedItem(self, anId, score, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + ClickedItem, display=LanguageMap({'en-US': ClickedItem}))
        result = Result(score = score,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendLog(self, anId, verb, score, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))
        result = Result(score = score,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send a KC Score about performance on a specific skill during the activity.
        KC scores override any default KC scores inferred from a task's Completed message
        (e.g., which might be assumed that KC's used to recommend the task are also those that
        are assessed by that same task).  Relevance is intended to be used to determine the level
        of confidence for each assessment, and can be left undefined if all scores have high confidence
        and all KC's used to select a task have been assessed by that task.
        Message Data: <userId> | KCScore | <kcName> | <score>
        @param kcName: The name of the knowledge component that was assessed during this task.
        @type kcName: string
        @param score: The score the system gave for this KC, from 0 to 1.
        @type score: float
        @param relevance: The credit or confidence of your assessment of that KC, from 0 (irrelevant) to 1 (strong confidence in this assessment).  Relevance of 0 should be used if a KC that is associated with choosing this task was not encountered during the task. Typically, relevance can be left undefined, which will default to 1.
        @type relevance: float
    '''

    def sendKCScore(self, kcName, score, relevance, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = kcName, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + KC_SCORE_VERB, display=LanguageMap({'en-US': KC_SCORE_VERB}))

        if relevance == None:
            relevance = 1.0
        relevance = self.clampToUnitValue(relevance)
        score = self.clampToUnitValue(score)

        result = Result(score = score,)

        tempContext = {}
        tempContext[KC_RELEVANCE_KEY] = relevance

        context = self.addContext(tempContext)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)

        self.sendLoggingMessage(statement);

    '''
    Send a Mastery score, which is a claim by a system about a user's overall knowledge
        about a knowledge component. This score is expected to be based on all evidence available
        to the system at the time when the KC mastery was calculated.
        Message Data: <userId> | Mastery | <kcName> | <score>
        @param kcName: The name of the knowledge component whose mastery level was estimated.
        @type kcName: string
        @param score: The score the system gave for this KC, from 0 to 1.
        @type score: float
        @param numObservations: A weighted sum for the number of observations that supports this estimate. Some observations might be worth less than one (e.g., because the context was only partly relevant), while other observations might be worth more than one (e.g., because they were received from systems which reported a large number of observations).
        @type numObservations: float
    '''
    def sendMastery(self, kcName, score, numObservations, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = kcName, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + MASTERED_VERB, display=LanguageMap({'en-US': MASTERED_VERB}))

        score = self.clampToUnitValue(score)

        result = Result(score = score,)

        tempContext = {}
        if numObservations != None and numObservations > 0:
            tempContext[NUM_OBSERVATIONS_KEY] = numObservations

        context = self.addContext(tempContext)

        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)

        self.sendLoggingMessage(statement);


    '''
    Notify that a hint was presented
        Message Data: <taskId> | TaskHint | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the hint.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendHint(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(ProcessCoachHint, content, stepId, helpType, contentType, sysComp, description, timestamp)

    '''
    Notify that feedback was presented
        Message Data: <taskId> | TaskFeedback | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the feedback.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''

    def sendFeedback(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(ProcessCoachFeedback, content, stepId, helpType, contentType, sysComp, description, timestamp)

    #Notify that positive feedback was presented
    def sendPositiveFeedback(self, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self.sendFeedback(content, stepId, POSITIVE_HELP_TYPE, contentType, sysComp, description, timestamp)

    #Notify that neutral feedback was presented
    def sendNeutralFeedback(self, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self.sendFeedback(content, stepId, NEUTRAL_HELP_TYPE, contentType, sysComp, description, timestamp)

    #Notify that negative feedback was presented
    def sendNegativeFeedback(self, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self.sendFeedback(content, stepId, NEGATIVE_HELP_TYPE, contentType, sysComp, description, timestamp)

    '''
    Notify that task was decomposed
        Message Data: <taskId> | TaskDecomposition | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner decomposed the task.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''

    def sendTaskDecomposed(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(TASK_DECOMPOSITION_VERB, content, stepId, helpType, contentType, sysComp, description, timestamp)

    '''
    Notify that some other help was presented. In general, this should be used
        only when more specific verbs such as Feedback or Hint are not appropriate.
        Message Data: <userId> | TaskHelp | <stepId> | <score>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the help.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendHelp(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(TASK_HELP_VERB, content, stepId, helpType, contentType, sysComp, description, timestamp)

    '''
    Notify that task presented some content. This can be at any time that
        new content was presented (e.g., moving to a new panel, etc.).
        Message Data: <taskId> | Presented | <elementId> | <content>
        @param elementId: The HTML element where the content was displayed (if relevant)
        @type elementId: string
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the help.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendPresented(self, elementId, content, stepId, contentType, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url+self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + PRESENTED_VERB, display=LanguageMap({'en-US': PRESENTED_VERB}))

        if contentType == None and content != None:
            contentType = 'text'
            content = str(content)

        result = Result(response=content,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        tempContext[RESULT_CONTENT_TYPE_KEY] = contentType

        context = self.addContext(tempContext)

        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Notify that user selected some element (e.g., in terms of HTML: making active)
        This should be used when the user has selected a choice or option, but has not
        necessarily submitted it (e.g., picking a dropdown but before hitting "Submit",
        or writing a text answer before submitting it or clearing it).
        Message Data: <userId> | SelectedOption | <elementId> | <content>
        @param elementId: The HTML element where the option was selected or provided.
        @type elementId: string
        @param content: The content of the selection chosen (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner selected the option.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendSelectedOption(self, elementId, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self._sendInputMessage(SELECTED_OPTION_VERB, elementId, content, stepId, contentType, sysComp, description, timestamp)

    '''
    Notify that user submitted an answer or choice.
        Message Data: <userId> | SubmittedAnswer | <elementId> | <content>
        @param elementId: The HTML element where the option was selected or provided.
        @type elementId: string
        @param content: The content of the submission or choice locked in (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner submitted the value.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendSubmittedAnswer(self, elementId, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self._sendInputMessage(SUBMITTED_ANSWER_VERB, elementId, content, stepId, contentType, sysComp, description, timestamp)

        '''
        Notify that user demonstrated a misconception.
            This requires the misconception ID, rather than the element.
            Message Data: <userId> | SubmittedAnswer | <misconceptionId> | <content>
            @param misconceptionId: An id that uniquely identifies this misconception across a variety of problems.
            @type misconceptionId: string
            @param content: The content of the submission or choice locked in (e.g., the option or value)
            @type: string
            @param stepId: An id that represents the task situation (e.g., decision point) where the learner's misconception was shown. Optional.
            @type stepId: string
            @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
            @type contentType: string
        '''
        def sendMisconception(self, misconceptionId, content, stepId, contentType, sysComp = '', description='', timestamp=None):
            self._sendInputMessage(MISCONCEPTION_VERB, misconceptionId, content, stepId, contentType, sysComp, description, timestamp)

    '''Send the overall level of system support given to the user for this task.
        This is the system's assessment of the level of support that was provided.
        Message Data: <userId> | TaskSupport | <taskId> | <supportLevel>
        @param supportLevel: Fraction of the total support given to the user during the task, in [0,1].
        @type supportLevel: float
    '''
    def sendTaskSupport(self, supportLevel, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url+self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + TASK_SUPPORT_VERB, display=LanguageMap({'en-US': TASK_SUPPORT_VERB}))

        supportLevel = self.clampToUnitValue(supportLevel)
        result = Result(score=supportLevel,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send the overall number of help acts given. To be used when individual hints cannot be logged, but the aggregate can be.
        No need to use this if help actions can be logged individually.
        Message Data: <userId> | TaskHelpCount | <taskId> | <numHelpActs>
        @param numHelpActs: The total number of help acts provided during the task.
        @type numHelpActs: int
    '''
    def sendTaskHelpCount(self, numHelpActs, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url+self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + TASK_HELP_COUNT_VERB, display=LanguageMap({'en-US': TASK_HELP_COUNT_VERB}))

        if numHelpActs < 0:
            numHelpActs = 0

        result = Result(score=numHelpActs,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send the words per second when user was expected to enter content
        Message Data: <userId>, WordsPerSecond, <evidence>, <value>
        @param value: The number of words per second, during times when input was expected.
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'text' : '...', 'duration' : '5.4'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the text input given to this task.
        @type stepId: string
    '''
    def sendWordsPerSecond(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
            if value < 0:
                value = 0
            self._sendMetricMessage(WORDS_PER_SECOND_VERB, value, evidence, stepId, False, sysComp, description, timestamp)

    '''
    Send the actions per second when user was expected to interact with the system
        Message Data: <userId>, ActionsPerSecond, <evidence>, <value>
        @param value: The number of actions per second, during times when input was expected.
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'actions' : ['a1', 'a2'], 'duration' : '5.4'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the actions given to this task.
        @type stepId: string
    '''
    def sendActionsPerSecond(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
            if value < 0:
                value = 0
            self._sendMetricMessage(ACTIONS_PER_SECOND_VERB, value, evidence, stepId, False, sysComp, description, timestamp)

    '''
    Send the semantic match for content submitted. Can be either for a single step (if stepId given)
        or for the whole task (if no stepId given).
        Message Data: <userId>, AnswerSemanticMatch, <evidence>, <value>
        @param value: The semantic match score, in [0,1]
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'match' : 0.6, 'ideal' : 'pen', 'answer' : 'pencil'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the actions given to this task.
        @type stepId: string
    '''
    def sendAnswerSemanticMatch(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(ANSWER_SEMANTIC_MATCH_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendPersistence(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(PERSISTENCE_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendImpetuousness(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(IMPETUOUSNESS_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendGamingTheSystem(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(GAMING_SYSTEM_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendConfusion(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(CONFUSION_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendDisengagement(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(DISENGAGEMENT_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendWheelspinning(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(WHEELSPINNING_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    #ToDo
    def sendRequestRecommendedTasks(self, userName, numberOfRecommendations, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = numberOfRecommendations, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + RECOMMENDED_TASKS_VERB, display=LanguageMap({'en-US': RECOMMENDED_TASKS_VERB}))

        statement = Message(actor, verb, anObject, "", "Request")
        self.sendLoggingMessage(statement)


    '''
    Internal function to notify server that user submitted input
        @param verb: The verb to use for the user input message
        @type verb: string
        @param elementId: The HTML element where the user performed the interaction.
        @type elementId: string
        @param content: The content of the selection chosen (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner selected the option. Optional.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def _sendInputMessage(self, verb, elementId, content, stepId, contentType, sysComp, description, timestamp):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = elementId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))

        if contentType == None and content != None:
            contentType = 'text'
            content = str(content)

        result = Result(response=content,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        tempContext[RESULT_CONTENT_TYPE_KEY] = contentType

        context = self.addContext(tempContext)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    '''
    Internal Function to notify server that some help message was presented
        @param verb: The verb to use for the help log message
        @type verb: string
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the hint. Optional.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, a prompt, etc. Optional.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML). Defaults to text.
        @type contentType: string
    '''
    def _sendHelpMessage(self, verb, content, stepId, helpType, contentType, sysComp, description, timestamp):
        if (contentType == None) and content != None:
            contentType = 'text'
            content = str(content)
        if helpType == None:
            helpType = NEUTRAL_HELP_TYPE

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = stepId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))
        result = Result(response=content,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        tempContext[HELP_TYPE_KEY] = helpType
        tempContext[RESULT_CONTENT_TYPE_KEY] = contentType

        context = self.addContext(tempContext)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Internal function for sending metric values
        @param verb: The verb to use for the metric message
        @type verb: string
        @param value: Value of the metric to send.
        @type value: numeric
        @param stepId: The stepId that the metric applies to. If None, applies to the task overall.
        @type stepId: string
        @param clampToUnit: If true, adjust value to fit between 0 and 1. Null values are not changed.
        @type clampToUnit: bool
    '''
    def _sendMetricMessage(self, verb, value, evidence,  stepId, clampToUnit, sysComp, description, timestamp):
        if evidence == None:
            evidence = []
        if clampToUnit:
            value = self.clampToUnitValue(value)

        actor = Agent( object_type = 'Agent', openid = self ._userId)
        anObject = Activity( id = evidence, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))
        result = Result(response=value,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId

        context = self.addContext(tempContext)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Add context to the message.  This adds the userId, taskId, classroomId,
        activityType, and duration so far. It also adds any service context items,
        followed by the parameter context. Context within the context parameter does
        not override any existing message context.
        @param msg: The original message to modify by adding context data.
        @type msg: Messaging.Message
        @param context: Dictionary of key-value items to add to the message context. Not used if keys already exist.
        @type context: object
        @return: Modified message in msg
        @rtype: Messaging.Message
    '''

    def addContext(self, parentLabel  = "Session"):

        tempContext = {}
        tempContext[USER_ID_KEY] = self._userId
        tempContext[TASK_ID_KEY] = self._taskId
        tempContext[CLASSROOM_ID_KEY] = self._classroomId
        tempContext[ACTIVITY_TYPE_KEY] = self._activityType
        tempContext[DURATION_KEY] = self.calcDuration()
        
       #constructing a parent dicitonary to pass to Activity List class , so that it's converted to tincan.ActivityList and then passed to parent argument in the ContextActivities
        parentDict = {
                "id": "http://www.abcya.com/" + parentLabel,
                "definition": {
                    "name": {
                        "en-US": parentLabel
                    },
                }
            }
        
        
        
        agentAccount = AgentAccount(name = "dummyName", home_page="http://dummyHomepage.com")
        
        context = Context(
        registration=str(uuid.uuid4()),
        instructor=Agent(
            account=agentAccount
            ), 
        #extensions = Extensions(tempContext),
        context_activities = ContextActivities(parent = ActivityList([parentDict]))#, parent = parent)
        # language='en-US',
        )        

       # for key in context:
       #     if not self.hasContextValue(key):
       #         tempContext[key] = context[key]
       # for key in self._context:
       #     if not self.hasContextValue(key):
       #         tempContext[key] = context[key]
       # context = Context( extensions = tempContext)
        return context

    '''
    Finalize any post-processing of the message and then send it
        @param msg: Message to send
        @type msg: Messaging.Message
        @param context: Dictionary of key-value items to add to the message context. Not used if keys already exist.
        @type context: object
    '''
    # send message to json file (to-do: connecting to learn locker)
    def sendLoggingMessage(self, statement):
        message = Message(actor="logger", verb=XAPI_LOG_VERB, obj=None, result=statement.to_json())
        self.sendMessage(message)

    # values to fit within a [0,1] range
    def clampToUnitValue(self, val):
        if val != None:
            return min(max(val, 0.0), 1.0)
        return val
