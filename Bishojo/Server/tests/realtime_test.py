from whisper_mic.whisper_mic import WhisperMic

print("何か話してください")
mic = WhisperMic(model="whisper-base-japanese")
mic.listen_loop(phrase_time_limit=1)
