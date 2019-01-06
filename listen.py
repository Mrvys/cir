import speech_recognition as sr

class Listen:

	def listen(self):
		r = sr.Recognizer()

		with sr.Microphone() as source:
			audio = r.listen(source)
			try:
				with open('resources\\speech.wav', 'wb') as f:
					f.write(audio.get_wav_data())
			except:
				with open('..\\resources\\speech.wav', 'wb') as f:
					f.write(audio.get_wav_data())

		try:
			return r.recognize_google(audio)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))