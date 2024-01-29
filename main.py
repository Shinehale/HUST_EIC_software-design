from src.AttendanceSystemControl import Control
from src.AttendanceSystemView import AttendanceSystemView
from src.AttendanceSystemData import Data

if __name__ == '__main__':
    app = AttendanceSystemView()
    Data.initialize()
    Control.train_images()
    app.run()
    Data.organize_csv_file()
