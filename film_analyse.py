# -*- coding: gbk -*-
#猫眼电影网数据分析
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "./maoyan.csv"
#index_col = False表示不把第一列作为索引
df = pd.read_csv(path,sep=",",encoding="utf-8",index_col=False)

#删除第一列数据
df.drop(df.columns[0],axis = 1,inplace = True)

#删除空白值
df.dropna(inplace=True)

#删除重复值
df.drop_duplicates(inplace=True)

#查看数据
#print(df)
#print(df.info())
#print(df.columns)
#print(df.shape)

#设置全局中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

#使用plt.subplots()返回一个元组，包含一个画布对象，和坐标对象数组
fig,ax = plt.subplots(figsize=(9,6),dpi=70)
#筛选出年份小于2018的电影信息，再选择上映时间这一列进行数目统计，统计出2018前各年的电影数目,再按index索引排序序列，拿得到的序列在指定子图上绘图
ax.set_xlabel('时间（年）')
ax.set_ylabel('上映数量')
ax.set_title('上映时间&上映的电影数目')
df[df['上映时间']<2018]['上映时间'].value_counts().sort_index().plot(kind = "line",ax = ax)

#保存图片必须在show之前
plt.savefig('img1.jpg')
plt.show()

#记录一个bug，解决：https://stackoverflow.com/questions/48079316/python-error-tuple-index-out-of-range-when-plotting-pandas-columns-x-vs-y
#显式用list()转换x,保证和y都为列表，否则抛出tuple index out of range错误
x=list(df[df['上映时间']<2018]['上映时间'].value_counts().sort_index().index)
y=df[df['上映时间']<2018]['上映时间'].value_counts().sort_index().values
y2=df[df['上映时间']<2018].sort_values(by='上映时间').groupby('上映时间').mean()['评分'].values

fig,ax=plt.subplots(figsize=(10,5),dpi=70)
ax.plot(x,y,label='上映数量')
ax.set_xlim(1980,2017)
ax.set_xlabel('上映时间')
ax.set_ylabel('上映数量')
ax.set_title('时间&上映数量&评分均值')

ax2=ax.twinx()
ax2.plot(x,y2,c='y',ls='--',label='评分')
#放置图例，loc为位置
ax.legend(loc=1)
ax2.legend(loc=2)

plt.savefig('img2.jpg')
plt.show()


fig,ax=plt.subplots(figsize=(10,7),dpi=60)
#df[df['评分']>0].groupby('上映时间').mean()['评分']返回一个series，index为年份，values为评分，用这个series进行绘图
df[df['评分']>0].groupby('上映时间').mean()['评分'].plot(kind='line',ax=ax)
ax.set_ylabel('评分')
ax.set_title('世界&上映时间&均值评分')
plt.savefig("img3.jpg")
plt.show()

fig,ax=plt.subplots(figsize=(10,7),dpi=60)
df[df['评分']>0].groupby('上映时间').mean()['评分'].plot(kind='line',ax=ax)
ax.set_ylabel('评分')
ax.set_title('世界&上映时间&均值评分')
plt.savefig("img4.jpg")
plt.show()

#统计电影各类型的数目，绘制条形图
types=[]
for tp in df['类型']:
    ls=tp.split(',')
    for x in ls:
        types.append(x)
tp_df=pd.DataFrame({'类型':types})
fig,ax=plt.subplots(figsize=(9,6),dpi=60)
tp_df['类型'].value_counts().plot(kind='bar',ax=ax)
ax.set_xlabel('类型')
ax.set_ylabel('数量')
ax.set_title('世界&类型&数目')
plt.savefig("img5.jpg")
plt.show()

#影片时长和评分的散点分布图
x=df[df['评分']>0].sort_values(by='时长(min)')['时长(min)'].values
y=df[df['评分']>0].sort_values(by='时长(min)')['评分'].values
fig,ax=plt.subplots(figsize=(9,6),dpi=70)
ax.scatter(x,y,alpha=0.6,marker='o')
ax.set_xlabel('时长(min)')
ax.set_ylabel('评分')
ax.set_title('影片时长&评分分布图')
plt.savefig("img6.jpg")
plt.show()

#筛选出地区中含中国的电影信息
china_df = df[df['地区'].str.contains("中国")]
#重置index索引
china_df.reset_index(inplace=True)

# 中国&世界均值评分比较 时间范围在1980-2017
x1 = list(df[df['评分'] > 0].groupby('上映时间').mean()['评分'].index)
y1 = df[df['评分'] > 0].groupby('上映时间').mean()['评分'].values
x2 = list(china_df[china_df['评分'] > 0].groupby('上映时间').mean()['评分'].index)
y2 = china_df[china_df['评分'] > 0].groupby('上映时间').mean()['评分'].values
fig,ax = plt.subplots(figsize=(12, 9), dpi=60)
ax.plot(x1, y1, ls='-', c='DarkTurquoise', label='世界')
ax.plot(x2, y2, ls='--', c='Gold', label='中国')
ax.set_title('中国&世界均值评分')
ax.set_xlabel('时间')
ax.set_xlim(1980, 2017)
ax.set_ylabel('评分')
ax.legend()
plt.savefig("img7.jpg")
plt.show()

print(df["类型"])

#中国&世界影片类型比较条形图

#自定义函数统计世界和中国的各类型电影数目
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
    #扩展数组
    types.extend(types1)
    #合成DataFrame
    type_df=pd.DataFrame({'类型':types})
    return pd.DataFrame(type_df['类型'].value_counts().sort_values(ascending=False))

df1=cuttig_type(china_df['类型'])
df2=cuttig_type(df['类型'])
#合并series
trans=pd.concat([df1,df2],axis=1)

trans.dropna(inplace=True)
trans.columns=['中国','世界']
fig,ax=plt.subplots(figsize=(15,9),dpi=80)
trans.plot(kind='bar',ax=ax)
#倾斜x轴标签30°
fig.autofmt_xdate(rotation=30)
ax.set_title('中国&世界类型对比图')
ax.set_xlabel('类型')
ax.set_ylabel('影片的数目')
plt.savefig("img8.jpg")
plt.show()

#然后就是散点分布了，中国&世界&时长&评分分布
y = df[df['评分'] > 0].sort_values(by='时长(min)')['评分'].values
x = df[df['评分'] > 0].sort_values(by='时长(min)')['时长(min)'].values
y2 = china_df[china_df['评分'] > 0].sort_values(by='时长(min)')[u'评分'].values
x2 = china_df[china_df['评分'] > 0].sort_values(by='时长(min)')['时长(min)'].values
fig, ax = plt.subplots(figsize=(10,7), dpi=80)
ax.scatter(x, y, c='DeepSkyBlue', alpha=0.6, label=u'世界')
ax.scatter(x2, y2, c='Salmon', alpha=0.7, label=u'中国')
ax.set_title('中国&世界评分分布情况')
ax.set_xlabel('时长(min)')
ax.set_ylabel('评分')
ax.legend(loc=4)
plt.savefig("img8.jpg")
plt.show()

#查找1980年到2019年的电影信息并显示
df=df.sort_index(by='上映时间')
dfs=df[(df['上映时间']>1980)&(df['上映时间']<2019)]
print(dfs)

#查看1980年到2019年上映的电影名字+年份
for x in range(0,len(dfs)):
    print(dfs.iat[x,0],dfs.iat[x,-1])
