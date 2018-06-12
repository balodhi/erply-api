import requests as rq

class EAPI:
	def __init__(self,url = None, clientCode = None, username = None, password = None, sslCACertPath = None):
		self.url = url
		self.clientCode = clientCode
		self.username = username
		self.password = password
		self.sslCACertPath = sslCACertPath
		self.session = {}
	def _getSessionKey(self):
		if 'EAPISessionKey' not in self.session:

			result = self.sendRequest("verifyUser",{"username" : self.username, "password" : self.password})
			results = result.json()
			self.session = {'EAPISessionKey': {
											self.clientCode: 
											{
												self.username: results['records'][0]['sessionKey']												
											}
										},
							'EAPISessionKeyExpires' :
												{
													self.clientCode :
													{
														self.username: results['records'][0]['sessionLength']
													}
												}
							}

		
		return self.session['EAPISessionKey'][self.clientCode][self.username]

	def sendRequest(self,request, parameters={}):

		parameters['request'] = request
		parameters['clientCode'] = self.clientCode
		parameters['version'] = '1.0'
		parameters['username'] = self.username
		parameters['password'] = self.password

		if (request != 'verifyUser'):
			parameters['sessionKey'] = self._getSessionKey()
			#print(parameters['sessionKey'])

		res = rq.post(self.url, params=parameters)
		response=res.json()
		return res
		
		#print(res.text)

