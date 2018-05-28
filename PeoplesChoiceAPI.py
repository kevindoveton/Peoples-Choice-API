import requests, uuid, json, datetime

apiKey = 'b7e8d8cad79c4126b4f0b13a3cd5d774'

# ----------------------------------------------------------------------
# register
# Register a New Device
# ----------------------------------------------------------------------
def register(memberId, password, pin, deviceName):

	headers = {
		'MP-API-KEY' : apiKey,
		'Connection' : 'keep-alive',
		'Content-Type' : 'application/json',
		'charset' : 'UTF-8',
		'Accept' : 'application/json, text/javascript, */*; q=0.01'
	}

	# GET https://online.peopleschoicecu.com.au/platform/devices/deviceId
	deviceId = requests.get('https://online.peopleschoicecu.com.au/platform/devices/deviceId', headers=headers).json()['Body']

	requestData = {
		"DeviceId" : deviceId,
		"UserId" : memberId,
		"Password" : password,
		"Pin" : pin,
		"DeviceName" : deviceName,
		"Factor2Code" : "",
		"AuthenticationId" : 0
	}

	# POST https://online.peopleschoicecu.com.au/platform/devices/
	register = requests.post('https://online.peopleschoicecu.com.au/platform/devices/register', headers=headers, data=json.dumps(requestData))

	return register, deviceId

# ----------------------------------------------------------------------
# keepAlive
# Keep the connection alive
# ----------------------------------------------------------------------
def keepAlive(authToken):
	headers = {
		'MP-API-KEY' : apiKey,
		'MP-AUTH-TOKEN' : authToken,
		'Connection' : 'keep-alive',
		'Content-Type' : 'application/json',
		'charset' : 'UTF-8',
		'Accept' : 'application/json, text/javascript, */*; q=0.01'
	}

	keepAlive = requests.post('https://online.peopleschoicecu.com.au/platform/session/keepalive', headers=headers)

	return keepAlive.json()['Body']

# ----------------------------------------------------------------------
# login
# Log in to an account using a deviceID and Pin
# Returns the auth code
# ----------------------------------------------------------------------
def login(deviceId, pin):

	headers = {
		'MP-API-KEY' : apiKey,
		'Connection' : 'keep-alive',
		'Content-Type' : 'application/json',
		'charset' : 'UTF-8',
		'Accept' : 'application/json, text/javascript, */*; q=0.01'
	}

	requestData = {
		"IsDeviceAndPin": True,
		"DeviceId": deviceId,
		"MemberNumber": "",
		"PasswordOrPin": pin,
		"Factor2Code": ""
	}

	# POST /platform/session/ HTTP/1.1
	login = requests.post('https://online.peopleschoicecu.com.au/platform/session/', headers=headers, data=json.dumps(requestData))

	return login.json()['AuthToken']

# ----------------------------------------------------------------------
# getAccounts
# Get an array of accounts
# ----------------------------------------------------------------------
def getAccounts(authToken):

	headers = {
		'MP-API-KEY' : apiKey,
		'MP-AUTH-TOKEN' : authToken,
		'Connection' : 'keep-alive',
		'Content-Type' : 'application/json',
		'charset' : 'UTF-8',
		'Accept' : 'application/json, text/javascript, */*; q=0.01'
	}

	# POST /platform/session/ HTTP/1.1
	accounts = requests.get('https://online.peopleschoicecu.com.au/platform/accounts/', headers=headers)

	return accounts.json()


# ----------------------------------------------------------------------
# getTransactionsFromEpoch
# A wrapper of getTransactions using epoch millis times
# ----------------------------------------------------------------------
def getTransactionsFromEpoch(authToken, accountNumber, startDate, endDate):
	startDate = "/Date("+startDate+")/"
	endDate = "/Date("+endDate+")/"
	return getTransactions(authToken, accountNumber, startDate, endDate)

# ----------------------------------------------------------------------
# getTransactions
# Get a list of transactions for a single account
# between startDate and endDate
# ----------------------------------------------------------------------
def getTransactions(authToken, accountNumber, startDate, endDate):
	headers = {
		'MP-API-KEY' : apiKey,
		'MP-AUTH-TOKEN' : authToken,
		'Connection' : 'keep-alive',
		'Content-Type' : 'application/json',
		'charset' : 'UTF-8',
		'Accept' : 'application/json, text/javascript, */*; q=0.01'
	}

	requestData = {
		"AccountNumber": accountNumber,
		"TransactionType": 1,
		"BeginDate": startDate,
		"EndDate": endDate
	}

	# POST /platform/session/ HTTP/1.1
	accounts = requests.post('https://online.peopleschoicecu.com.au/platform/transactions/history', headers=headers, data=json.dumps(requestData))

	return accounts

# ----------------------------------------------------------------------
# getDate
# Get the current time from the PCCU server
# ----------------------------------------------------------------------
def getDate():
	headers = {
		'MP-API-KEY' : apiKey,
		'charset' : 'UTF-8',
		'Accept' : 'application/json, text/javascript, */*; q=0.01'
	}

	# POST /platform/session/ HTTP/1.1
	date = requests.get('https://online.peopleschoicecu.com.au/platform/session/', headers=headers).text
	date = parseDate(date)

	return date

# ----------------------------------------------------------------------
# parseDate
# Convert a JSON UTC date string to python datetime
# ----------------------------------------------------------------------
def parseDate(datestring):
	timepart = datestring.split('(')[1].split(')')[0]
	milliseconds = int(timepart[:-5])
	hours = int(timepart[-5:]) / 100
	time = milliseconds / 1000

	dt = datetime.datetime.utcfromtimestamp(time + hours * 3600)
	# return dt.strftime("%Y-%m-%dT%H:%M:%S") + '%02d:00' % hours
	return dt

# ----------------------------------------------------------------------
# dtToEpoch
# Convert a python datetme to seconds from epoch
# ----------------------------------------------------------------------
def dtToEpoch(dt):
	return (dt - datetime.datetime(1970,1,1)).total_seconds()*1000

# ----------------------------------------------------------------------
# dtToEpochStr
# A wrapper of dtToEpoch to return the datetime as a string
# ----------------------------------------------------------------------
def dtToEpochStr(dt):
	return str(int(dtToEpoch(dt)))
