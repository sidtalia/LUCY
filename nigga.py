from gtts import gTTS
import speech_recognition as sr #requires pyaudio
import playsound
import os
import time
import webbrowser as wb
import sys

def speaketh(audio_string):
	tits = gTTS(text=audio_string, lang='en-uk') #tits -> text input to speech. get your head out the gutter
	file_name = ""
	success=False
	i = 0
	while success == False:
		i+=1
		try:
			file_name = "temp_{}.mp3".format(str(i))
			tits.save(file_name)#create temp audio file
			success=True
		except:
			pass
	playsound.playsound(file_name,True) #play it
	os.remove(file_name)#destroy it. I think a better alternative might be to just save certain responses. TODO : fix this

def listenn(wait_Time):
	print("say something")#i'm giving up on you
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("ready") #debugging. replace with " yes boss? "
		audio = r.listen(source,timeout=wait_Time)
		# print("got something") # debugging. replace with "on it/affirmative.
	data = ""
	try:
		data = r.recognize_google(audio,language='en-GB')
		print(data)#debugging
	except sr.UnknownValueError:
		# print("we fucked up") # debugging : replace with "I'm sorry i didn't get that, can you repeat yourself please?"
		speaketh("I'm sorry, i didn't get that.")
	except sr.RequestError as e:
		# print("request error") # debugging : replace with "can you speak with a lighter accent? geez"
		speaketh("null pointer exception boss")

	return data

def googleit(query):
	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
	url = "https://www.google.co.in/search?q=" +query+ "&oq="+query+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
	wb.open_new(url)

def check_keyphrase(query,word):
	string = query.lower()
	return f'{word}' in f'{string}'

annoying = 0

def process(query):
	global annoying
	if check_keyphrase(query,"what") or check_keyphrase(query,"why") or check_keyphrase(query,"when") or check_keyphrase(query,"how") or check_keyphrase(query,"where") or check_keyphrase(query,"who"):
		if(annoying >= 1 and annoying <2):
			speaketh("so many questions!")
		if(annoying >= 2):
			speaketh("stop bothering me with this nonsense!")
		googleit(query)
		annoying +=1 
	if check_keyphrase(query,"dumbass"):#because its always fun to call an AI a dumbass when it makes a mistake.
		speaketh("HOW DARE YOU!")
	if check_keyphrase(query,"quit"):
		sys.exit()

# googleit("how many seconds in a minute")
active = False
timeout = 0
while 1:
	if not active:
		time.sleep(1)
		query = listenn(4)
		if check_keyphrase(query,"lucy"):
			active = True
			timeout = time.time()

	if active:
		query = listenn(10)
		process(query)
		if time.time() - timeout>100:
			print("default")
			active = False


