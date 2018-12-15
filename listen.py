import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
	audio = r.listen(source)

	with open('resources\\speech.wav', 'wb') as f:
		f.write(audio.get_wav_data())