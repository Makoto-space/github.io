import streamlit as st
import requests
import pandas as pd
from PIL import Image
import io

st.title("写真")
st.write("#### 患者様の発疹画像の選択をお願いいたします。")
# Streamlitのファイルアップローダー
uploaded_file = st.file_uploader("***発疹画像ファイルを以下のBrowse filesボタンから選択してください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # ファイルをFastAPIに送信
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    response = requests.post("http://localhost:8000/uploadfile/", files=files)
    
    # 画像を表示
    image = Image.open(io.BytesIO(uploaded_file.getvalue()))
    # 画像を縮小（20分の1に）
    width, height = image.size
    new_size = (width // 20, height // 20)
    resized_image = image.resize(new_size)
    # 画像をStreamlitで表示
    st.image(resized_image, caption='送付画像')

    # 回答があった場合に確率の情報を入手
    if response.status_code == 200:
        answer = response.json()
        numbers = answer['prediction'][0]
        check = answer['confirmation']
        
        # 数値をパーセント表示に変換する関数の定義
        def convert_to_percentage(numbers):
            return ["{:.1%}".format(num) for num in numbers]

        # 数値をパーセントに変換して表示
        percentages = convert_to_percentage(numbers)
        pred_df = pd.DataFrame([percentages], columns=['はしか','アトピー性皮膚炎','帯状疱疹','手足口病','水ぼうそう'], index=['確率'])
        # 最も確率の高い疾患を特定し、対象内の画像のみを選別する工程を入れて表示
        name = pred_df.idxmax(axis=1).tolist()
        st.write('##### 画像の判定結果')
        if check == "accept":
            st.write(pred_df)
            st.write('この発疹は、',str(name[0]),'の可能性があります。')  
            if max(numbers) < 0.75:
                st.write('ただし判定結果の確率があまり高くないので典型的な',str(name[0]),'の発疹ではありません。他の皮膚疾患の可能性もあります。')

        else:
            st.write('対象の5つの皮膚疾患の典型的な発疹画像と異なるため、判定できませんでした。')
 
    else:
        st.write("ファイルのアップロードに失敗しました。")

st.write("")

st.title("問診票")
st.write("#### 患者様の情報のご入力をお願いいたします。")
number = st.number_input("***年齢を入力して下さい", value=0, min_value=0, max_value=100, step=1)
sex = st.selectbox(
    "***性別を入力して下さい。",
    ("男性", "女性"),
    index=None,
    placeholder="選択してください。",
)
number2 = st.number_input("***体温を入力して下さい。", value=35.0, min_value=35.0, max_value=43.0, step=0.1, format="%.1f")
rounded_number2 = round(number2, 1)
st.write("")
st.markdown('<p style="font-size:16px;">***発疹のある部位を全てチェックして下さい。</p>', unsafe_allow_html=True)
# 複数の選択肢をリストで定義
options = ["顔", "首", "口", "肩、胸", "お腹", "背中", "腕", "手のひら", "足"]

# 各選択肢に対してチェックボックスを作成
selected_options = []
for option in options:
    if st.checkbox(option):
        selected_options.append(option)

# 選択されたオプションをカンマ区切りの文字列に変換
selected_options_str = "、".join(selected_options)
st.write("")
st.markdown('<p style="font-size:16px;">***発疹についてあてはまるものを全てチェックして下さい。</p>', unsafe_allow_html=True)
# 複数の選択肢をリストで定義
options2 = ["発疹は体の片側にある", "発疹は帯状になっている", "発疹はピリピリする痛みがある", "発疹は夜間に痛みが強くなる", "発疹はかゆみがある", "水ぶくれがある", "発疹やかさぶたが混在する", "発疹は手のひらや足の裏にある", "発疹は左右対称である"]

# 各選択肢に対してチェックボックスを作成
selected_options2 = []
for option2 in options2:
    if st.checkbox(option2):
        selected_options2.append(option2)

# 選択されたオプションをカンマ区切りの文字列に変換
selected_options2_str = "。".join(selected_options2)

st.write("")
st.markdown('<p style="font-size:16px;">***発疹以外の症状についてあてはまるものを全てチェックして下さい。</p>', unsafe_allow_html=True)
# 複数の選択肢をリストで定義
options3 = ["発疹が出る前にピリピリする痛みがあった", "ものを飲み込むときに痛みがある", "口の中に白い斑点がある", "せき、鼻水、目やに", "くしゃみ、のどの痛み", "目の充血", "頭痛", "倦怠感", "便秘や排尿困難がある"]

# 各選択肢に対してチェックボックスを作成
selected_options3 = []
for option3 in options3:
    if st.checkbox(option3):
        selected_options3.append(option3)

# 選択されたオプションをカンマ区切りの文字列に変換
selected_options3_str = "、".join(selected_options3)
st.write("")

# 自由記述欄を作成
free_description = st.text_area("***ここに自由記述してください")

st.write("")
st.write("")
st.write("###### ***患者様の情報は以下でよろしいでしょうか？よろしければ”送信する”ボタンをクリックして下さい。")
st.write(f"{number}歳の{sex}です。体温は{rounded_number2}℃です。発疹の部位は、{selected_options_str}です。{selected_options2_str}。他の症状は、{selected_options3_str}です。{free_description}")
if rounded_number2 > 36.9:
    text = f"{number}歳の{sex}。発熱は{rounded_number2}℃。発疹は{selected_options_str}。{selected_options2_str}。{selected_options3_str}。{free_description}"
else:
    text = f"{number}歳の{sex}。発疹は{selected_options_str}。{selected_options2_str}。{selected_options3_str}。{free_description}"

# FastAPIにデータを送信
if st.button("送信する"):
    response = requests.post("http://localhost:8000/propose/", json={"text": text})
    if response.status_code == 200:
        result = response.json()
        ratios = result['expectation'][0]

        # 数値をパーセント表示に変換する関数の定義
        def convert_to_percentage2(ratios):
            return ["{:.1%}".format(ratio) for ratio in ratios]

        # 数値をパーセントに変換して表示
        percentages2 = convert_to_percentage2(ratios)
        pred_df2 = pd.DataFrame([percentages2], columns=['はしか','アトピー性皮膚炎','帯状疱疹','手足口病','水ぼうそう'], index=['確率'])
        # 最も確率の高い疾患を特定して表示
        name2 = pred_df2.idxmax(axis=1).tolist()
        st.write('##### 症状の判定結果')
        st.write(pred_df2)
        st.write('この症状は、',str(name2[0]),'の可能性があります。')    
      
    else:
        st.write('##### 症状の判定結果')
        st.write("解析に失敗しました。")