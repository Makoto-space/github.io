# 本ファイルの位置づけ
本ファイルはデプロイする前にローカル環境で動作確認したものです。実際はこの後にDockerでコンテナ化して、Google Cloud Run上にデプロイしました。その時はDockerfile, requirements.txt, サービスアカウントキーファイルを作成してアップロードしました。今回はこれらのデプロイ時に用いたファイルは公開していません。

# 発疹画像分類の学習
5つの疾患（アトピー性皮膚炎、はしか、手足口病、水ぼうそう、帯状疱疹）の画像ファイルは、Makoto-space/Photos-of-skin-diseasesリポジトリに入っています。5つのフォルダをColaboratoryのMyDrive/medical foldersに置いて学習させました。

# 発疹画像の適格性確認の学習
5つの疾患（アトピー性皮膚炎、はしか、手足口病、水ぼうそう、帯状疱疹）の画像ファイルは、Makoto-space/Photos-of-skin-diseasesリポジトリに入っています。5つのフォルダをColaboratoryのMyDrive/medical foldersに置いて学習させました。

# 症例テキスト分類の学習
5つの疾患（アトピー性皮膚炎、はしか、手足口病、水ぼうそう、帯状疱疹）の症例テキストは本リポジトリの症例テキストフォルダに入っています。5つのエクセルファイルをColaboratoryの/Contentフォルダに取り込んでから各100例の症例テキストを作成して学習に使用しました。

# ライブラリのバージョン
2025-5-1に動作確認したところ、エラーが出た（原因はnumpy2.0となり、np.Infがなくなってnp.infが使われるようになった）ため、numpy==1.25, pytorch_lightning==1.9.4に修正しました。

# main.py(FastAPI), app.py(streamlit)の動作確認
Visual Studio Codeで仮想環境を作成して、3つの学習済モデルをパソコンのフォルダに置いて、uvicornで動かしました。仮想環境にインストールされている全てのパッケージをrequirements.txtに記しました。
