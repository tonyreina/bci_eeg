#!/usr/bin/env python
# coding: utf-8

# # Load EEG Data

# ## BCI2000
# 
# ### Experimental Protocol
# 
# The data set consists of over 1500 one- and two-minute EEG recordings, obtained from 109 volunteers, as described below. The dataset was anonymized by the researchers.
# 
# The original data is [here](https://physionet.org/content/eegmmidb/1.0.0/). 
# 
# It is licensed under the [Open Data Commons Attribution License v1.0](https://physionet.org/content/eegmmidb/view-license/1.0.0/)
# 
# 109 subjects performed different motor/imagery tasks while 64-channel EEG were recorded using the BCI2000 system (http://www.bci2000.org). Each subject performed 14 experimental runs: two one-minute baseline runs (one with eyes open, one with eyes closed), and three two-minute runs of each of the four following tasks:
# 
# 1. A target appears on either the left or the right side of the screen. The subject opens and closes the corresponding fist until the target disappears. Then the subject relaxes.
# 2. A target appears on either the left or the right side of the screen. The subject imagines opening and closing the corresponding fist until the target disappears. Then the subject relaxes.
# 3. A target appears on either the top or the bottom of the screen. The subject opens and closes either both fists (if the target is on top) or both feet (if the target is on the bottom) until the target disappears. Then the subject relaxes.
# 4. A target appears on either the top or the bottom of the screen. The subject imagines opening and closing either both fists (if the target is on top) or both feet (if the target is on the bottom) until the target disappears. Then the subject relaxes.
# In summary, the experimental runs were:
# 
# + Baseline, eyes open
# + Baseline, eyes closed
# + Task 1 (open and close left or right fist)
# + Task 2 (imagine opening and closing left or right fist)
# + Task 3 (open and close both fists or both feet)
# + Task 4 (imagine opening and closing both fists or both feet)
# + Task 1
# + Task 2
# + Task 3
# + Task 4
# + Task 1
# + Task 2
# + Task 3
# + Task 4
# 
# The data are provided here in EDF+ format (containing 64 EEG signals, each sampled at 160 samples per second, and an annotation channel). For use with PhysioToolkit software, rdedfann generated a separate PhysioBank-compatible annotation file (with the suffix .event) for each recording. The .event files and the annotation channels in the corresponding .edf files contain identical data.
# 
# Each annotation includes one of three codes (T0, T1, or T2):
# 
# + T0 corresponds to rest
# + T1 corresponds to onset of motion (real or imagined) of the left fist (in runs 3, 4, 7, 8, 11, and 12) both fists (in runs 5, 6, 9, 10, 13, and 14)
# + T2 corresponds to onset of motion (real or imagined) of the right fist (in runs 3, 4, 7, 8, 11, and 12) both feet (in runs 5, 6, 9, 10, 13, and 14)
# 
# In the BCI2000-format versions of these files, which may be available from the contributors of this data set, these annotations are encoded as values of 0, 1, or 2 in the TargetCode state variable.

# This data set was created and contributed to PhysioBank by Gerwin Schalk (schalk at wadsworth dot org) and his colleagues at the BCI R&D Program, Wadsworth Center, New York State Department of Health, Albany, NY. W.A. Sarnacki collected the data. Aditya Joshi compiled the dataset and prepared the documentation. D.J. McFarland and J.R. Wolpaw were responsible for experimental design and project oversight, respectively. This work was supported by grants from NIH/NIBIB ((EB006356 (GS) and EB00856 (JRW and GS)).
# 
# The original publication can be found here:
# [Schalk, G., McFarland, D.J., Hinterberger, T., Birbaumer, N., Wolpaw, J.R. BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. IEEE Transactions on Biomedical Engineering 51(6):1034-1043, 2004.](https://ieeexplore.ieee.org/document/1300799)
# 
# The PhysioNet publication is here:
# [Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation. 101 (23), pp. e215–e220.](https://pubmed.ncbi.nlm.nih.gov/10851218/)
# You can download and unzip the EEG dataset with this command.
# !wget -q --show-progress -O tmp.zip https://physionet.org/static/published-projects/eegmmidb/eeg-motor-movementimagery-dataset-1.0.0.zip && unzip -qq tmp.zip && rm tmp.zip

"""
Download the data from Zenodo and unzip
"""
import urllib.request
from zipfile import ZipFile
from tqdm import tqdm

zip_url = 'https://physionet.org/static/published-projects/eegmmidb/eeg-motor-movementimagery-dataset-1.0.0.zip'


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

print("Downloading the EEG dataset")
download_url(zip_url, 'temp_eeg_data.zip')

# Open the .zip file
print("Unzipping the dataset")
with ZipFile(file='temp_eeg_data.zip') as zip_file:

    # Loop over each file
    for file in tqdm(iterable=zip_file.namelist(), total=len(zip_file.namelist())):

        # Extract each file to another directory
        # If you want to extract to current working directory, don't specify path
        zip_file.extract(member=file, path='.')
"""
END download data
"""

from pyedflib import highlevel

import csv
import glob
import os
import numpy as np

#from tqdm.notebook import tqdm

tasks = ["Baseline, eyes open",
         "Baseline, eyes closed",
         "Task 1",
         "Task 2",
         "Task 3",
         "Task 4",
         "Task 1",
         "Task 2",
         "Task 3",
         "Task 4",
         "Task 1",
         "Task 2",
         "Task 3",
         "Task 4"]

csv_filename = "eeg_data.csv"
print(f"Exporting to CSV file: {csv_filename}")
filenames = tqdm(glob.glob("./files/S*/*.edf"), position=0)

with open(csv_filename, 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(["Filename", "Task", "Run", "Code", "EEG"])
    
    for filename in filenames:

        filenames.set_description(f"{filename}")

        run_idx = int(os.path.splitext(os.path.basename(filename))[0].split("R")[1]) - 1
        task = tasks[run_idx]

        signals, signal_headers, header = highlevel.read_edf(filename)

        sample_rate = signal_headers[0]["sample_rate"]

        for idx in range(len(header["annotations"])):

            length_time = int(np.ceil(header["annotations"][idx][1] * sample_rate)) - 2
            data = np.zeros((len(signals), length_time))

            for channel in range(len(signals)):

                begin_idx = int(header["annotations"][idx][0] * sample_rate)
                end_idx   = begin_idx + length_time

                code_label = header["annotations"][idx][2]
                
                eeg = signals[channel, begin_idx:end_idx]
                eeg = (eeg - np.mean(eeg)) / np.std(eeg)

                data[channel, :len(eeg)] = eeg
            
        datawriter.writerow([filename, task, run_idx, code_label, data])

print(f"FINISHED. Data is in {csv_filename}")

