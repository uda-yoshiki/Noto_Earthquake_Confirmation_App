import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from datetime import datetime, timedelta

# 日本語フォントの設定
rcParams['font.family'] = 'meiryo ui'

# 緯度経度を数値に変換する関数
def convert_to_float(deg_str):
    if '°' in deg_str and '’' in deg_str:
        degrees, minutes = deg_str.split('°')
        minutes = minutes.replace('’', '')
        return float(degrees) + float(minutes) / 60
    else:
        return None

# データの読み込みと前処理
df = pd.read_csv('data/zishin.csv', names=["発震日時", "緯度", "経度", "深さ(Km)", "マグニチュード", "震源地名", "地震名", "観測地点", "震央距離(Km)", "最大加速度南北(Gal)", "最大加速度東西(Gal)", "最大加速度上下(Gal)", "ＰＳＩ値南北(cm・s^-1/2)", "ＰＳＩ値東西(cm・s^-1/2)", "ＰＳＩ値上下(cm・s^-1/2)", "記録番号", "記録（波形）データ（オリジナル）", "記録（波形）データ（補正）", "記録（波形）データ（ＳＭＡＣ相当）"], skiprows=1)
df["緯度"] = df["緯度"].apply(convert_to_float)
df["経度"] = df["経度"].apply(convert_to_float)
df["マグニチュード"] = pd.to_numeric(df["マグニチュード"], errors='coerce')
df["発震日時"] = pd.to_datetime(df["発震日時"])

# フィルタ機能の追加
st.sidebar.title("フィルター")
default_start_date = datetime.now() - timedelta(days=30)
default_end_date = datetime.now()
start_date, end_date = st.sidebar.date_input("発震日時で絞り込む", [default_start_date, default_end_date])
df = df[(df["発震日時"] >= pd.to_datetime(start_date)) & (df["発震日時"] <= pd.to_datetime(end_date))]

# グラフのスタイルを設定
sns.set(style="whitegrid")

# マグニチュードの分布を表示
st.subheader("マグニチュードの分布")
fig, ax = plt.subplots()
sns.histplot(df["マグニチュード"].dropna(), bins=30, kde=True, color="skyblue", ax=ax)
ax.set_title("マグニチュードの分布", fontsize=16)
st.pyplot(fig)

# 地震の深さの分布を表示
st.subheader("地震の深さの分布")
fig, ax = plt.subplots()
sns.histplot(df["深さ(Km)"].dropna(), bins=30, kde=True, color="lightgreen", ax=ax)
ax.set_title("地震の深さの分布", fontsize=16)
st.pyplot(fig)

# マグニチュードと深さの関係を表示
st.subheader("マグニチュードと深さの関係")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="深さ(Km)", y="マグニチュード", hue="マグニチュード", palette="coolwarm", ax=ax)
ax.set_title("マグニチュードと深さの関係", fontsize=16)
st.pyplot(fig)

# 地震の発生時間の分布を表示
st.subheader("地震の発生時間の分布")
df["時間"] = df["発震日時"].dt.hour
fig, ax = plt.subplots()
sns.histplot(df["時間"].dropna(), bins=24, kde=False, color="violet", ax=ax)
ax.set_title("地震の発生時間の分布", fontsize=16)
st.pyplot(fig)

# 地震の発生地点の分布を表示
st.subheader("地震の発生地点の分布")
fig = plt.figure()
sns.scatterplot(data=df, x="経度", y="緯度", size="マグニチュード", sizes=(20, 200), hue="マグニチュード", palette="coolwarm")
plt.title("地震の発生地点の分布", fontsize=16)
st.pyplot(fig)
