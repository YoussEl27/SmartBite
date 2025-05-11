import streamlit as st

st.markdown("""
<style>
.block-container { text-align: center; }
img { transform: rotate(-15deg); padding: 7em; }
</style>
""", unsafe_allow_html=True)

st.title('3, 2, 1, ... Lift off')
st.image("rocket.png")
st.caption("Your first Streamlit app is running.")
st.write("Now, make it your own!")