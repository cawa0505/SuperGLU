package Core;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Predicate;
import java.util.logging.Level;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;

import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

/**
 * This class will send and receive messages over SocketIO.
 * It's basically a bridge between the SuperGLU infrastructure and the SocketIO framework.
 * @author auerbach
 *
 */

public class HTTPMessagingGateway extends MessagingGateway implements DataListener<Map<String, String>>
{
    
    /**
     * This is the object that handles the communication over the socket.
     */
    private SocketIOServer socketIO;
    
    
    /**
     * store the clients in association with the persistent session id.
     * 
     */
    private ConcurrentHashMap<String, List<String>> clients; 
    
    public static final String MESSAGES_KEY = "message";
    public static final String DATA_KEY = "data";
    public static final String MESSAGES_NAMESPACE = "/messaging";
    
    
    public HTTPMessagingGateway()
    {
	super();
	this.socketIO = new SocketIOServer(new Configuration());
	this.clients = new ConcurrentHashMap<>();
    }
    
    
    public HTTPMessagingGateway(String anId, MessagingGateway gateway, Map<String, Object> scope, Collection<BaseMessagingNode> nodes, Predicate<BaseMessage> conditions, SocketIOServer socketIO)
    {
	super(anId, gateway, scope, nodes, conditions);
	this.socketIO = socketIO;
	this.clients = new ConcurrentHashMap<>();
	
	this.socketIO.addEventListener(MESSAGES_NAMESPACE, Map.class, (DataListener)this);
    }
    

    @Override
    public void receiveMessage(BaseMessage msg)
    {
	super.receiveMessage(msg);
	log.log(Level.INFO, "message received");
	this.sendAJAXMesage(msg);
	log.log(Level.INFO, "Distributing message: " + SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
	this.distributeMessage(msg, this.getId());
	log.log(Level.INFO, "message distributed");
    }

    @Override
    public void sendMessage(BaseMessage msg)
    {
	// TODO Auto-generated method stub
	super.sendMessage(msg);
    }
    
    
    public void sendAJAXMesage(BaseMessage msg)
    {
	
    }
    


    @Override
    public void onData(SocketIOClient client, Map<String, String> data, AckRequest ackSender) throws Exception
    {
	String sid = client.getSessionId().toString();
            
	if(data.containsKey(DATA_KEY))
	{
	    String sessionId = data.getOrDefault(SESSION_KEY, null);
	    if(SESSION_KEY != null)
	    {
		client.joinRoom(sessionId);
		
		if(!this.clients.containsKey(sessionId))
		    this.clients.put(sessionId, new ArrayList<>());
		
		List<String> sids = new ArrayList<>();
		sids.add(sid);
		this.clients.put(sessionId, sids);
		
		String msgAsString = data.get(DATA_KEY);
		BaseMessage msg = (BaseMessage) SerializationConvenience.nativeizeObject(msgAsString, SerializationFormatEnum.JSON_FORMAT);
		
		if(this.gateway != null)
		    this.gateway.dispatchMessage(msg, this.getId());
		
		this.distributeMessage(msg, this.getId());
	    }
	}
	else
	{
	    log.log(Level.WARNING, "GATEWAY DID NOT UNDERSTAND: " + data.toString());
	}
	
    }

}
