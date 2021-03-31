from client import Udp
import pyaudio

chunk_size = 512
fs = 44100
channels = 1
rate = 20000
audio_format = pyaudio.paInt16
audio=pyaudio.PyAudio()
recording_stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size) 
playing_stream = audio.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)

client=Udp(("192.168.0.156",89))

def connect():
    client.Send("h".encode())

def RecordAudio():
    data = recording_stream.read(512) #recording
    return data
    

def PlayAudio(data):
    playing_stream.write(data) #playing

def Send():
    data=RecordAudio()
    client.Send(data) #send the record

def Recieve():
    data,addr=client.Recieve()
    PlayAudio(data) #play the record

def Close():
    client.close()
