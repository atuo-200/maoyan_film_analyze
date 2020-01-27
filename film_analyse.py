# -*- coding: gbk -*-
#è�۵�Ӱ�����ݷ���
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "./maoyan.csv"
#index_col = False��ʾ���ѵ�һ����Ϊ����
df = pd.read_csv(path,sep=",",encoding="utf-8",index_col=False)

#ɾ����һ������
df.drop(df.columns[0],axis = 1,inplace = True)

#ɾ���հ�ֵ
df.dropna(inplace=True)

#ɾ���ظ�ֵ
df.drop_duplicates(inplace=True)

#�鿴����
#print(df)
#print(df.info())
#print(df.columns)
#print(df.shape)

#����ȫ����������
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

#ʹ��plt.subplots()����һ��Ԫ�飬����һ���������󣬺������������
fig,ax = plt.subplots(figsize=(9,6),dpi=70)
#ɸѡ�����С��2018�ĵ�Ӱ��Ϣ����ѡ����ӳʱ����һ�н�����Ŀͳ�ƣ�ͳ�Ƴ�2018ǰ����ĵ�Ӱ��Ŀ,�ٰ�index�����������У��õõ���������ָ����ͼ�ϻ�ͼ
ax.set_xlabel('ʱ�䣨�꣩')
ax.set_ylabel('��ӳ����')
ax.set_title('��ӳʱ��&��ӳ�ĵ�Ӱ��Ŀ')
df[df['��ӳʱ��']<2018]['��ӳʱ��'].value_counts().sort_index().plot(kind = "line",ax = ax)

#����ͼƬ������show֮ǰ
plt.savefig('img1.jpg')
plt.show()

#��¼һ��bug�������https://stackoverflow.com/questions/48079316/python-error-tuple-index-out-of-range-when-plotting-pandas-columns-x-vs-y
#��ʽ��list()ת��x,��֤��y��Ϊ�б������׳�tuple index out of range����
x=list(df[df['��ӳʱ��']<2018]['��ӳʱ��'].value_counts().sort_index().index)
y=df[df['��ӳʱ��']<2018]['��ӳʱ��'].value_counts().sort_index().values
y2=df[df['��ӳʱ��']<2018].sort_values(by='��ӳʱ��').groupby('��ӳʱ��').mean()['����'].values

fig,ax=plt.subplots(figsize=(10,5),dpi=70)
ax.plot(x,y,label='��ӳ����')
ax.set_xlim(1980,2017)
ax.set_xlabel('��ӳʱ��')
ax.set_ylabel('��ӳ����')
ax.set_title('ʱ��&��ӳ����&���־�ֵ')

ax2=ax.twinx()
ax2.plot(x,y2,c='y',ls='--',label='����')
#����ͼ����locΪλ��
ax.legend(loc=1)
ax2.legend(loc=2)

plt.savefig('img2.jpg')
plt.show()


fig,ax=plt.subplots(figsize=(10,7),dpi=60)
#df[df['����']>0].groupby('��ӳʱ��').mean()['����']����һ��series��indexΪ��ݣ�valuesΪ���֣������series���л�ͼ
df[df['����']>0].groupby('��ӳʱ��').mean()['����'].plot(kind='line',ax=ax)
ax.set_ylabel('����')
ax.set_title('����&��ӳʱ��&��ֵ����')
plt.savefig("img3.jpg")
plt.show()

fig,ax=plt.subplots(figsize=(10,7),dpi=60)
df[df['����']>0].groupby('��ӳʱ��').mean()['����'].plot(kind='line',ax=ax)
ax.set_ylabel('����')
ax.set_title('����&��ӳʱ��&��ֵ����')
plt.savefig("img4.jpg")
plt.show()

#ͳ�Ƶ�Ӱ�����͵���Ŀ����������ͼ
types=[]
for tp in df['����']:
    ls=tp.split(',')
    for x in ls:
        types.append(x)
tp_df=pd.DataFrame({'����':types})
fig,ax=plt.subplots(figsize=(9,6),dpi=60)
tp_df['����'].value_counts().plot(kind='bar',ax=ax)
ax.set_xlabel('����')
ax.set_ylabel('����')
ax.set_title('����&����&��Ŀ')
plt.savefig("img5.jpg")
plt.show()

#ӰƬʱ�������ֵ�ɢ��ֲ�ͼ
x=df[df['����']>0].sort_values(by='ʱ��(min)')['ʱ��(min)'].values
y=df[df['����']>0].sort_values(by='ʱ��(min)')['����'].values
fig,ax=plt.subplots(figsize=(9,6),dpi=70)
ax.scatter(x,y,alpha=0.6,marker='o')
ax.set_xlabel('ʱ��(min)')
ax.set_ylabel('����')
ax.set_title('ӰƬʱ��&���ֲַ�ͼ')
plt.savefig("img6.jpg")
plt.show()

#ɸѡ�������к��й��ĵ�Ӱ��Ϣ
china_df = df[df['����'].str.contains("�й�")]
#����index����
china_df.reset_index(inplace=True)

# �й�&�����ֵ���ֱȽ� ʱ�䷶Χ��1980-2017
x1 = list(df[df['����'] > 0].groupby('��ӳʱ��').mean()['����'].index)
y1 = df[df['����'] > 0].groupby('��ӳʱ��').mean()['����'].values
x2 = list(china_df[china_df['����'] > 0].groupby('��ӳʱ��').mean()['����'].index)
y2 = china_df[china_df['����'] > 0].groupby('��ӳʱ��').mean()['����'].values
fig,ax = plt.subplots(figsize=(12, 9), dpi=60)
ax.plot(x1, y1, ls='-', c='DarkTurquoise', label='����')
ax.plot(x2, y2, ls='--', c='Gold', label='�й�')
ax.set_title('�й�&�����ֵ����')
ax.set_xlabel('ʱ��')
ax.set_xlim(1980, 2017)
ax.set_ylabel('����')
ax.legend()
plt.savefig("img7.jpg")
plt.show()

print(df["����"])

#�й�&����ӰƬ���ͱȽ�����ͼ

#�Զ��庯��ͳ��������й��ĸ����͵�Ӱ��Ŀ
def cuttig_type(typeS):
    types=[]
    types1=[]
    for x in typeS:
        if len(x)<4:
            # print x
            types1.append(x)
        ls=x.split(',')
        for i in ls:
            types.append(i)
    #��չ����
    types.extend(types1)
    #�ϳ�DataFrame
    type_df=pd.DataFrame({'����':types})
    return pd.DataFrame(type_df['����'].value_counts().sort_values(ascending=False))

df1=cuttig_type(china_df['����'])
df2=cuttig_type(df['����'])
#�ϲ�series
trans=pd.concat([df1,df2],axis=1)

trans.dropna(inplace=True)
trans.columns=['�й�','����']
fig,ax=plt.subplots(figsize=(15,9),dpi=80)
trans.plot(kind='bar',ax=ax)
#��бx���ǩ30��
fig.autofmt_xdate(rotation=30)
ax.set_title('�й�&�������ͶԱ�ͼ')
ax.set_xlabel('����')
ax.set_ylabel('ӰƬ����Ŀ')
plt.savefig("img8.jpg")
plt.show()

#Ȼ�����ɢ��ֲ��ˣ��й�&����&ʱ��&���ֲַ�
y = df[df['����'] > 0].sort_values(by='ʱ��(min)')['����'].values
x = df[df['����'] > 0].sort_values(by='ʱ��(min)')['ʱ��(min)'].values
y2 = china_df[china_df['����'] > 0].sort_values(by='ʱ��(min)')[u'����'].values
x2 = china_df[china_df['����'] > 0].sort_values(by='ʱ��(min)')['ʱ��(min)'].values
fig, ax = plt.subplots(figsize=(10,7), dpi=80)
ax.scatter(x, y, c='DeepSkyBlue', alpha=0.6, label=u'����')
ax.scatter(x2, y2, c='Salmon', alpha=0.7, label=u'�й�')
ax.set_title('�й�&�������ֲַ����')
ax.set_xlabel('ʱ��(min)')
ax.set_ylabel('����')
ax.legend(loc=4)
plt.savefig("img8.jpg")
plt.show()

#����1980�굽2019��ĵ�Ӱ��Ϣ����ʾ
df=df.sort_index(by='��ӳʱ��')
dfs=df[(df['��ӳʱ��']>1980)&(df['��ӳʱ��']<2019)]
print(dfs)

#�鿴1980�굽2019����ӳ�ĵ�Ӱ����+���
for x in range(0,len(dfs)):
    print(dfs.iat[x,0],dfs.iat[x,-1])
