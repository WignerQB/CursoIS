from __future__ import print_function
from is_wire.core import Channel, Subscription, Message, StatusCode, Status, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor
import time
from random import randint
from RequisicaoRobo_pb2 import RequisicaoRobo 
from is_msgs import common_pb2
from is_msgs.robot_pb2 import RobotTaskRequest
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import Position



class Robot():
	def __init__(self, id, x, y, z):
		self.id = id
		self.pos_x = x
		self.pos_y = y
		self.pos_z = z
		
	def get_id(self):
		return self.id
	
	def set_position(self, x, y, z):
		self.pos_x = x
		self.pos_y = y
		self.pos_z = z
		
	def get_position(self):
		return self.pos_x, self.pos_y, self.pos_z
		

def get_position(Robot_info, ctx):
	RobTReq = RobotTaskRequest()
	for robot in ROBOTS:
		if robot.id == Robot_info.id:
			RobTReq.basic_move_task.positions.extend([Position(x =0, y = 0, z = 0)])
			RobTReq.id = Robot_info.id
			RobTReq.basic_move_task.positions[0].x, RobTReq.basic_move_task.positions[0].y, RobTReq.basic_move_task.positions[0].z = robot.get_position()
		#print([RobTReq.basic_move_task.positions[0].x, RobTReq.basic_move_task.positions[0].y, RobTReq.basic_move_task.positions[0].z])
	return RobTReq
	
def set_position(Robot_info, ctx):
	time.sleep(0.2)
	for robot in ROBOTS:
		if robot.id == Robot_info.id:
			set_x = int(Robot_info.basic_move_task.positions[0].x)
			set_y = int(Robot_info.basic_move_task.positions[0].y)
			set_z = int(Robot_info.basic_move_task.positions[0].z)
			robot.set_position(set_x, set_y, set_z)
			return Status(StatusCode.OK)
	#txt = "Robo {} está na posição {}"
	
	'''
	print(txt.format(R1.id, R1.get_position()))
	print(txt.format(R2.id, R2.get_position()))
	print(txt.format(R3.id, R3.get_position()))
	print(txt.format(R4.id, R4.get_position()))
'''

		
R1 = Robot(1, 1, 12, 1)
R2 = Robot(2, 3, 5, 10)
R3 = Robot(3, 5, 5, 5)
R4 = Robot(4, 2, 9, 0)
ROBOTS = [R1, R2, R3, R4]

#R1.set_position(5, 4, 0)


txt = "Robo {} está na posição {}"
print(txt.format(R1.id, R1.get_position()))
print(txt.format(R2.id, R2.get_position()))
print(txt.format(R3.id, R3.get_position()))
print(txt.format(R4.id, R4.get_position()))



channel = Channel("amqp://guest:guest@localhost:5672")
provider = ServiceProvider(channel)
logging = LogInterceptor()
provider.add_interceptor(logging)

provider.delegate(
	topic = "Requisicao.Get_position",
	function = get_position,
	request_type = RobotTaskRequest,
	reply_type = RobotTaskRequest)

provider.delegate(
	topic = "Requisicao.Set_position",
	function = set_position,
	request_type = RobotTaskRequest,
	reply_type = Empty)
	
provider.run()













