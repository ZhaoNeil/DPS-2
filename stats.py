# %%
from glob import glob
import os
import pandas as pd  

folder='d:/dps/a2/DPS-2/result'
def read_result(type, param):
  result=[]
  files=glob(os.path.join(folder, type+'_'+str(param)+'*'))
  for file in files:
    with open(file, 'r') as f:
      next(f)
      for line in f:
        fromId, keyId, targetId, measure=line.strip().split('\t')
        result.append([param, fromId, keyId, targetId, int(measure)])
  return result

#read the path length data 
nNode=[64, 256, 1020]
e1_res=[]
for n in nNode:
  e1_res+=read_result('e1', n)

e1_res_df=pd.DataFrame(data=e1_res, columns=['nNode', 'fromId', 'keyId', 'targetId', 'nStep'])

#read the timeout data
prob=[0.1, 0.3, 0.5]
e2_res=[]
for p in prob:
  e2_res+=read_result('e2', p)
e2_res_df=pd.DataFrame(data=e2_res, columns=['prob', 'fromId', 'keyId', 'targetId', 'nTimeout'])

# %%
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.rcParams["axes.labelsize"] = 12
plt.rcParams["legend.title_fontsize"]=12
plt.rcParams['legend.fontsize']='large'

#compute mean and median path length
step_mean=e1_res_df.groupby(by='nNode')['nStep'].mean()
step_median=e1_res_df.groupby(by=['nNode'])['nStep'].median()

#path length: box plot
ax=sns.boxplot(x='nNode', y='nStep', data=e1_res_df, whis=[1, 99],  palette="pastel")
ax.set(xlabel='Number of nodes', ylabel='Path length', yticks=range(0, 13))
ax.legend(labels=['1st and 99th percentiles'], loc='best')
plt.savefig('e1_box.pdf')
plt.show()

#path length: KDE plot
g=sns.displot(data=e1_res_df, x='nStep', hue="nNode", palette='muted',
                kind='kde', clip=(0, 15), bw_method=1)
g.set(xlabel='Path length', ylabel='Kernel density')
g._legend.set_title('Number of nodes')
plt.savefig('e1_kde.pdf')
plt.show()


#%%
#get the mean number of timeout and percentiles
timeout_mean=e2_res_df.groupby(by=['prob'])['nTimeout'].mean()
timeout_1st=e2_res_df.groupby(by=['prob'])['nTimeout'].quantile(0.1)
timeout_99th=e2_res_df.groupby(by=['prob'])['nTimeout'].quantile(0.99)


# %%



# %%
