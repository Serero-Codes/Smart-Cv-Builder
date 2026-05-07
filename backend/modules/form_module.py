from modules.cv_builder import build_cv

def generate_form_cv(data):

    # you can validate here if you want
    file_path = build_cv(data)

    return file_path