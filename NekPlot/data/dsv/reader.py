import pandas

def ReadDSV(fpath, **kwargs):
    sep = kwargs.pop('delimiter',',')
    return pandas.read_csv(fpath, sep=sep, **kwargs)