import os

extensions = ['.log', '.zip']
comments = ['hdsfvgjh', 'hgfsdjhgv', 'fdgg.zip']


def check_logs():
    for ext in extensions:
        res = [comment for comment in comments if ext in comment]
        if len(res) > 0:
            return True


#
# def check_logs():
#
#     res = [i for i in comments if extensions[0] or extensions[1] in i]
#     if len(res) > 0:
#         return True
#     else:
#         return False
location = 'D:/repo_updates'
if not os.path.isdir(location):
    os.mkdir(location)
if check_logs():
    print('logs are present')
else:
    print('logs are present')

