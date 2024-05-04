import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

databaseURL = 'https://fileuploading-67153-default-rtdb.asia-southeast1.firebasedatabase.app' 

ticketValue = '-NvSCmNWdSZkeSG8nxKY'

cred = credentials.Certificate("fbaseKey1.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':databaseURL
	})

ref = db.reference(f"/transaction/{ticketValue}")

transactionStatus = ref.child("transactionStatus").get()

print(transactionStatus)