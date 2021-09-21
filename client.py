from __future__ import print_function
from is_wire.core import Channel, Message, Subscription,StatusCode, Status, Logger
import time
from is_wire.rpc import ServiceProvider, LogInterceptor
from random import randint
from RequisicaoRobo_pb2 import RequisicaoRobo
import socket
from is_msgs import common_pb2
from is_msgs.robot_pb2 import RobotTaskRequest
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import Position

channel = Channel("amqp://guest:guest@localhost:5672")


#Primeira parte do trabalho-------------------------------------------------------------------------------------------------
while True:
	#Pub
	MessageText = "Ligar sistema"
	msg = Message()
	msg.body = MessageText.encode('utf-8')
	channel.publish(msg, topic = "Controle.Console")
	
	#Sub
	subscription = Subscription(channel)
	subscription.subscribe(topic = "Controle.Console")
	msg = channel.consume()
	print(msg.body.decode('utf-8'))
	
	if msg.body.decode('utf-8') == "LIGADO":
		break
	time.sleep(1)	



while True:
	time.sleep(5)
	RoboReq = RequisicaoRobo()
	RoboReq.id = 3
	
	f = randint(0,1)
	
	if f == 0:#GET POSITION
		RoboReq.function = "get"
	else:#SET POSITION
		RoboReq.function = "set"
		RoboReq.positions.x = randint(1,10)
		RoboReq.positions.y = randint(1,10)
		RoboReq.positions.z = randint(1,10)

	subscription = Subscription(channel)
	rmsg = Message(content = RoboReq, reply_to = subscription)
	channel.publish(rmsg, topic = "Requisicao.Robo")	
	try:
		rep = channel.consume(timeout = 2.0)
		RobotReturn = rep.unpack(RequisicaoRobo)
		print(RobotReturn.id)
		if f == 0:#GET POSITION
			txt = "GET POSITION | Id: {} | Positions:({}, {}, {})"
			print(txt.format(RobotReturn.id, RobotReturn.positions.x, RobotReturn.positions.y, RobotReturn.positions.z))
		else: #SET POSITION
			txt = "SET POSITION | Id: {} | Positions:({}, {}, {})"
			print(txt.format(RoboReq.id, RoboReq.positions.x, RoboReq.positions.y, RoboReq.positions.z))
	except socket.timeout:
		print('No reply')
	
	
	
	
	
	
	
	
	
	
