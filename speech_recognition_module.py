def recognize_speech():
	import speech_recognition as sr

	#Sample rate is how often values are recorded
	sample_rate = 48000

	#Chunk is like a buffer. It stores 2048 samples (bytes of data)
	chunk_size = 2048

	#Initialize the recognizer
	r = sr.Recognizer()
	
	#Initialize the mic
	mic = sr.Microphone(sample_rate = sample_rate, chunk_size = chunk_size)


	with mic as source:
		#wait for a second to let the recognizer adjust the
		#energy threshold based on the surrounding noise level
		r.adjust_for_ambient_noise(source)
		print ("Say Something")
		#listens for the user's input
		audio = r.listen(source)
			
		try:
			text = r.recognize_google(audio)
			return text
		except:
			print("Google Speech Recognition could not understand audio")
