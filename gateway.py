from __future__ import print_function
from is_wire.core import Channel, Subscription, Message,StatusCode, Status, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor
import time
from random import randint
from RequisicaoRobo_pb2 import RequisicaoRobo
from is_msgs.robot_pb2 import RobotTaskRequest
import socket
from is_msgs.common_pb2 import Position
from google.protobuf.empty_pb2 import Empty
from is_msgs import common_pb2

channel = Channel("amqp://guest:guest@localhost:5672")
#subscription = Subscription(channel)
#subscription.subscribe(topic="Controle.Console")



def RobotGateway(Robot_info, ctx):
	RobTasReq = RobotTaskRequest()
	if Robot_info.function == "get": #GET POSITION-------------------------------------------
		RobTasReq.id = Robot_info.id
		subscription = Subscription(channel)
		MsgRobTasReq = Message(content = RobTasReq, reply_to = subscription)
		channel.publish(MsgRobTasReq, topic = "Requisicao.Get_position")
		try:
			ReplyRobot = channel.consume(timeout = 1.0)
			RobotUnpack = ReplyRobot.unpack(RobotTaskRequest)
			Robot_info.positions.x = RobotUnpack.basic_move_task.positions[0].x
			Robot_info.positions.y = RobotUnpack.basic_move_task.positions[0].y
			Robot_info.positions.z = RobotUnpack.basic_move_task.positions[0].z
			return Robot_info
		except socket.timeout:
			print('No reply')
			
			
			
	elif Robot_info.function == "set":#SET POSITION-------------------------------------------
		RobTasReq.id = Robot_info.id
		RobTasReq.basic_move_task.positions.extend([Position(x = Robot_info.positions.x, y = Robot_info.positions.y, z = Robot_info.positions.z)])
		subscription = Subscription(channel)
		MsgRobTasReq = Message(content = RobTasReq, reply_to = subscription)
		channel.publish(MsgRobTasReq, topic = "Requisicao.Set_position")
		try:
			ReplyRobot = channel.consume(timeout = 1.0)
			return Status(ReplyRobot.status.code, why = ReplyRobot.status.why)
		except socket.timeout:
			print('No reply')


#Primeira parte do trabalho--------------------------------------------------------------------------------------------
while True: 
	subscription = Subscription(channel)
	subscription.subscribe(topic="Controle.Console")
	RecMsg = channel.consume()
	RecStr = RecMsg.body.decode('utf-8')
	time.sleep(1)
	if RecStr == "Ligar sistema":
		rand = randint(0, 1)
		if rand == 0:
			MessageText = "LIGADO"
			msg = Message()
			msg.body = MessageText.encode('utf-8')
			channel.publish(msg, topic= "Controle.Console")
			print("\nSISTEMA LIGADO\n")
			break	
		else:
			MessageText = "NÃO FOI POSSÍVEL LIGAR O SISTEMA"
			

			msg = Message()
			msg.body = MessageText.encode('utf-8')
			channel.publish(msg, topic = "Controle.Console")
			continue
	time.sleep(1)


#Segunda parte do trabalho--------------------------------------------------------------------------------------------
			
provider = ServiceProvider(channel)
logging = LogInterceptor()
provider.add_interceptor(logging)

provider.delegate(
	topic = "Requisicao.Robo",
	function = RobotGateway,
	request_type = RequisicaoRobo,
	reply_type = RequisicaoRobo)
			
provider.run()









