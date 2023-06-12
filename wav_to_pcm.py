import numpy as np


def wav2pcm(src_path, des_path):
    with open(file=src_path, mode='rb') as f:
        f.seek(0)
        f.read(44)
        data = np.fromfile(f, dtype=np.int16)
        data.tofile(des_path)
