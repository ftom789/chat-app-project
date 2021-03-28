from client import Udp
import pyaudio
import threading
chunk_size = 512
fs = 44100
channels = 1
rate = 20000
audio_format = pyaudio.paInt16
audio=pyaudio.PyAudio()
recording_stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
playing_stream = audio.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)

client=Udp(("127.0.0.1",89))
client.Send("h".encode())
def RecordAudio():
    data = recording_stream.read(512)
    return data
    

def PlayAudio(data):
    playing_stream.write(data)

def Send():
    while True:
        print("sent")
        data=RecordAudio()
        client.Send(data)

def Recieve():
    while True:
        print("recieved")
        data,addr=client.Recieve()
        PlayAudio(data)

send=threading.Thread(target=Send)
recieve=threading.Thread(target=Recieve)
send.start()
recieve.start()