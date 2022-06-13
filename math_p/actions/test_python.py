import json
import sys
import ast

from st2common.runners.base_action import Action
import paramiko
class Mytestfunction(Action):
	result = dict()
	def run(self, server_name,user_name,password):
		ProcessToRestart = ['falcon-sensor']   ## Process Which needs to be restarted
		RestartedProcess = []
		ErrorMSG = ''
		ErrorFlag = '0'
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(server_name, username=user_name, password=password)
			TopProcessCommand=("ps -eo pid,ppid,%mem,%cpu,comm --sort=-%cpu | head")
			stdin, stdout, stderr = ssh.exec_command(TopProcessCommand)
			TopProcess = stdout.read().decode("utf-8")
			TopProcess = TopProcess.lstrip()
			TopProcess = TopProcess.split('\n')
			flag = 'NO_PROCESS_TO_RESTART'
			for i in range(1,len(TopProcess)-1):
				data = TopProcess[i].split()
				if(data[4] in ProcessToRestart):
					try:
						flag = 'PROCESS_TO_RESTART'
						KillCommand=("echo {0} | sudo systemctl restart {1}").format(password,data[4])
						stdin, stdout, stderr = ssh.exec_command(KillCommand)
						err = stderr.read().decode("utf-8")
						if(err == ''):
							RestartedProcess.append(data[4])
						else:
							raise Exception(err)
					except Exception as err1:
						ErrorFlag = '-1'
						flag = 'ERROR_PROCESS_TO_RESTART'
						ErrorMSG = ErrorMSG + str(err1)

			if(ErrorFlag != '-1'):       
				if(flag == 'PROCESS_TO_RESTART'):
					output = {"retCode" : "0", "result" : " Processes Restarted Successfully", "retDesc" : "Success"}     
				else:
					output = {"retCode" : "0", "result" : "No Process in Top Consuming Processes to Restart", "retDesc" : "Success"}
			else:
				output = {"retCode" : "1", "result" : ErrorMSG , "retDesc" : "Failure"}
			print(output)

		except Exception as err:
			output = {"retCode" : "1", "result" : err, "retDesc" : "Failure"}
			print(output)
