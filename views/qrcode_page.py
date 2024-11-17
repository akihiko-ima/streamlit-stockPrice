import streamlit as st
import qrcode
from PIL import Image
import io


def qrcode_page():
    # ユーザー名とパスワードの入力フォーム
    st.header("QRコード生成", divider="blue")

    text_input = st.text_input(
        "QRコードに埋め込むテキストを入力してください：", value="Hello, QR Code!"
    )

    version_input = st.number_input(
        "QRコードのバージョンを入力してください (1～40の整数)：",
        min_value=1,
        max_value=40,
        value=1,
        step=1,
    )

    if st.button("QRコードを生成", type="primary"):
        try:
            qr = qrcode.QRCode(
                version=version_input,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text_input)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Pillowでリサイズ (幅または高さを640px以下に制限)
            max_size = 480
            img = img.resize((max_size, max_size), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            st.image(
                Image.open(buffer),
                caption="生成されたQRコード",
                use_container_width=True,
            )

            st.download_button(
                label="QRコードをダウンロード",
                data=buffer,
                file_name="qrcode.png",
                mime="image/png",
            )
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
