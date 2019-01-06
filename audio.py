from google.cloud import texttospeech
import pygame as pg

class Audio:

	def audio(self, text_to_read):
		# Instantiates a client
		client = texttospeech.TextToSpeechClient()

		self.__text_to_read = text_to_read

		# Set the text input to be synthesized
		synthesis_input = texttospeech.types.SynthesisInput(text=self.__text_to_read)

		# Build the voice request, select the language code ("en-US") and the ssml
		# voice gender ("neutral")
		voice = texttospeech.types.VoiceSelectionParams(
		    language_code='en-US',
		    name='en-US-Wavenet-D')

		# Select the type of audio file you want returned
		audio_config = texttospeech.types.AudioConfig(
		    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

		# Perform the text-to-speech request on the text input with the selected
		# voice parameters and audio file type
		response = client.synthesize_speech(synthesis_input, voice, audio_config)

		# The response's audio_content is binary.
		try:
			with open('resources\\output.mp3', 'w+b') as out :
				out.write(response.audio_content)
		except:
			with open('..\\resources\\output.mp3', 'w+b') as out:
				# Write the response to the output file.
				out.write(response.audio_content)

		pg.mixer.init()
		clock = pg.time.Clock()
		try:
			f = open('resources\\output.mp3', 'rb')
		except:
			f = open('..\\resources\\output.mp3', 'rb')
		pg.mixer.music.load(f)
		#pg.mixer.music.load('resources\\output.mp3')
		pg.mixer.music.play(loops=0, start=0.0)
		while pg.mixer.music.get_busy():
			# check if playback has finished
			clock.tick(30)
		pg.mixer.music.stop()
		pg.mixer.quit()
		f.close()