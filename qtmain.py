import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QWidget

import jungsoseoul
import sh
import chungyakhome


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Oh My House')
        self.setWindowIcon(QIcon('static/web.png'))
        #self.statusBar().showMessage('Ready')

        grid = QGridLayout()
        self.setLayout(grid)
        articleList = []
        articleList += jungsoseoul.get_data()
        #articleList += sh.get_data()
        articleList += chungyakhome.get_data()

        self.drawGrid(grid, articleList)

        self.move(0, 0)
        self.resize(0, 0)
        self.show()

    def drawGrid(self, grid, articleList):
        tr_id = QLabel('#')
        tr_type = QLabel('구분')
        tr_area = QLabel('지역')
        tr_subject = QLabel('내용')
        tr_start_date = QLabel('청약시작')
        tr_end_date = QLabel('청약마감')
        tr_date = QLabel('공고일')
        grid.addWidget(tr_id, 0, 0)
        grid.addWidget(tr_type, 0, 1)
        grid.addWidget(tr_area, 0, 2)
        grid.addWidget(tr_subject, 0, 3)
        grid.addWidget(tr_start_date, 0, 4)
        grid.addWidget(tr_end_date, 0, 5)
        grid.addWidget(tr_date, 0, 6)

        #rr = sorted(articleList, key=(lambda x: x['start_date']))
        for i in range(0, len(articleList)):
            article = articleList[i]
            id = QLabel(str(i+1))
            type = QLabel(article['type'])
            area = QLabel(article['area'])
            subject = QLabel(article['link'])
            subject.setOpenExternalLinks(True)
            start_date = QLabel()
            end_date = QLabel()
            if 'start_date' in article.keys():
                start_date = QLabel(article['start_date'].isoformat())
            if 'end_date' in article.keys():
                end_date = QLabel(article['end_date'].isoformat())
            date = QLabel(article['date'].isoformat())
            grid.addWidget(id, i+1, 0)
            grid.addWidget(type, i+1, 1)
            grid.addWidget(area, i+1, 2)
            grid.addWidget(subject, i+1, 3)
            grid.addWidget(start_date, i+1, 4)
            grid.addWidget(end_date, i+1, 5)
            grid.addWidget(date, i+1, 6)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
