import os

extension = ['.log', '.zip']
comment = ['hdsfvgjh', 'hgfsdjhgv', 'fdgg.log']


def check_logs(extensions=extension, comments=comment):
    for ext in extensions:
        res = [comment for comment in comments if ext in comment]
        if len(res) > 0:
            return True


if check_logs():
    print('logs are present')
else:
    print('logs are not present')

