def clean_filename(filename):
    if not filename:
        return filename
    exclusions = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '+']
    filename = ''.join(s for s in filename if s not in exclusions)
    return filename.rstrip()
