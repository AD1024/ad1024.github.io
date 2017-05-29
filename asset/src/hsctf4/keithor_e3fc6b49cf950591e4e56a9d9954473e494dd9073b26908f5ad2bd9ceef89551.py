from hashlib import *
from base64 import *

#xydj: vbqw edbo sedjqydi sqfyjqb bujjuhi qdt dkcruhi qdt de ifusyqb sxqhqsjuhi
FLAG = b'{insert flag here}'
FLAG = b64decode(FLAG)

def main():
    n = ''
    n += md5(FLAG).hexdigest()
    n += sha1(FLAG).hexdigest()
    n += sha224(FLAG).hexdigest()
    n += sha256(FLAG).hexdigest()
    n += sha384(FLAG).hexdigest()
    n += sha512(FLAG).hexdigest()

    if b64encode(n.encode()) == b'NGY3OTgwN2E3YzQ3ZjY5N2JkNWYwNmJlZWY5NTVjZmRmNGZkYWVmOGFkZThlZGY3MDc4NThmZTQyOTRkNzgwZDY5ZDRkNmE4OTdkODU5OGNlMzE0MmQyMDc2NDBjYTUxZDgyMTVkMGQ2YzY5Mzg3M2ZkMzJjMWY2ZTQ2ODc1MDAyN2I1ZGIzNGI3ZDljZTBhNzk3NTNlY2M3M2RhNjY0YTk5NTg4OWUwZDM2ZGI0YmZjNjhkZjlmYzhkYTNkMzY5YjI2NmU2MTdhNjE1OGQxNmNjYWQ0MTg5ZjBhM2RjYWU2MmQ5YjEwM2I1MGIwZDQzMzdjOTYxNjM0NzFiNDIzZmMyOGYzY2RhMjk0MTdiNzI4MGViOTMyMTQ5MjA3NWM1ODkwZGMwMzM0NzFjZjkxNzgxYTA3MDAxY2VhNjY5NmIzMmNkZjU2YjIxMjliYzc2YTgzMjE4YmVlNTJjODMwYThiZmMwOWVjNTVhZTM3MjExMGMwY2M4OTUwZWY1NzdkMzJlZDIxMWQ0MDMwN2MzZmQ2Njg0MTEzMzQxZTYwM2M=':
        print('Correct flag!')
    else:
        print('Incorrect flag :(')

main()
