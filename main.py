from ui import *



if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)

    app.setApplicationName("Simple Pic Tool")
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
