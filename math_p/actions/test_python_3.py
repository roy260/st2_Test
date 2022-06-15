import json
import sys
import ast

from st2common.runners.base_action import Action
import paramiko
class MyEchoAction(Action):
	result = dict()
	def run(self, server_name,user_name):
		try:
			ssh = paramiko.SSHClient()
<<<<<<< HEAD
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
=======
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
>>>>>>> bbd8eecf27336f15ead8837a5d8a44ce5d637bf0
			#ssh.load_system_host_keys()
			key_file = paramiko.RSAKey.from_private_key_file("/home/automation/.ssh/id_rsa")
			ssh.connect(server_name, username=user_name, pkey=key_file, allow_agent=False, look_for_keys=False)
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
