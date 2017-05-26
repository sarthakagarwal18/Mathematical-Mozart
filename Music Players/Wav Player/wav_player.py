import pyaudio
import wave
import sys
import os.path
import time

CHUNK_SIZE = 1024

def play_wav(wav_filename, chunk_size=CHUNK_SIZE):

    print ('Trying to play file ' + wav_filename)
    wf = wave.open(wav_filename, 'rb')
        
    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    p.terminate()

def usage():
    prog_name = os.path.basename(sys.argv[0])
    print ("Usage: {} filename.wav".format(prog_name))
    print ("or: {} -f wav_file_list.txt".format(prog_name))

def main():
    lsa = len(sys.argv)
    if lsa < 2:
        usage()
        sys.exit(1)
    elif lsa == 2:
        play_wav(sys.argv[1])
    else:
        if sys.argv[1] != '-f':
            usage()
            sys.exit(1)
        with open(sys.argv[2]) as wav_list_fil:
            for wav_filename in wav_list_fil:
                # Remove trailing newline.
                if wav_filename[-1] == '\n':
                    wav_filename = wav_filename[:-1]
                play_wav(wav_filename)
                time.sleep(3)

if __name__ == '__main__':
    main()
