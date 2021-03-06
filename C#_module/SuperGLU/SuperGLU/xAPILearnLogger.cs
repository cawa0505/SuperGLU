﻿using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Collections.Generic;
using TinCan;

namespace SuperGLU
{
    public class xAPILearnLogger: BaseLearnLogger
    {
        string mbox = "mailto:SMART-E@ict.usc.edu";
        string activityURI = "http://id.tincanapi.com/activity/";

        ActivityTree activityTree;


        RemoteLRS remoteLRS;

        /* ---------------- constructor, getter and setter --------------- */
        public xAPILearnLogger(string userId = "", string userName = ""): base()
        {
            this.activityTree = new ActivityTree();
            this.userId = userId;
            this.userName = userName;
            this.mbox = "mailto:" + userId + "@ict.usc.edu";
            this.url = new Uri("https://github.com/GeneralizedLearningUtilities/SuperGLU/");

            remoteLRS = new RemoteLRS("http://ictsmarte.org/data/xAPI", "e181f39b3cbb6b1f1c08a2c5fc59ccda617c2212", "3ba7fd269e3bc03234a3ce77861c76c7fa6b142e");
        }

        public void SetUserId(string userId)
        {
            this.userId = userId;
        }

        public void SetUserName(string userName)
        {
            this.userName = userName;
        }

        /* ---------------------- create xAPI object ---------------------- */
        // create actor
        private Agent CreateActor(string name, string openid, string mbox)
        {
            Agent actor = new Agent();
            actor.name = name;
            actor.openid = openid;
            actor.mbox = mbox;

            return actor;
        }

        // create agent account, used as an instructor agent in context
        private AgentAccount CreateAgentAccount(string name, string homePage)
        {
            AgentAccount agentAccount = new AgentAccount();
            agentAccount.name = name;
            agentAccount.homePage = new Uri(homePage);

            return agentAccount;
        }

        // create verb
        private Verb CreateCompletedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/complete");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "completed");

            return verb;
        }

        private Verb CreateStartedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/start");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "started");

            return verb;
        }

        private Verb CreateTerminiatedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/terminate");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "terminated");

            return verb;
        }

        private Verb CreatePresentedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/present");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "presented");

            return verb;
        }


        private Verb CreateWatchedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/watch");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "watched");

            return verb;

        }

        // create activity
        private Activity CreateSession(string activityId, string name, string description)
        {
            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>(){ { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/tutor-session");

            return activity;
        }

        private Activity CreateTopic(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/topic");

            return activity;
        }

        private Activity CreateLesson(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/lesson");

            return activity;
        }

        private Activity CreateSublesson(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/sublesson");

            return activity;
        }

        private Activity CreateTask(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/task");

            return activity;
        }

        private Activity CreateStep(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/step");

            return activity;
        }

        private Activity CreateVideo(string activityId= "http://activitystrea.ms/schema/1.0/video", string name= "video", string description= "Video content of any kind")
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/video");

            return activity;
        }

        // TODO: activity tree class need to be implemented
        private Activity CreateActivityTree(string activityId = "http://activitystrea.ms/schema/1.0/activityTree", string name = "activityTree", string description = "Activity tree (not implemented yet)")
        {
            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/activityTree");

            return activity;
        }

        // create result
        private Result CreateResult(string response = "", bool? success = null)
        {
            Result result = new Result();
            if (response != "")
            {
                result.response = response;
            }
            if (success != null)
            {
                result.success = success;
            }

            return result;
        }

        // create context
        private Context CreateContext(JObject contextJson)
        {   
            // instructor agent
            AgentAccount agentAccount = CreateAgentAccount("instructorAgent", "http://instructorHomepage.com");

            Context context = new Context();
            context.registration = Guid.NewGuid();   // globally unique indentifier
            context.instructor = new Agent(new JObject { { "account", agentAccount.ToJObject()} });
            context.extensions = new TinCan.Extensions(contextJson);    // 'Extensions' is ambiguous reference between 'Newtonsoft.Json' and 'TinCan'
            context.contextActivities = new ContextActivities();
            context.contextActivities.grouping = this.activityTree.convertPathToGrouping();
            List<Activity> parent = new List<Activity>();
            if(this.activityTree.findParentActivity() != null)
                parent.Add(this.activityTree.findParentActivity());
            context.contextActivities.parent = parent;

            return context;
        }

        /* ------------------- construct xAPI statement ------------------- */
        // start
        public void SendStartSession(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateSession(activityId, name, description);

            activityTree.enterActivity(null, activity, null);

            Result result = CreateResult(response: "User started a new Session");
            Context context = CreateContext(contextJson);

            

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartLesson(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateLesson(activityId, name, description);

            activityTree.enterActivity(null, activity, null);

            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);


            

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartSublesson(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateSublesson(activityId, name, description);

            activityTree.enterActivity(null, activity, null);

            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

            

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartTask(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateTask(activityId, name, description);
            activityTree.enterActivity(null, activity, null);


            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

            

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartStep(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateStep(activityId, name, description);

            activityTree.enterActivity(null, activity, null);

            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

           

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        // terminiate or complete
        public void SendTerminiatedSession(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateTerminiatedVerb();
            Activity activity = this.activityTree.findCurrentActivity();
            Result result = CreateResult();

            this.activityTree.exitActivity(null);

            Context context = CreateContext(contextJson);


            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            
            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendCompletedLesson(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = this.activityTree.findCurrentActivity();
            Result result = CreateResult();

            activityTree.exitActivity(activity);

            Context context = CreateContext(contextJson);


            

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendCompletedSublesson(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = this.activityTree.findCurrentActivity();
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            this.activityTree.exitActivity(activity);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendCompletedTask(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = this.activityTree.findCurrentActivity();
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            this.activityTree.exitActivity(activity);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        /* work in progress. currently requires custom_score_URI and custom_score but not all applications will have this.
           If a raw_score is provided then a max_score must be provided too.
           Might want to provide more detailed information relating to the knowledge components involved in the step.
        */
        public void SendCompletedStep(string choice, string customScoreURI, double customScore, JObject contextJson, double rawScore = -1, double maxScore = -1, double minScore = 0, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = this.activityTree.findCurrentActivity();
            Result result = new Result();
            Context context = CreateContext(contextJson);
            TinCan.Extensions extensions = new TinCan.Extensions(new JObject { {customScoreURI, customScore} });

            // handle different result
            if (rawScore != -1)
            {
                result.response = choice;
                result.score = new Score(new JObject { { "raw", rawScore }, { "min", minScore }, {"max", maxScore} });
                result.extensions = extensions;
            } else
            {
                result.response = choice;
                result.extensions = extensions;
            }

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }


        public void SendWatchedVideo(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateWatchedVerb();
            Activity activity = CreateVideo(); 
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        private void SendLoggingMessage(Statement statement)
        {
            //send to learnlocker
            this.remoteLRS.SaveStatement(statement);
            Console.Out.WriteLine("sent statement");
            string path = Directory.GetCurrentDirectory();
            // write to log file
            using (System.IO.StreamWriter logFile =
                new System.IO.StreamWriter(path + "\\xAPILog.json", true))
                {
                    logFile.WriteLine(statement.ToJSON());
                }
        }
    }

   

}
