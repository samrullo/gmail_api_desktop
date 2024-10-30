import datetime

to_str = datetime.datetime.strftime


def to_yyyymmdd(date):
    return to_str(date, '%Y%m%d')


def to_yyyymmdd_with_hyphen(date):
    return to_str(date, '%Y-%m-%d')


def to_mmddyyyy_with_slash(date):
    return to_str(date, '%m/%d/%Y')
