from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.


build_options = {
    'packages': [],
    'excludes': 
        [
        "zoneinfo", "sqlite3", "email", "html", "jupyter_client", "jupyter_core", "matplotlib", "numpy"
        ],
    'include_files' : ["Icon/"]
    }

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('aret_ita.py', base=base, target_name = 'Aret')
]

setup(name='ARET',
    version = '1',
    description = 'AmazingRandomExamTutor',
    options = 
            {
                'build_exe': build_options
            },
    executables = executables)
