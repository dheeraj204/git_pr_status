import os

extension = ['.log', '.zip']
comment = ['hdsfvgjh', 'hgfsdjhgv', 'fdgg']


def check_logs(extensions=None, comments=None):
    global comment
    if comments is None:
        comments = comment
    if extensions is None:
        extensions = extension
    for ext in extensions:
        res = [comment for comment in comments if ext in comment]
        if len(res) > 0:
            return True


if check_logs():
    print('logs are present')
else:
    print('logs are not present')

