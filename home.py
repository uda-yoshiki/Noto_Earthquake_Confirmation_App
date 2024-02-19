import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

from datetime import datetime, timedelta

# 緯度経度を数値に変換する関数
def convert_to_float(deg_str):
    if '°' in deg_str and '’' in deg_str:
        degrees, minutes = deg_str.split('°')
        minutes = minutes.replace('’', '')
        return float(degrees) + float(minutes) / 60
    else:
        return None

# CSVから地震情報を取得
df = pd.read_csv('data/zishin.csv', names=["発震日時", "緯度", "経度", "深さ(Km)", "マグニチュード", "震源地名", "地震名", "観測地点", "震央距離(Km)", "最大加速度南北(Gal)", "最大加速度東西(Gal)", "最大加速度上下(Gal)", "ＰＳＩ値南北(cm・s^-1/2)", "ＰＳＩ値東西(cm・s^-1/2)", "ＰＳＩ値上下(cm・s^-1/2)", "記録番号", "記録（波形）データ（オリジナル）", "記録（波形）データ（補正）", "記録（波形）データ（ＳＭＡＣ相当）"], skiprows=1)

# 緯度と経度の列を数値型に変換
df["緯度"] = df["緯度"].apply(convert_to_float)
df["経度"] = df["経度"].apply(convert_to_float)

# マグニチュードの列を数値型に変換
df["マグニチュード"] = pd.to_numeric(df["マグニチュード"], errors='coerce')

# 地震情報を絞り込むための日付選択
st.sidebar.title("フィルター")
# デフォルトを今日から一か月前までに設定
default_start_date = datetime.now() - timedelta(days=30)
default_end_date = datetime.now()
try:
    start_date, end_date = st.sidebar.date_input("発震日時で絞り込む", [default_start_date, default_end_date])
    if start_date and end_date:
        df = df[(pd.to_datetime(df["発震日時"]) >= pd.to_datetime(start_date)) & (pd.to_datetime(df["発震日時"]) <= pd.to_datetime(end_date))]
except ValueError as e:
    st.error("日付の選択が正しくありません。もう一度試してください。")
    st.stop()

# 地図を作成
m = folium.Map(location=[35.6895, 139.6917], zoom_start=5)

# 地震情報を地図に追加し、マグニチュードに応じて色を変更
for _, row in df.iterrows():
    if pd.notnull(row["緯度"]) and pd.notnull(row["経度"]):  # 緯度と経度がNaNでないことを確認
        if row["マグニチュード"] <= 3:
            color = 'green'
        elif row["マグニチュード"] <= 5:
            color = 'orange'
        else:
            color = 'red'
        
        folium.Circle(
            location=[row["緯度"], row["経度"]],
            radius=20000,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"{row['発震日時']} {row['震源地名']} マグニチュード: {row['マグニチュード']}"
        ).add_to(m)

# Streamlitで地図を表示
st.title("地震情報マップ")
st.markdown("""
マップ上の円の色は、地震のマグニチュードの大きさによって変わります。
- <span style="color:green">**緑色の円**</span>はマグニチュード3以下の地震を示しています。
- <span style="color:orange">**オレンジ色の円**</span>はマグニチュードが3を超え5以下の地震を示しています。
- <span style="color:red">**赤色の円**</span>はマグニチュードが5を超える地震を示しています。

この色分けにより、一目で地震の強さを把握することができます。
""", unsafe_allow_html=True)
folium_static(m)

