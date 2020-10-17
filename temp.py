from PIL import Image
import dhash
import os
import matplotlib.pyplot as plt
from imageio import imread
import time

photoDir = 'C://Users//Wilson Lab//Documents//Python//FB_photos//Combined'
file_list = os.listdir(photoDir)




img = Image.open(os.path.join(photoDir, '20120730 7.jpg'))
h = dhash.dhash_int(img)


hash_list = []
hash_keys = dict()
for index, filename in enumerate(os.listdir(photoDir)):
    print(index)
    if os.path.isfile(os.path.join(photoDir, filename)):
        img = Image.open(os.path.join(photoDir, filename))
        filehash = dhash.dhash_int(img)
        hash_list.append(filehash)
        

minDiffs = []
for i in range(0, len(hash_list)):
    print(i)
    diffs = []
    for j in range(0, len(hash_list)):
        if i != j:
            diffs.append(dhash.get_num_bits_different(hash_list[i], hash_list[j]))    
    minDiffs.append(min(diffs))
    
    
noDupeList = [f for d,f in zip(minDiffs, file_list) if d > 10]


#for i in noDupeList:
i = noDupeList[7];
print(i)
plt.imshow(imread(os.path.join(photoDir, i)))
time.sleep(1)





