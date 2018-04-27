package edu.usc.ict.superglu.core;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.core.config.GatewayBlackWhiteListConfiguration;
import edu.usc.ict.superglu.core.config.GatewayConfiguration;
import edu.usc.ict.superglu.ontology.OntologyBroker;
import edu.usc.ict.superglu.ontology.mappings.MessageMapFactory;
import edu.usc.ict.superglu.ontology.mappings.MessageType;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

/**
 * Messaging Node specifically designed to act as a entry/exit point between
 * systems.
 *
 * @author auerbach
 */

public class BaseMessagingGateway extends BaseMessagingNode {

    public static final String GATEWAY_BLACKLIST_KEY = "gatewayBlackList";
    public static final String GATEWAY_WHITELIST_KEY = "gatewayWhiteList";

    private Map<String, Object> scope;
    protected Map<String, BaseMessagingNode> nodes;
    private OntologyBroker ontologyBroker;

    protected Map<String, List<BlackWhiteListEntry>> gatewayBlackList;

    protected Map<String, List<BlackWhiteListEntry>> gatewayWhiteList;

    public BaseMessagingGateway() {// Default constructor for ease of access
        this(null, null, null, null, null, new GatewayConfiguration());
        ontologyBroker = new OntologyBroker(MessageMapFactory.buildMessageMaps(),
                MessageMapFactory.buildDefaultMessageTemplates());
    }

    public BaseMessagingGateway(String anId, Map<String, Object> scope, Collection<BaseMessagingNode> nodes,
                                Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers, GatewayConfiguration config) {
        super(anId, conditions, handlers, config.getBlackList(), config.getWhiteList());
        if (scope == null)
            this.scope = new HashMap<>();
        else
            this.scope = scope;

        this.scope.put(ORIGINATING_SERVICE_ID_KEY, this.id);

        this.nodes = new HashMap<>();
        this.addNodes(nodes);

        ontologyBroker = new OntologyBroker(MessageMapFactory.buildMessageMaps(),
                MessageMapFactory.buildDefaultMessageTemplates());

        this.gatewayBlackList = buildGatewayBlackWhiteList((GatewayBlackWhiteListConfiguration) config.getParams().getOrDefault(GATEWAY_BLACKLIST_KEY, null));
        this.gatewayWhiteList = buildGatewayBlackWhiteList((GatewayBlackWhiteListConfiguration) config.getParams().getOrDefault(GATEWAY_WHITELIST_KEY, null));
    }


    private Map<String, List<BlackWhiteListEntry>> buildGatewayBlackWhiteList(GatewayBlackWhiteListConfiguration config) {
        Map<String, List<BlackWhiteListEntry>> result = new HashMap<>();

        if (config == null)
            return result;

        for (String destination : config.getKeys()) {
            List<String> entriesAsString = config.getMessageList(destination);

            List<BlackWhiteListEntry> entries = new ArrayList<>();

            for (String entryAsString : entriesAsString) {
                BlackWhiteListEntry entry = new BlackWhiteListEntry(entryAsString);
                entries.add(entry);
            }

            result.put(destination, entries);
        }

        return result;
    }


    /**
     * override this function to place disconnection code in here
     **/
    public void disconnect() {

    }

    /**
     * When gateway receives a message, it distributes it to child nodes
     */
    @Override
    public boolean receiveMessage(BaseMessage msg) {
        if (super.receiveMessage(msg)) {
            String senderId = (String) msg.getContextValue(ORIGINATING_SERVICE_ID_KEY);
            this.distributeMessage(msg, senderId);
            return true;
        }
        return false;
    }


    protected boolean isMessageOnDestinationList(List<BlackWhiteListEntry> entries, BaseMessage msg) {
        if (entries != null) {
            for (BlackWhiteListEntry entry : entries) {
                if (entry.evaluateMessage(msg))
                    return true;
            }
        }

        return false;
    }


    @Override
    protected boolean isMessageOnGatewayBlackList(BaseMessagingNode destination, BaseMessage msg) {
        String destinationID = destination.getId();
        List<BlackWhiteListEntry> entries = this.gatewayBlackList.getOrDefault(destinationID, null);

        boolean result = isMessageOnDestinationList(entries, msg);

        List<BlackWhiteListEntry> allDestinationEntries = this.gatewayBlackList.getOrDefault(GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS, null);

        result = result || isMessageOnDestinationList(allDestinationEntries, msg);

        return result;

    }


    @Override
    protected boolean isMessageOnGatewayWhiteList(BaseMessagingNode destination, BaseMessage msg) {

        if (this.gatewayWhiteList.isEmpty())
            return true;

        String destinationID = destination.getId();
        List<BlackWhiteListEntry> entries = this.gatewayWhiteList.getOrDefault(destinationID, null);

        boolean result = isMessageOnDestinationList(entries, msg);

        List<BlackWhiteListEntry> allDestinationEntries = this.gatewayWhiteList.getOrDefault(GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS, null);

        result = result || isMessageOnDestinationList(allDestinationEntries, msg);

        return result;


    }

    protected boolean isMessageOnGatewayExternalBlackList(BaseMessage msg) {
        if (!USE_BLACK_WHITE_LIST)
            return false;

        List<BlackWhiteListEntry> externalEntries = this.gatewayBlackList.getOrDefault(GatewayBlackWhiteListConfiguration.EXTERNAL_DESTINATIONS, null);
        boolean result = isMessageOnDestinationList(externalEntries, msg);
        List<BlackWhiteListEntry> allEntries = this.gatewayBlackList.getOrDefault(GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS, null);
        result = result || isMessageOnDestinationList(allEntries, msg);

        return result;
    }


    protected boolean isMessageOnGatewayExternalWhiteList(BaseMessage msg) {
        if (!USE_BLACK_WHITE_LIST)
            return true;

        if (this.gatewayWhiteList.isEmpty())
            return true;

        List<BlackWhiteListEntry> externalEntries = this.gatewayWhiteList.getOrDefault(GatewayBlackWhiteListConfiguration.EXTERNAL_DESTINATIONS, null);
        boolean result = isMessageOnDestinationList(externalEntries, msg);
        List<BlackWhiteListEntry> allEntries = this.gatewayWhiteList.getOrDefault(GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS, null);
        result = result || isMessageOnDestinationList(allEntries, msg);

        return result;
    }

    /**
     * """ Send a message from a child node to parent and sibling nodes """
     *
     * @param msg      Message to be sent
     * @param senderId Sender ID
     */
    public void distributeMessage(BaseMessage msg, String senderId) {
        this.addContextDataToMsg(msg);
        for (BaseMessagingNode node : nodes.values()) {
            if (!isMessageOnGatewayBlackList(node, msg) && isMessageOnGatewayWhiteList(node, msg))
                if (node.id != senderId && (node.getMessageConditions() == null || node.getMessageConditions().test(msg)))
                    node.receiveMessage(msg);
        }
    }


    /**
     * """ Register the signatures of messages that the node is interested in "
     * ""
     *
     * @param node
     */
    public void register(BaseMessagingNode node) {
        this.nodes.put(node.id, node);
    }

    /**
     * """ Take actions to remove the node from the list """
     *
     * @param node
     */
    public void unregister(BaseMessagingNode node) {
        if (this.nodes.containsKey(node.id))
            this.nodes.remove(node.id);
    }

    /**
     * """ Add extra context to the message, if not present """
     *
     * @param msg
     */
    public void addContextDataToMsg(BaseMessage msg) {
        for (String key : this.scope.keySet()) {
            if (!msg.hasContextValue(key))
                msg.setContextValue(key, this.scope.get(key));
        }
    }


    /* Node Management */

    /**
     * Connect nodes to this node
     **/
    public void addNodes(Collection<BaseMessagingNode> newNodes) {
        if (newNodes != null) {
            for (BaseMessagingNode node : newNodes) {
                addNode(node);
            }
        }
    }

    public void addNode(BaseMessagingNode node) {
        this.onBindToNode(node);
    }

    public Collection<BaseMessagingNode> getNodes() {
        return this.nodes.values();
    }

    /**
     * Register the node and signatures of messages that the node is interested
     * in
     **/
    public void onBindToNode(BaseMessagingNode node) {
        if (!this.nodes.containsKey(node.getId())) {
            this.nodes.put(node.getId(), node);
        }
    }

    /**
     * This removes this node from a connected node (if any)
     **/
    public void onUnbindToNode(BaseMessagingNode node) {
        if (this.nodes.containsKey(node.getId())) {
            this.nodes.remove(node.getId());
        }
    }

    /**
     * This function will process a non-SuperGLU message through the ontology
     * converter
     */
    public BaseMessage convertMessages(BaseMessage incomingMessage, Class<?> destinationMessageType) {
        String incomingMessageTypeAsString = incomingMessage.getClassId();

        String messageName = "";

        if (incomingMessage instanceof Message)
            messageName = ((Message) incomingMessage).getVerb();
        else if (incomingMessage instanceof VHMessage)
            messageName = ((VHMessage) incomingMessage).getFirstWord();
        else if (incomingMessage instanceof GIFTMessage)
            messageName = ((GIFTMessage) incomingMessage).getHeader();

        MessageType inMsgType = ontologyBroker.buildMessageType(incomingMessageTypeAsString, messageName, 1.0f, 1.0f);
        MessageType outMsgType = ontologyBroker.buildMessageType(destinationMessageType.getSimpleName(), "", 1.0f,
                1.0f);

        BaseMessage result = ontologyBroker.findPathAndConvertMessage(incomingMessage, inMsgType, outMsgType,
                this.context, true);

        return result;
    }
}
