# Module for basic audio manipulation like triming,
# converting by sox and scipy to np.array, etc
import os
import sys
from subprocess import call
from pathlib import Path
from typing import Union, List
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


SOX_PATH = r'c:\Program Files (x86)\sox-14-4-2\sox.exe'  #'/usr/local/bin/sox' TODO: 


def convert_audio(input_path: Union[Path, str], output_path: Union[Path, str]=None, frequency: int=44100):
    """ Convert file to np.array """
    assert Path.exists(Path(SOX_PATH)), 'install sox or setup path to sox properly'
    output_path = output_path if output_path is not None else Path('../tmp/temp.wav')
    if not Path.exists(Path(output_path)):
        command = f'"{SOX_PATH}" "{input_path}" -r {frequency} "{output_path}"'
        call(command, shell=True)
    data_file = wavfile.read(output_path)
    # Convert `data` to 32 bit integers:
    data = data_file[1]
    data = (np.iinfo(np.int32).max * (data / np.abs(data).max())).astype(np.int32)
    wavfile.write(output_path, frequency, data)
    return data


def findpeaks(data, part=4):
    signal = np.abs(data[:, 0])
    w = np.ones(int(len(signal)/20), 'd')
    y = np.convolve(w/w.sum(), signal, mode='valid')
    p_dist = int(len(y)/10)
    for i in range(10-part):
        peaks, _ = find_peaks(y, distance=p_dist+i*p_dist/part)
        if len(peaks) == 4:
            break
    if len(peaks) != 4:
        return None
    return peaks

# custom peakfinder bellow:
def find_angle(arr, n=35):
    l = len(arr)
    step = int(l/n)
    tg_phi = []
    for i in range(n-1):
        point1, point2 = arr[step*i], arr[step*(i+1)]
        tg_phi += [(point2-point1)/step] * step
    return tg_phi

def castum_findpeaks(data, trshld=0.1):
    signal = np.abs(data[:, 0])
    w = np.ones(int(len(signal)/20), 'd')
    y = np.convolve(w/w.sum(), signal, mode='valid')
    angl = find_angle(y)
    ppp = (angl>-np.max(angl)*trshld) & (angl<np.max(angl)*trshld)
    p = ppp[0]

    points = []
    for i in range(len(ppp)):
        if ppp[i]!=p:
            points += [i]
            p = ppp[i]

    start_isx = ppp[0]
    cuts = []
    for i in range(start_isx, len(points)-1, 2):
        cuts += [int((points[i+1]+points[i])/2)]
    return cuts


# vizualization:
if __name__ == '__main__':

    audios = os.path.normpath(os.path.join(os.path.dirname(__file__), '../res'))

    for file_name in [x for x in os.listdir(audios) if '.wav' in x and not '_out' in x]:
        file_path = Path(os.path.join(audios, file_name))
        data = convert_audio(input_path=file_path, output_path=str(file_path).replace('.wav', '_out.wav'))
        signal = np.abs(data[:, 0])
        w = np.ones(int(len(signal) / 20), 'd')
        y = np.convolve(w / w.sum(), signal, mode='valid')
        # peaks = findpeaks(data)
        cuts = castum_findpeaks(data, trshld=0.05)
        f = plt.figure(figsize=(14, 4))
        plt.title(file_path.name)
        plt.plot(signal)
        plt.plot(y)
        # plt.plot(peaks, y[peaks])
        # xcoords = [(peaks[i+1]+peaks[i])/2 for i in range(3)]
        xcoords = cuts
        for xc in xcoords:
            plt.axvline(x=xc, c='red')
        plt.show()