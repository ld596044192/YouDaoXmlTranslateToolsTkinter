from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

app = QApplication([])

# create a system tray icon
tray_icon = QSystemTrayIcon()
tray_icon.setIcon(QIcon('icon.png'))
tray_icon.setToolTip('My App')
tray_icon.setContextMenu(QMenu())

# create a window
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Hello, world!'))
window.setLayout(layout)

# define a slot to show the window
def show_window(reason):
    if reason == QSystemTrayIcon.Trigger:
        QTimer.singleShot(0, window.show)

# connect the activated signal to the show_window slot
tray_icon.activated.connect(show_window)

# create a button to simulate clicking on the system tray icon
button = QPushButton('Show Window')
button.clicked.connect(lambda: tray_icon.activated.emit(QSystemTrayIcon.Trigger))

# show the system tray icon and run the event loop
tray_icon.show()
button.show()
app.exec_()
