from google.cloud import texttospeech
import streamlit as st


def synthesize_speech(text, lang='日本語'):
    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    return response

st.title('音声出力アプリ')

st.markdown('### データ準備')

input_option = st.selectbox(
    '入力データの選択',
    ('直接入力', 'テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力してください。', 'Cloud Speech-to-Text用のサンプル文になります。')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.markdown('入力データ')
    st.write(input_data)
    st.markdown('### パラメータ設定')
    st.subheader('言語の選択')

    lang = st.selectbox(
        '言語の選択', 
        ('日本語', '英語')
    )
    st.markdown('### 音声合成')
    st.write('こちらの文章で音声ファイルの生成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        response = synthesize_speech(input_data, lang = lang)
        st.audio(response.audio_content)
        comment.write('完了しました')