from dotenv import load_dotenv
from oai import ask_openai
from chat_result import Chat_Result
import streamlit as st
from PIL import Image



load_dotenv(".env")

_icon = "\U0001F987"

def streamlit_interface():
    st.set_page_config(
        layout="wide",
        page_title="Ask ChatGPT",
        #page_icon="🚀",
        page_icon=_icon
        #page_icon="\U0001F47E"
    )
    st.title('Ask ChatGPT')
    left, right = st.columns(2)
    with left:
        # test picture from https://picsum.photos/images
        # https://fastly.picsum.photos/id/26/4209/2769.jpg?hmac=vcInmowFvPCyKGtV7Vfh7zWcA_Z0kStrPDW3ppP0iGI
        url_input = st.text_input("Enter an URL or upload an image")
        uploaded_file = st.file_uploader(label='Upload image',
                                         type=['.png','.jpg','.jpeg'],
                                         accept_multiple_files=False)
        text_input = st.text_area("Prompt:")
        int_value = st.slider("Max token:", min_value=200, max_value=2000, value=500, step=50)   
        li, re = st.columns(2)     
        if text_input:
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                source = uploaded_file
            elif url_input:
                source = url_input
            else:
                source = None  
            if url_input:
                with re:
                    if st.checkbox("Show image"):
                        st.write('downloading ...')
            with li:
                if st.button("start"):
                    with st.spinner():
                        answer = ask_openai(source=source,prompt=text_input,max=int_value)
                        result = Chat_Result.from_completion(completion=answer)
                        with right:
                            st.subheader(f"Result -------------------  Token: {result.token}")
                            st.write(result.content)



if __name__ == "__main__":
    streamlit_interface()
 