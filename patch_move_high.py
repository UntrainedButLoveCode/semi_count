import numpy as np
import shutil
import os 

labeled_list = np.loadtxt('label_list/high-5.txt', dtype = str)
all_croped = os.listdir('high/uncertain_data/')

for file in all_croped:
    if (file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2]+ '.jpg') in labeled_list:
        shutil.copyfile('high/uncertain_data/' + file, 'high/uncertain_data_5/' + file )


labeled_list = np.loadtxt('label_list/high-10.txt', dtype = str)

for file in all_croped:
    if (file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2]+ '.jpg') in labeled_list:
        shutil.copyfile('high/uncertain_data/' + file, 'high/uncertain_data_10/' + file )

labeled_list = np.loadtxt('label_list/high-40.txt', dtype = str)

for file in all_croped:
    if (file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2]+ '.jpg') in labeled_list:
        shutil.copyfile('high/uncertain_data/' + file, 'high/uncertain_data_40/' + file )