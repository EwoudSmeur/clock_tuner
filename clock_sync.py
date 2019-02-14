import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

# Set plot environment
get_ipython().run_line_magic('matplotlib', 'notebook')

fs = 48000 # Not sure how to check if this is feasible
duration = 10.0  # seconds

# Amount of ticks that your watch should make per second (e.g. 5.0)
target_freq = 5.0

# Record stuff
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True)

# Process data
# Go to mono magnitude
absdata = abs(myrecording[:,0])
# Normalize
absdata = absdata / np.amax(absdata)

x = 0
peaks = []

while x < len(absdata) - fs/target_freq:

    # Find the first pulse
    peaks.append(x + np.argmax(absdata[x:x+int(fs/target_freq)]))

    # Skip number of samples so that we are surely past the last tick.
    x = peaks[-1] + int(fs/target_freq/2)

# Always measure between two beats of the same type.
if len(peaks) % 2 == 0:
    peaks.pop(-1)

output = absdata

plt.plot(output)
plt.scatter(peaks, output[peaks], c=(1,0,0), edgecolors='face')
plt.ylabel('recording')
plt.show()

# The wheel rocks back and forth, one way may be faster than the other way,
# hence the two frequencies.
freq1 = 1 / ((peaks[-1] - peaks[0])/fs / (len(peaks)-1))
freq2 = 1 / ((peaks[-2] - peaks[0])/fs / (len(peaks)-2))

print('frequency:', freq1, 'Hz')
print('ticks per hour:', freq1*60*60)
print('error per day:', (1/target_freq - 1/freq1) * 3600*24, 'seconds (- behind, + ahead)')
print('off beat:', (1/min(freq1,freq2) - 1/max(freq1,freq2)) * 1000, 'ms')

