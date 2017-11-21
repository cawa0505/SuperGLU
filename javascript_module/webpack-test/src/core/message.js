const Zet = require('../util/zet')
const Serializable = require('../util/serializable')
const tokenizeObject = tokenizeObject
const untokenizeObject = untokenizeObject

module.exports = Zet.declare({
    superclass: Serializable,
    CLASS_ID: 'Message',
    defineBody: function (self) {
        // Private Properties

        // Public Properties

        /** Create a Message
         @param actor: The actor who did or would do the given action
         @param verb: Some action that was or would be done by the actor
         @param obj: An object or target for the action
         @param result: The outcome of the action
         @param speechAct: A performative, stating why this message was sent
         @param context: A context object for the message, with additional data
         @param timestamp: A timestamp for when the message was created
         @param anId: A unique Id.  If none given, one will be assigned.
         **/
        self.construct = function construct(actor, verb, obj, result, speechAct,
                                            context, timestamp, anId) {
            self.inherited(construct, [anId])
            if (typeof actor === "undefined") {
                actor = null
            }
            if (typeof verb === "undefined") {
                verb = null
            }
            if (typeof obj === "undefined") {
                obj = null
            }
            if (typeof result === "undefined") {
                result = null
            }
            if (typeof speechAct === "undefined") {
                speechAct = INFORM_ACT
            }
            if (typeof context === "undefined") {
                context = {}
            }
            if (typeof timestamp === "undefined") {
                timestamp = null
            }
            self._actor = actor
            self._verb = verb
            self._obj = obj
            self._result = result
            self._speechAct = speechAct
            self._timestamp = timestamp
            if (self._timestamp == null) {
                self.updateTimestamp()
            }
            // Fill in version keys
            if (!(MESSAGE_VERSION_KEY in context)) {
                context[MESSAGE_VERSION_KEY] = VERSION
            }
            if (!(SUPERGLU_VERSION_KEY in context)) {
                context[SUPERGLU_VERSION_KEY] = SUPERGLU_VERSION
            }
            self._context = context
        }

        /** Get the actor for the message **/
        self.getActor = function getActor() {
            return self._actor
        }
        /** Set the actor for the message **/
        self.setActor = function setActor(value) {
            self._actor = value
        }

        /** Get the verb for the message **/
        self.getVerb = function getVerb() {
            return self._verb
        }
        /** Set the verb for the message **/
        self.setVerb = function setVerb(value) {
            self._verb = value
        }

        /** Get the object for the message **/
        self.getObject = function getObject() {
            return self._obj
        }
        /** Set the object for the message **/
        self.setObject = function setObject(value) {
            self._obj = value
        }

        /** Get the result for the message **/
        self.getResult = function getResult() {
            return self._result
        }
        /** Set the result for the message **/
        self.setResult = function setResult(value) {
            self._result = value
        }

        /** Get the speech act for the message **/
        self.getSpeechAct = function getSpeechAct() {
            return self._speechAct
        }
        /** Set the speech act for the message **/
        self.setSpeechAct = function setSpeechAct(value) {
            self._speechAct = value
        }

        /** Get the timestamp for the message (as an ISO-format string)**/
        self.getTimestamp = function getTimestamp() {
            return self._timestamp
        }
        /** Set the timestamp for the message (as an ISO-format string) **/
        self.setTimestamp = function setTimestamp(value) {
            self._timestamp = value
        }
        /** Update the timestamp to the current time **/
        self.updateTimestamp = function updateTimestamp() {
            self._timestamp = new Date().toISOString()
        }

        /** Check if the context field has a given key **/
        self.hasContextValue = function hasContextValue(key) {
            return (key in self._context) === true
        }

        /** Get all the keys for the context object **/
        self.getContextKeys = function getContextKeys() {
            var key, keys
            keys = []
            for (key in self._context) {
                keys.push(key)
            }
            return keys
        }

        /** Get the context value with the given key. If missing, return the default. **/
        self.getContextValue = function getContextValue(key, aDefault) {
            if (!(key in self._context)) {
                return aDefault
            }
            return self._context[key]
        }

        /** Set a context value with the given key-value pair **/
        self.setContextValue = function setContextValue(key, value) {
            self._context[key] = value
        }

        /** Delete the given key from the context **/
        self.delContextValue = function delContextValue(key) {
            delete self._context[key]
        }

        /** Save the message to a storage token **/
        self.saveToToken = function saveToToken() {
            var key, token, newContext, hadKey
            token = self.inherited(saveToToken)
            if (self._actor != null) {
                token.setitem(ACTOR_KEY, tokenizeObject(self._actor))
            }
            if (self._verb != null) {
                token.setitem(VERB_KEY, tokenizeObject(self._verb))
            }
            if (self._obj != null) {
                token.setitem(OBJECT_KEY, tokenizeObject(self._obj))
            }
            if (self._result != null) {
                token.setitem(RESULT_KEY, tokenizeObject(self._result))
            }
            if (self._speechAct != null) {
                token.setitem(SPEECH_ACT_KEY, tokenizeObject(self._speechAct))
            }
            if (self._timestamp != null) {
                token.setitem(TIMESTAMP_KEY, tokenizeObject(self._timestamp))
            }
            hadKey = false
            newContext = {}
            for (key in self._context) {
                hadKey = true
                newContext[tokenizeObject(key)] = tokenizeObject(self._context[key])
            }
            if (hadKey) {
                token.setitem(CONTEXT_KEY, tokenizeObject(newContext))
            }
            return token
        }

        /** Initialize the message from a storage token and some additional context (e.g., local objects) **/
        self.initializeFromToken = function initializeFromToken(token, context) {
            self.inherited(initializeFromToken, [token, context])
            self._actor = untokenizeObject(token.getitem(ACTOR_KEY, true, null), context)
            self._verb = untokenizeObject(token.getitem(VERB_KEY, true, null), context)
            self._obj = untokenizeObject(token.getitem(OBJECT_KEY, true, null), context)
            self._result = untokenizeObject(token.getitem(RESULT_KEY, true, null), context)
            self._speechAct = untokenizeObject(token.getitem(SPEECH_ACT_KEY, true, null), context)
            self._timestamp = untokenizeObject(token.getitem(TIMESTAMP_KEY, true, null), context)
            self._context = untokenizeObject(token.getitem(CONTEXT_KEY, true, {}), context)
        }
    }
})