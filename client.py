import rsa, pyaudio, sys, wave, struct, cv2
import tkinter as Tk

# Set audio properties
CHANNELS      = 2
RATE          = 8000
WIDTH         = 2
BLOCKLEN      = 4

def end_call():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

root = Tk.Tk()
Label_1 = Tk.Label(root, text = 'Value adjustment')
B_quit = Tk.Button(root, text = 'Quit', command = end_call)

Label_1.pack()
B_quit.pack()

p = pyaudio.PyAudio()

output_wavfile = 'input.wav'
output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

output_wavfile1 = 'encrypted.wav'
output_wf1 = wave.open(output_wavfile1, 'w')      # wave file
output_wf1.setframerate(RATE)
output_wf1.setsampwidth(WIDTH)
output_wf1.setnchannels(CHANNELS)

output_wavfile2 = 'decrypted.wav'
output_wf2 = wave.open(output_wavfile2, 'w')      # wave file
output_wf2.setframerate(RATE)
output_wf2.setsampwidth(WIDTH)
output_wf2.setnchannels(CHANNELS)

stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

(pubkey, privkey) = rsa.newkeys(256)

CONTINUE = True

while CONTINUE:
  input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)

  output_wf.writeframes(input_bytes)

  crypto = rsa.encrypt(input_bytes, pubkey)

  output_wf1.writeframes(crypto)

  output_bytes = rsa.decrypt(crypto, privkey)

  output_wf2.writeframes(output_bytes)

  print(sys.getsizeof(crypto),sys.getsizeof(output_bytes))
  stream.write(output_bytes)

  root.update()

print('* Finished')
stream.stop_stream()
stream.close()
p.terminate()
output_wf.close()
output_wf1.close()
output_wf2.close()