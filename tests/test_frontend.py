import importlib

def test_import_streamlit_app():
    try:
        importlib.import_module("app.pages.app")
    except Exception as e:
        assert False, f"Streamlit app failed to import: {e}"
