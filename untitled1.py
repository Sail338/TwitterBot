from flask import Flask
from flask import request
from flask import render_template
import json as js
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from havenondemand.hodindex import HODClient
client = HODClient("http://api.havenondemand.com/",
                            "075a1e5f-ad81-4677-9362-7ca4649103f2")

listofData = []

class ClassName(StreamListener):
	fuckmylife = 0
	"""docstring for ClassName"""
	def on_status(self, status):
		ClassName.fuckmylife +=1
		#parsed_data = "tweet='%s'"%(status.text)
		
		listofData.append(status.text)
		
			
		if(ClassName.fuckmylife<25):
			return True

		else:
			return False
			


		
		

	

	def on_error(self, status):

		print (status)



app = Flask(__name__)
#intialize tweepy

acces = '4084903883-arskmHkXnoaHE36lLC8lIVEh4ifSdLNq62DJhEa'
key ='kx0s8vYDWfp4HFQQVYzDFzHoFTIlPW4xoVF0DtfSIu9lh'
consumerkey = '1hSwjB3VjGewtve7MtAapDaKB'
consumersecret ='v6wpvt4UXUl4t4OMmkqrX0UFTHzcS6SaJJG4gmHo09313s9Lvw'
def login():
			auth = OAuthHandler(consumerkey,consumersecret)
			auth.set_access_token(acces, key)
			return auth

def streamData(n):


			autth = login()
			stream = tweepy.streaming.Stream(autth, ClassName())
			
			stream.filter(track=[n])

		



@app.route('/')
def hello_world():

	


    return render_template("index.html")
@app.route('/data',methods =['GET','POST'])
def data():
	if(request.method == 'POST'):
		sk = request.form["kek"]

		streamData(sk)
		badcounter = 0
		goodCounter = 0
		for tweet in listofData:
			 #print tweet
			 r=client.post('analyzesentiment',{'text':tweet})
			 data = r.json()
			 print data["aggregate"]["score"]
			 if(data["aggregate"]["score"] >0 or data["aggregate"]['sentiment'] == "positive"):
			 	goodCounter +=1
			 elif (data["aggregate"]["score"] < 0 or data["aggregate"]["sentiment"] == "negative"):
			 	badcounter +=1


			 
			 #print data



		
		
		
		return render_template("data.html",goodCounter=goodCounter,badCounter=badcounter)
	return "kek"



if __name__ == '__main__':
	app.debug = True
	app.run(port=8000)
