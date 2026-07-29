# Skin Disease Candidate Suggestion Web App

> **Project status:** Earlier portfolio project. This repository is not under active feature development, although minor documentation and maintenance updates may still be made.
>
> **Medical disclaimer:** This project is an educational and research prototype. It is not intended for clinical diagnosis, treatment selection, medical decision-making, or use as a medical device.

An experimental web application that combines a skin image and symptom information to suggest one of five candidate disease categories.

## Overview

The prototype was developed to explore whether image analysis and symptom-text classification could help distinguish several common or clinically important rash-related conditions.

The application accepts:

1. a skin image captured by the user; and
2. symptom information entered through a questionnaire.

It then uses three trained components:

- skin-image classification;
- image suitability checking; and
- symptom-text classification.

The supported candidate categories are:

| Candidate category | Japanese |
|---|---|
| Atopic dermatitis | アトピー性皮膚炎 |
| Measles | はしか |
| Hand, foot, and mouth disease | 手足口病 |
| Chickenpox | 水ぼうそう |
| Herpes zoster | 帯状疱疹 |

Because the model is limited to these five categories, its output must not be interpreted as a comprehensive differential diagnosis.

## Project Scope

This repository contains files used to verify the application in a local environment before deployment.

The deployment version was containerized and published on Google Cloud Run using separate FastAPI and Streamlit containers. Deployment-specific files and credentials are not included in this public repository.

## Training Components

### 1. Skin-image classification

The medical images used in the historical experiment are not redistributed in the public repository. Access to source images is subject to the original providers' licenses, terms of use, privacy requirements, and other applicable restrictions.

Training was performed in Google Colaboratory.

### 2. Image suitability checking

A separate model was trained to identify images that differ from the typical rash images used for the five supported categories.

Its purpose is to return an “unable to classify” response when an input image is outside the intended scope of the prototype.

### 3. Symptom-text classification

The repository includes symptom-text files for the five supported categories.

Five Excel files were imported into Google Colaboratory, and 100 case-text examples per category were used for training.

## Application Components

- `main.py`: FastAPI application
- `app.py`: Streamlit user interface
- `requirements.txt`: Python dependencies used in the local verification environment
- Three trained model files are required for local execution

## Historical Local Execution Outline

The following is a general execution outline. Model-file paths and environment-specific settings may need to be adjusted to match the repository configuration.

**Note:** The trained model files required by `main.py` and `app.py` are not included. The models are withheld because the historical training medical images were assembled from multiple external sources with differing copyright, licensing, and privacy conditions. The commands below document the historical execution procedure but are not sufficient to run the complete application.

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m uvicorn main:app --reload
```

Open a second terminal, activate the same virtual environment, and start Streamlit:

```cmd
.venv\Scripts\activate.bat
python -m streamlit run app.py
```

On Linux, macOS, or WSL, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Compatibility Note

The project was checked on **2025-05-01**. A compatibility problem occurred after the NumPy 2.0 change from `np.Inf` to `np.inf`.

The local environment was therefore adjusted to:

```text
numpy==1.25
pytorch_lightning==1.9.4
```

These versions reflect the historical project environment and may not represent current recommended versions.

## Demo

An earlier version of this prototype was deployed on Google Cloud Run.

The public demo is currently unavailable because cloud hosting has been discontinued. The source code and project documentation remain availablein this repository.

## Application Screenshots

The screenshots show an earlier working version of the application.

The public Google Cloud Run deployment is no longer active. These images are provided to demonstrate the historical user interface and application workflow.

## Security and Privacy

- No passwords, API keys, service-account keys, or other credentials should be committed to this repository.
- Deployment credentials must be managed outside the source repository.
- Do not submit identifiable patient information or private medical images.
- Before reusing external images, confirm their licenses, terms of use, and privacy requirements.

## Limitations

- The prototype supports only five candidate categories.
- It does not cover the full range of dermatological or systemic diseases that can cause a rash.
- Model outputs may be incorrect, incomplete, or affected by image quality and input wording.
- The repository does not document prospective clinical validation.
- The application must not replace evaluation by a qualified healthcare professional.

## Disclaimer

This project is provided solely as an educational and research portfolio example.

It is not intended to:

- diagnose a disease;
- recommend treatment;
- determine whether medical care is necessary;
- replace a physician or other qualified healthcare professional; or
- function as a regulated medical device.

Anyone with a rash or other health concern should consult a qualified healthcare professional.

<details>
<summary><strong>Japanese / 日本語</strong></summary>

## 概要

本プロジェクトは、皮膚画像と問診情報を組み合わせて、次の5つの疾患カテゴリーの候補を提示する教育・研究目的の試作Webアプリです。

- アトピー性皮膚炎
- はしか
- 手足口病
- 水ぼうそう
- 帯状疱疹

利用者が入力した皮膚画像と症状情報に対して、以下の3つの学習済みモデルを使用します。

- 発疹画像分類
- 入力画像の適格性確認
- 症例テキスト分類

対象は5カテゴリーに限定されているため、出力を包括的な鑑別診断として解釈することはできません。

## リポジトリの位置づけ

本リポジトリには、デプロイ前にローカル環境で動作確認したファイルを収録しています。

デプロイ版では、FastAPIとStreamlitを別々のコンテナとしてDocker化し、Google Cloud Runへ配置しました。デプロイ固有のファイルおよび認証情報は、この公開リポジトリには含めていません。

## 学習内容

### 発疹画像分類

過去の実験で使用した医療画像は、公開リポジトリでは再配布していません。元画像の利用については、各提供元のライセンス、利用規約、プライバシー要件その他の条件に従う必要があります。

学習はGoogle Colaboratoryで実施しました。

### 入力画像の適格性確認

5カテゴリーの典型的な発疹画像と異なる画像が入力された場合に、判定対象外として扱うことを目的としたモデルです。

### 症例テキスト分類

5カテゴリーについて、各100例の症例テキストを作成し、Google Colaboratoryで学習に使用しました。

### 過去のローカル実行手順

注: main.py と app.py で必要となる学習済みモデルファイルは、本リポジトリには含まれていません。過去の学習に用いた医療画像データは、著作権、ライセンス、プライバシー条件が異なる複数の外部情報源から収集したため、学習済みモデルの公開を控えています。そのため、公開されているファイルだけでは、推論アプリケーションを完全に実行することはできません。

## プロジェクトの状態

本プロジェクトは以前に作成したポートフォリオ作品であり、現在、新機能の積極的な開発は行っていません。ただし、文書や保守上の軽微な更新を行う場合があります。

## デモ

このプロトタイプの以前のバージョンは、Google Cloud Runへデプロイしていました。現在はクラウドでのホスティングを終了しているため、公開デモは利用できません。ソースコードとプロジェクト文書は、このリポジトリで引き続き閲覧できます。

## アプリケーション画面

掲載したスクリーンショットは、以前正常に動作していたバージョンのアプリケーション画面です。現在、Google Cloud Run上の公開環境は稼働していません。これらの画像は、過去のユーザーインターフェースとアプリケーションの処理の流れを示すために掲載しています。


## 医療上の注意

本プロジェクトは教育・研究目的の試作です。

実際の診断、治療方針の決定、受診判断、医療機器としての使用を目的としていません。健康上の問題がある場合は、医師その他の有資格医療専門職へ相談してください。

</details>

## Repository

- [Source code](https://github.com/Makoto-space/skin-disease-diagnosis-webapp)
