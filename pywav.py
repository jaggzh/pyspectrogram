#!/usr/bin/python
from __future__ import print_function
import wave
import struct
import os
import ipdb as pdb
from ansi import *
from util import *
import numpy as np
import scipy.signal
import pylab             # for display
from pylab import *

file="test.wav"

_formats = {1: "<%dB", 2:"<%dh", 4:"<%dl"}
_zeroline = {1: 128, 2: 0 , 4: 0}

sx,sy = get_linux_termsize_xy()

filesize=os.path.getsize(file)

wr=wave.open(file, 'r')
nchannels=wr.getnchannels()
sampwidth=wr.getsampwidth()
framerate=wr.getframerate()
framecount=wr.getnframes()
framewidth=sampwidth*nchannels
maxsampval = (2**(sampwidth*8))/2 # 32768
print("Filesize:", filesize)
print("Channels:", nchannels, "Sample width:", sampwidth,
	 "Framerate:", framerate, "Framecount:", framecount)
print("Framewidth:", framewidth)
print("Maximum sample value:", maxsampval)

u_channel=0 # Left 0, Right 1
r_fcnt=framerate*1
loops=0
import matplotlib.gridspec as gridspec
import time
while True:
	loops = loops+1
	frames=wr.readframes(r_fcnt)
	print("Length of 60 frames read:", len(frames))
	audio = np.array(
		struct.unpack_from(_formats[sampwidth] % (len(frames)/sampwidth,),
			frames)) - _zeroline[sampwidth]
	if nchannels > 1: audio=audio.reshape((-1, nchannels))
	audio = audio[:,u_channel]
	#audio = abs(audio[0])
	
	f, t, Zxx = scipy.signal.stft(audio, fs=1.0, window='hann',
		nperseg=256, noverlap=None, nfft=None, detrend=False,
		return_onesided=True, boundary='zeros', padded=True, axis=-1)
	print(Zxx)

	if loops < 2:
		fig_view,axs = plt.subplots(1,1,figsize=(1,1))
		plt.ion()
		gs = gridspec.GridSpec(5,2)
		ax1 = plt.subplot(gs[0,0])
		line = ax1.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=2 * np.sqrt(2))
		plt.title('STFT Magnitude')
		plt.ylabel('Frequency [Hz]')
		plt.xlabel('Time [sec]')
		plt.show()
	else:
		#pdb.set_trace()
		ax1 = plt.subplot(gs[0,0])
		time.sleep(1)
		line = ax1.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=2 * np.sqrt(2))
		plt.show()

	#pdb.set_trace()
	#for i in range(0,len(frames),framewidth):
	#	#print("I:", i)
	#	# Frame and channel data
	#	fcdata = frames[i+u_channel:i+u_channel+sampwidth]
	#	#print("Frame data len:", len(fcdata))
	#	#print("Frame data:", fcdata)
	#	frame = struct.unpack("<h", fcdata)[0]
	#	#print("Frame[",i,"] ", frame, sep="")
	#	if not (i%2**6) and frame != 0 and abs(frame)>5:
	#		#print(frame)
	#		norm = frame*1.0/maxsampval + .5
	#		#print(norm)
	#		gxy(int(norm*sx), sy)
	#		print("*")
	if len(frames)*framewidth < r_fcnt: break
	

wr.close()
