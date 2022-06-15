import json
import sys
import ast

from st2common.runners.base_action import Action
import paramiko
class MyEchoAction(Action):
	result = dict()
	def run(self, server_name,user_name,password):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(server_name, username=user_name, password=password)
			TopProcessCommand='hostname'
			stdin, stdout, stderr = ssh.exec_command(TopProcessCommand)
			out=stdout.read()
			err = stderr.read().decode("utf-8")
			if(err == ''):
				output = {"retCode" : "0", "result" : out, "retDesc" : "Success"}
				print(output)
			else:
				raise Exception(err)
		except Exception as err:
			output = {"retCode" : "1", "result" : err, "retDesc" : "Failure"}
			print(output)
