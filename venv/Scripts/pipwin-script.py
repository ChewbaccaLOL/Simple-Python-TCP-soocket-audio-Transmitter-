#!C:\Users\volko\PycharmProjects\netw(laba1)\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pipwin==0.4.9','console_scripts','pipwin'
__requires__ = 'pipwin==0.4.9'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pipwin==0.4.9', 'console_scripts', 'pipwin')()
    )
