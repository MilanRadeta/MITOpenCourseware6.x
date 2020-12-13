# No Imports Allowed!


def backwards(sound):
    return {'rate': sound['rate'], 'left': list(reversed(sound['left'])), 'right': list(reversed(sound['right']))}


def mix(sound1, sound2, p):
    if sound1['rate'] != sound2['rate']:
        return None
    
    out_len = min(len(sound1['left']), len(sound2['left']))
    
    def mix_channel(channel):
        return [p * sound1[channel][i] + (1 - p) * sound2[channel][i] for i in range(out_len)]
    
    return {'rate': sound1['rate'], 'left': mix_channel('left'), 'right': mix_channel('right')}


def multimix(sounds, ps):
    if len(sounds) != len(ps):
        return None

    rate = sounds[0]['rate']
    out_len = len(sounds[0]['left'])
    for s in sounds:
        if s['rate'] != rate:
            return None
        if len(s['left']) < out_len:
            out_len = len(s['left'])
    
    def mix_channel(channel):
        result = [0] * out_len
        for i in range(out_len):
            for j in range(len(sounds)):
                p, s = ps[j], sounds[j]
                result[i] += s[channel][i] * p
        return result
    
    return {'rate': rate, 'left': mix_channel('left'), 'right': mix_channel('right')}


def echo(sound, num_echos, delay, scale, alternate=False):
    sample_delay = round(delay * sound['rate'])
    left_start = 0
    if alternate:
        right_start = 1
        step = 2
    else:
        right_start = 0
        step = 1

    def generate_channel(channel, start):
        channel = sound[channel].copy()

        result = []
        for j in range(len(channel) + num_echos * sample_delay):
            if j < len(channel):
                result.append(channel[j])
            else:
                result.append(0)

        for i in range(start, num_echos, step):
            for j in range(len(channel)):
                val = channel[j]
                k = (i + 1) * sample_delay + j
                result[k] += val * scale ** (i + 1)
            
        return result

    return {'rate': sound['rate'], 'left': generate_channel('left', left_start), 'right': generate_channel('right', right_start)}


def pan(sound):
    def pan_channel(channel, start, end):
        channel = sound[channel].copy()
        n = len(channel)
        step = (end - start) / (n - 1)

        for i in range(n):
            channel[i] *= start + step * i
            
        return channel

    return {'rate': sound['rate'], 'left': pan_channel('left', 1, 0), 'right': pan_channel('right', 0, 1)}


def remove_vocals(sound):
    left = sound['left']
    right = sound['right']
    channel = [left[i] - right[i] for i in range(len(left))]
    return {'rate': sound['rate'], 'left': channel, 'right': channel.copy()}


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct
import os
import pathlib

root_folder = pathlib.Path(__file__).parent.absolute().__str__()

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
            
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    folder = root_folder + '/sounds'
    # output = root_folder + '/reversed'
    # for sound in os.listdir(folder):
    #     if '.wav' in sound:
    #         res = load_wav('%s/%s' % (folder, sound))
    #         write_wav(backwards(res), '%s/%s' % (output, sound))

    # output = root_folder + '/mixes'
    # sounds = [('chord', 'meow', 0.7), ('synth', 'water', 0.2)]

    # for sound in sounds:
    #     sound1 = load_wav('%s/%s.wav' % (folder, sound[0]))
    #     sound2 = load_wav('%s/%s.wav' % (folder, sound[1]))
    #     write_wav(mix(sound1, sound2, sound[2]), '%s/%s-and-%s.wav' % (output, sound[0], sound[1]))

    # output = root_folder + '/echoes'
    # sounds = [('hello.wav', 4, 0.4, 0.4), ('chord.wav', 5, 0.3, 0.6)]

    # for sound in sounds:
    #     file = load_wav('%s/%s' % (folder, sound[0]))
    #     write_wav(echo(file, sound[1], sound[2], sound[3]), '%s/%s' % (output, sound[0]))

    # output = root_folder + '/pans'
    # sounds = ['doorcreak.wav', 'car.wav']

    # for sound in sounds:
    #     file = load_wav('%s/%s' % (folder, sound))
    #     write_wav(pan(file), '%s/%s' % (output, sound))

    # output = root_folder + '/karaoke'
    # sounds = ['coffee.wav']

    # for sound in sounds:
    #     file = load_wav('%s/%s' % (folder, sound))
    #     write_wav(remove_vocals(file), '%s/%s' % (output, sound))

    # output = root_folder + '/alt_echoes'
    # sounds = [('hello.wav', 4, 2, 0.7), ('chord.wav', 5, 0.3, 0.6)]

    # for sound in sounds:
    #     file = load_wav('%s/%s' % (folder, sound[0]))
    #     write_wav(echo(file, sound[1], sound[2], sound[3], alternate=True), '%s/%s' % (output, sound[0]))

    output = root_folder + '/multimixes'
    sounds = ['chord.wav', 'meow.wav', 'synth.wav']
    sounds = [load_wav('%s/%s' % (folder, s)) for s in sounds]
    ps = [0.5, 1, 0.2]
    write_wav(multimix(sounds, ps), '%s/%s' % (output, 'multimix.wav'))
