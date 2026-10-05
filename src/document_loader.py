def load_text_file(file):
    text = file.read()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    return text