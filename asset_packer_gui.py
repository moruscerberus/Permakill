import os
import struct
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QListWidget, QMessageBox, QLabel, QCheckBox
)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# === AES Configuration ===
KEY = b'\x9e\xfaA\xf3\xcfY\xb4\xa7\xe0\xd3t\xe3R\xc1\xe1\x87\xdc\x13\x90\xd5\x1a\xc7V\x05\x83^\xa4\xc3L\xc0\xa2K'

BLOCK_SIZE = 16

class AssetPacker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Packer (PyQt5 + Encryption)")
        self.setGeometry(100, 100, 500, 450)

        self.folders = []
        self.json_file = None
        self.encrypt = False

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Folders to Pack:"))
        layout.addWidget(self.list_widget)

        layout.addWidget(self.make_button("Add Folder", self.add_folder))
        layout.addWidget(self.make_button("Clear Folders", self.clear_folders))
        layout.addWidget(self.make_button("Select JSON File (optional)", self.select_json))

        self.encrypt_checkbox = QCheckBox("Encrypt file contents")
        self.encrypt_checkbox.stateChanged.connect(self.set_encryption)
        layout.addWidget(self.encrypt_checkbox)

        layout.addWidget(self.make_button("Pack Assets", self.pack_assets))
        self.setLayout(layout)

    def make_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        return btn

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folders.append(folder)
            self.list_widget.addItem(folder)

    def clear_folders(self):
        self.folders.clear()
        self.list_widget.clear()

    def select_json(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")
        if path:
            self.json_file = path
            QMessageBox.information(self, "JSON Selected", f"Using: {os.path.basename(path)}")

    def set_encryption(self, state):
        self.encrypt = bool(state)

    def encrypt_data(self, data):
        iv = get_random_bytes(16)
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(data, BLOCK_SIZE))
        return iv + encrypted  # IV is prepended for decryption

    def collect_files(self):
        entries = []

        if self.json_file:
            with open(self.json_file, "rb") as f:
                data = f.read()
                if self.encrypt:
                    data = self.encrypt_data(data)
                entries.append(("rewards.json", data))

        for folder in self.folders:
            for root, _, files in os.walk(folder):
                for name in files:
                    full_path = os.path.join(root, name)
                    rel_path = os.path.relpath(full_path, start=folder)
                    asset_path = os.path.join(os.path.basename(folder), rel_path).replace("\\", "/")
                    with open(full_path, "rb") as f:
                        data = f.read()
                        if self.encrypt:
                            data = self.encrypt_data(data)
                        entries.append((asset_path, data))

        return entries

    def write_assets(self, entries, output_path):
        with open(output_path, "wb") as f:
            f.write(struct.pack("<I", len(entries)))

            for path, data in entries:
                path_bytes = path.encode("utf-8")
                f.write(struct.pack("<H", len(path_bytes)))
                f.write(path_bytes)
                f.write(struct.pack("<I", len(data)))
                f.write(data)

        QMessageBox.information(self, "Success", f"Packed {len(entries)} files into:\n{output_path}")

    def pack_assets(self):
        if not self.folders:
            QMessageBox.warning(self, "Missing", "Add at least one folder.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save Asset File", "game.assets", "Asset Files (*.assets)")
        if not path:
            return

        entries = self.collect_files()
        self.write_assets(entries, path)

if __name__ == "__main__":
    app = QApplication([])
    window = AssetPacker()
    window.show()
    print("KEY length:", len(KEY))
    app.exec_()
