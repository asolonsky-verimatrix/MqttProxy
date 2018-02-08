import sys
import os
import argparse
import time
import datetime
import paho.mqtt.client as mqtt
import Queue
import random

def OnConnect(client, userdata, flags, rc):
  return
  #print("Connected with result code "+str(rc))

def OnMessage(client, userdata, msg):
  Temp = msg.topic+" "+str(msg.payload)
  #print(Temp)
  userdata.put(msg.payload)
  

def SendMqttMessage(User, Pwd, PubTopic, PubMsg, SubTopic, Timeout):
  
  SubMsgQ = Queue.Queue()
  
  Client = mqtt.Client()
  Client.tls_set('/etc/ssl/certs/DST_Root_CA_X3.pem')
  Client.username_pw_set(User,Pwd)
  Client.user_data_set(SubMsgQ)
  Client.on_connect = OnConnect
  Client.on_message = OnMessage

  Client.connect("mqtt.complianceblockchain.org", 8883, 60)
  Client.loop_start()
  #print "subscribing "
  Client.subscribe(SubTopic)
  time.sleep(1)
  #print"publishing: " + PubTopic + " : " + PubMsg
  Client.publish(PubTopic, PubMsg)
  
  TimeCount = 0
  while (TimeCount < Timeout):
    TimeCount = TimeCount + 1
    if (SubMsgQ.qsize() > 0):
      break;
    time.sleep(1)
    
  Client.disconnect()
  Client.loop_stop()
  if (SubMsgQ.qsize() > 0):
    return SubMsgQ.get()
  else:
    return ""
 

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument("--u", help="User Name")
  parser.add_argument("--p", help="Password")
  parser.add_argument("--gwid", help="GatewayId")
  parser.add_argument("--rw", help="Read/Write")
  parser.add_argument("--contract", help="Contract Name")
  parser.add_argument("--func", help="Function Name")
  parser.add_argument("--param", help="Parameter List '[1,2,3]'")
  parser.add_argument("--timeout", help="Timeout in seconds")
  args = parser.parse_args()
  User = args.u;
  Pwd = args.p;
  GatewayId = args.gwid;
  Cmd = args.rw;
  Contract = args.contract;
  Func = args.func;
  Param = args.param;
  Timeout = int(args.timeout);
  
  SeqNum = random.randint(1,64000);
  
  PubTopic = User+"/"+GatewayId+"/Us/Cmd";
  SubTopic = User+"/"+GatewayId+"/Us/Rsp";
  PubMsg = '{"SeqNum":'+str(SeqNum)+', "Cmd":"'+Cmd+'", "Contract":"'+Contract+'", "Function":"'+Func+'", "Parameters":' + Param + '}';

  print ("*******************************************************************************************")
  print ((datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + " " + PubTopic)
  print ("*******************************************************************************************")
  print "<<<<< " + PubMsg + "\n";
  SubMsg = SendMqttMessage(User, Pwd, PubTopic, PubMsg, SubTopic, Timeout)
  print ">>>>> " + SubMsg + "\n";
    
  
if __name__ == "__main__":
  main(sys.argv)
