import os
from PyInstaller.utils.hooks import get_package_paths

escpos_pkg_path = get_package_paths("escpos")[1]
datas = [
    (os.path.join(escpos_pkg_path, "capabilities.json"), "escpos"),
    (os.path.join(escpos_pkg_path, "capabilities_win.json"), "escpos")
]

