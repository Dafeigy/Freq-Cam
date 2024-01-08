import numpy as np
data_file = r"process-new\1\punch\amp.npy"

data = np.load(data_file)
data_length = len(data)
print(f"数据长度：{len(data)}")

ds_data = np.diff(data,axis=0)
ds_array_1_list = []
ds_array_2_list = []
for t in range(len(ds_data)):
    # t 是时间索引序号 理论上每25个sample是两秒
    # 即应该每隔25个sample会有一个比较大的波动
    y_data =  ds_data[t].tolist()
    y_data_1 = [y_data[i][0][0] for i in range(624)]
    y_data_2 = [y_data[i][0][1] for i in range(624)]
    ds_array_1_list.append(y_data_1)
    ds_array_2_list.append(y_data_2)

ds_array_1 = np.transpose(np.array(ds_array_1_list))
ds_array_2 = np.transpose(np.array(ds_array_2_list))

import matplotlib.pyplot as plt

plt.imshow(ds_array_1)
plt.show()