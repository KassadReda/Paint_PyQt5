# code : https://www.learnpyqt.com/tutorials/actions-toolbars-menus
# icones https://p.yusukekamiyamane.com

import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtXml import QDomDocument
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import Qt, QSize, QIODevice, QFile, QRect, QTextStream
from PyQt5.QtGui import QIcon, QFont, QPainter
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QFontDialog, QMainWindow, \
QToolBar,QAction,QStatusBar,QGraphicsView, \
QLabel,QVBoxLayout,QDialog, QDialogButtonBox, QColorDialog, QMenu
from svgReader import SvgReader
from save_open import SaveOpen
from scene import Scene

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("CAI-P21 : Editeur graphique")
        self.srcfile = None
        self.saved = False
        self.create_scene()
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        
    def create_scene(self) :
        view=QGraphicsView()
        self.scene=Scene(self)
        view.setScene(self.scene)
        self.setCentralWidget(view)
        self.srcfile = None

    def menu_surgissant(self,event):
        contextMenu = self.menu_style
        contextMenu.exec_(self.mapToGlobal(event.pos()))
        

    def mousePressEvent(self, event):
        if event.button()==Qt.RightButton :
            self.menu_surgissant(event)
    
    def create_actions(self) :

    # Undo Redo actions
        name = "Undo"
        self.action_undo = QAction(QIcon('Icons/undoButton.png'), name, self)
        self.action_undo.setStatusTip("Undo Item")
        self.action_undo.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))
        
        
        name = "Redo"
        self.action_redo = QAction(QIcon('Icons/redoButton.png'), name, self)
        self.action_redo.setStatusTip("Redo Item")
        self.action_redo.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

    # Menu File

        name="New"
        self.action_file_new=QAction(QIcon('Icons/new.png'), name, self)
        self.action_file_new.setStatusTip("New File")
        self.action_file_new.triggered.connect(self.file_new)

        name="Open"
        self.action_file_open=QAction(QIcon('Icons/open.png'), name, self)
        self.action_file_open.setStatusTip("Open File")
        self.action_file_open.triggered.connect(self.file_open)
    
        name="Save"
        self.action_file_save=QAction(QIcon('Icons/save.png'), name, self)
        self.action_file_save.setStatusTip("Save File")
        self.action_file_save.triggered.connect(self.file_save)

        name="Save As"
        self.action_file_save_as=QAction(QIcon('Icons/save.png'), name, self)
        self.action_file_save_as.setStatusTip("Save File")
        self.action_file_save_as.triggered.connect(self.file_save_as)

        name="Exit"
        self.action_file_exit=QAction(QIcon('Icons/exit.png'), name, self)
        self.action_file_exit.setStatusTip("Exit application")
        self.action_file_exit.triggered.connect(self.file_exit)
        
    #  Menu Tool

        name="Line"
        self.action_line=QAction(QIcon('Icons/tool_line.png'), name, self)
        self.action_line.setStatusTip("Line")
        self.action_line.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Ellipse"
        self.action_ellipse=QAction(QIcon('Icons/tool_ellipse.png'), name, self)
        self.action_ellipse.setStatusTip("Ellipse")
        self.action_ellipse.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Polygon"
        self.action_polygon=QAction(QIcon('Icons/tool_polygon.png'), name, self)
        self.action_polygon.setStatusTip("Polygon")
        self.action_polygon.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))
        
        name="Rectangle"
        self.action_rectangle=QAction(QIcon('Icons/tool_rectangle.png'), name, self)
        self.action_rectangle.setStatusTip("Rectangle")
        self.action_rectangle.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name = "Texte"
        self.action_texte = QAction(QIcon('Icons/tool_text.png'), name, self)
        self.action_texte.setStatusTip("Texte")
        self.action_texte.triggered.connect(lambda status, selection = name : self.on_triggered_action(status, selection))

    # Menu Style

        name="Font"
        self.action_style_font = QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_style_font.setStatusTip("Select Font")
        self.action_style_font.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

    # Menu Style > Menu Pen

        name="Pen Color" 
        self.action_style_pen_color=QAction(QIcon('Icons/monkey_on_16x16.png'), name, self)
        self.action_style_pen_color.setStatusTip("Select Pen color")
        self.action_style_pen_color.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

    # Menu Style > Menu Pen > Line

        name="Pen Solid Line"
        self.action_style_pen_solid_line = QAction(QIcon('Icons/SolidLine.png'), name, self)
        self.action_style_pen_solid_line.setStatusTip("Select Pen Solid Line Type")
        self.action_style_pen_solid_line.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Pen Dash Line"
        self.action_style_pen_dash_line = QAction(QIcon('Icons/DashLine.png'), name, self)
        self.action_style_pen_dash_line.setStatusTip("Select Pen Dash Line Type")
        self.action_style_pen_dash_line.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Pen Dot Line"
        self.action_style_pen_dot_line = QAction(QIcon('Icons/DotLine.png'), name, self)
        self.action_style_pen_dot_line.setStatusTip("Select Pen Dot Line Type")
        self.action_style_pen_dot_line.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Pen Dash Dot Line"
        self.action_style_pen_dash_dot_line = QAction(QIcon('Icons/DashDotLine.png'), name, self)
        self.action_style_pen_dash_dot_line.setStatusTip("Select Pen dash Dot Line Type")
        self.action_style_pen_dash_dot_line.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Pen Dash Dot Dot Line"
        self.action_style_pen_dash_dot_dot_line = QAction(QIcon('Icons/DashDotDotLine.png'), name, self)
        self.action_style_pen_dash_dot_dot_line.setStatusTip("Select Pen Dash Dot Dot Line Type")
        self.action_style_pen_dash_dot_dot_line.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

    # Menu Style > Menu Pen > Width

        name  ="Pen Width 1"
        self.action_style_pen_width_1 = QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_style_pen_width_1.setStatusTip("Select Pen Width 1")
        self.action_style_pen_width_1.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name  ="Pen Width 2"
        self.action_style_pen_width_2 = QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_style_pen_width_2.setStatusTip("Select Pen Width 2")
        self.action_style_pen_width_2.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name  ="Pen Width 3"
        self.action_style_pen_width_3 = QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_style_pen_width_3.setStatusTip("Select Pen Width 3")
        self.action_style_pen_width_3.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name  ="Pen Width 4"
        self.action_style_pen_width_4 = QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_style_pen_width_4.setStatusTip("Select Pen Width 4")
        self.action_style_pen_width_4.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name  ="Pen Width 5"
        self.action_style_pen_width_5 = QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_style_pen_width_5.setStatusTip("Select Pen Width 5")
        self.action_style_pen_width_5.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

    # Menu Style > Menu Brush

        name="Brush Color" 
        self.action_style_brush_color=QAction(QIcon('Icons/monkey_on_16x16.png'), name, self)
        self.action_style_brush_color.setStatusTip("Select Brush color")
        self.action_style_brush_color.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

    # Menu Style > Menu Brush > Menu Fill

        name="Brush Fill Solid Patern"
        self.action_style_brush_solid_patern = QAction(QIcon('Icons/SolidBrushPattern.png'), name, self)
        self.action_style_brush_solid_patern.setStatusTip("Select Solid Brush Pattern")
        self.action_style_brush_solid_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 1 Patern"
        self.action_style_brush_dense1_patern = QAction(QIcon('Icons/Dense1BrushPattern.png'), name, self)
        self.action_style_brush_dense1_patern.setStatusTip("Select Dense1 Brush Pattern")
        self.action_style_brush_dense1_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 2 Patern"
        self.action_style_brush_dense2_patern = QAction(QIcon('Icons/Dense2BrushPattern.png'), name, self)
        self.action_style_brush_dense2_patern.setStatusTip("Select Dense2 Brush Pattern")
        self.action_style_brush_dense2_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 3 Patern"
        self.action_style_brush_dense3_patern = QAction(QIcon('Icons/Dense3BrushPattern.png'), name, self)
        self.action_style_brush_dense3_patern.setStatusTip("Select Dense3 Brush Pattern")
        self.action_style_brush_dense3_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 4 Patern"
        self.action_style_brush_dense4_patern = QAction(QIcon('Icons/Dense4BrushPattern.png'), name, self)
        self.action_style_brush_dense4_patern.setStatusTip("Select Dense4 Brush Pattern")
        self.action_style_brush_dense4_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 5 Patern"
        self.action_style_brush_dense5_patern = QAction(QIcon('Icons/Dense5BrushPattern.png'), name, self)
        self.action_style_brush_dense5_patern.setStatusTip("Select Dense5 Brush Pattern")
        self.action_style_brush_dense5_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 6 Patern"
        self.action_style_brush_dense6_patern = QAction(QIcon('Icons/Dense6BrushPattern.png'), name, self)
        self.action_style_brush_dense6_patern.setStatusTip("Select Dense6 Brush Pattern")
        self.action_style_brush_dense6_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Dense 7 Patern"
        self.action_style_brush_dense7_patern = QAction(QIcon('Icons/Dense7BrushPattern.png'), name, self)
        self.action_style_brush_dense7_patern.setStatusTip("Select Dense7 Brush Pattern")
        self.action_style_brush_dense7_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Horizontal Patern"
        self.action_style_brush_horizontal_patern = QAction(QIcon('Icons/HorBrushPattern.png'), name, self)
        self.action_style_brush_horizontal_patern.setStatusTip("Select Horizontal Brush Pattern")
        self.action_style_brush_horizontal_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Vertical Patern"
        self.action_style_brush_vertical_patern = QAction(QIcon('Icons/VerBrushPattern.png'), name, self)
        self.action_style_brush_vertical_patern.setStatusTip("Select Vertical Brush Pattern")
        self.action_style_brush_vertical_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Cross Patern"
        self.action_style_brush_cross_patern = QAction(QIcon('Icons/CrossBrushPattern.png'), name, self)
        self.action_style_brush_cross_patern.setStatusTip("Select Cross Brush Pattern")
        self.action_style_brush_cross_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill BDiag Patern"
        self.action_style_brush_bdiag_patern = QAction(QIcon('Icons/BDiagBrushPattern.png'), name, self)
        self.action_style_brush_bdiag_patern.setStatusTip("Select BDiag Brush Pattern")
        self.action_style_brush_bdiag_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill FDiag Patern"
        self.action_style_brush_fdiag_patern = QAction(QIcon('Icons/FDiagBrushPattern.png'), name, self)
        self.action_style_brush_fdiag_patern.setStatusTip("Select FDiag Brush Pattern")
        self.action_style_brush_fdiag_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill DiagCross Patern"
        self.action_style_brush_diag_cross_patern = QAction(QIcon('Icons/CrossDiagBrushPattern.png'), name, self)
        self.action_style_brush_diag_cross_patern.setStatusTip("Select Cross Diagonal Brush Pattern")
        self.action_style_brush_diag_cross_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Linear Gradient Patern"
        self.action_style_brush_linear_gradient_patern = QAction(QIcon('Icons/LinearGradientBrushPattern.png'), name, self)
        self.action_style_brush_linear_gradient_patern.setStatusTip("Select Linear Gradient Brush Pattern")
        self.action_style_brush_linear_gradient_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Radial Gradient Patern"
        self.action_style_brush_radial_gradient_patern = QAction(QIcon('Icons/RadialGradientBrushPattern.png'), name, self)
        self.action_style_brush_radial_gradient_patern.setStatusTip("Select Radial Gradient Brush Pattern")
        self.action_style_brush_radial_gradient_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill Conical Gradient Patern"
        self.action_style_brush_conical_gradient_patern = QAction(QIcon('Icons/ConicalGradientBrushPattern.png'), name, self)
        self.action_style_brush_conical_gradient_patern.setStatusTip("Select Conical Gradient Brush Pattern")
        self.action_style_brush_conical_gradient_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))

        name="Brush Fill No Patern"
        self.action_style_brush_no_patern = QAction(QIcon('Icons/NoBrushPattern.png'), name, self)
        self.action_style_brush_no_patern.setStatusTip("Select No Brush Pattern")
        self.action_style_brush_no_patern.triggered.connect(lambda status,selection=name : self.on_triggered_action(status,selection))


    # Menu Help
        
        name="About Us"
        self.action_about_us=QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_about_us.setStatusTip("About Us")
        self.action_about_us.triggered.connect(lambda status, selection='About US","This software is created by : \n - KASSAD Reda :  r7kassad@enib.fr  \n - MARCHESE Caroline :  c7marche@enib.fr ' :
        self.about(status,selection))

        name="About Qt"
        self.action_about_qt=QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_about_qt.setStatusTip("Pen Width")
        self.action_about_qt.triggered.connect(lambda status, selection='This application is developed with PyQt5.\nFor more information, please visit\nthe following site https://www.qt.io' :
        self.about(status,selection))

        name="About the Application"
        self.action_about_the_application=QAction(QIcon('Icons/tool_pen.png'), name, self)
        self.action_about_the_application.setStatusTip("Pen Width")
        self.action_about_the_application.triggered.connect(lambda status, selection="Version 2.3 \n For further information, please refer to the README file" :
        self.about(status,selection))

        #additionnal actions
        name = "Erase"
        self.action_erase = QtWidgets.QAction(QIcon('Icons/eraser.png'), name, self)
        self.action_erase.setStatusTip(name)
        self.action_erase.setToolTip(name)
        self.action_erase.triggered.connect(lambda status, selection=name: self.on_triggered_action(status, selection))

        name = "Move"
        self.action_move = QtWidgets.QAction(QIcon('Icons/pointer.png'), name, self)
        self.action_move.setStatusTip(name)
        self.action_move.setToolTip(name)
        self.action_move.triggered.connect(lambda status, selection=name: self.on_triggered_action(status, selection))
        

        

        
    def create_toolbars(self) :
        self.toolbar=QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(16,16))
        self.setStatusBar(QStatusBar(self))

        self.toolbar.addAction(self.action_file_new)
        self.toolbar.addAction(self.action_file_open)
        self.toolbar.addAction(self.action_file_save)
        self.toolbar.addAction(self.action_file_exit)
        self.toolbar.addAction(self.action_ellipse)
        self.toolbar.addAction(self.action_rectangle)
        self.toolbar.addAction(self.action_line)
        self.toolbar.addAction(self.action_texte)
        # adding erase and moving icons
        self.toolbar.addAction(self.action_polygon)
        self.toolbar.addAction(self.action_erase)
        self.toolbar.addAction(self.action_move)
        #Undo Redo actions
        self.toolbar.addAction(self.action_undo)
        self.toolbar.addAction(self.action_redo)



    def create_menus(self) :
        menubar=self.menuBar()
     
    # Arborescence barre de menu
        self.menu_file = menubar.addMenu("&File")
        self.menu_tools = menubar.addMenu("&Tools")
        self.menu_style = menubar.addMenu("&Style")
        self.menu_help = menubar.addMenu("&Help")
        
    #Arborescence Menu File
        self.menu_file.addAction(self.action_file_new)
        self.menu_file.addAction(self.action_file_open)
        self.menu_file.addAction(self.action_file_save)
        self.menu_file.addAction(self.action_file_save_as)
        self.menu_file.addAction(self.action_file_exit)

    #Arborescence Menu Tools
        self.menu_tools.addAction(self.action_line)
        self.menu_tools.addAction(self.action_rectangle)
        self.menu_tools.addAction(self.action_ellipse)
        self.menu_tools.addAction(self.action_polygon)
        self.menu_tools.addAction(self.action_texte)

    # Arborescence menu Style
        self.pen_style = self.menu_style.addMenu("&Pen")
        self.brush_style = self.menu_style.addMenu("&Brush")
        self.menu_style.addAction(self.action_style_font)

    # Arborescence Menu Style > Menu Pen
        self.pen_style.addAction(self.action_style_pen_color)
        self.pen_style_line = self.pen_style.addMenu("&Line")
        self.pen_style_width = self.pen_style.addMenu("&Width")

    # Arborescence Menu Style > Menu Pen > Line
        self.pen_style_line.addAction(self.action_style_pen_solid_line)
        self.pen_style_line.addAction(self.action_style_pen_dash_line)
        self.pen_style_line.addAction(self.action_style_pen_dot_line)
        self.pen_style_line.addAction(self.action_style_pen_dash_dot_line)
        self.pen_style_line.addAction(self.action_style_pen_dash_dot_dot_line)

    # Arborescence Menu Style > menu Pen > Width

        self.pen_style_width.addAction(self.action_style_pen_width_1)
        self.pen_style_width.addAction(self.action_style_pen_width_2)
        self.pen_style_width.addAction(self.action_style_pen_width_3)
        self.pen_style_width.addAction(self.action_style_pen_width_4)
        self.pen_style_width.addAction(self.action_style_pen_width_5)

    # Arborescence Menu Style > Menu Brush
        self.brush_style.addAction(self.action_style_brush_color)
        self.brush_style_fill = self.brush_style.addMenu("&Fill")

    # Arborescence Menu Style > Menu Brush > Menu Fill
        self.brush_style_fill.addAction(self.action_style_brush_solid_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense1_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense2_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense3_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense4_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense5_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense6_patern)
        self.brush_style_fill.addAction(self.action_style_brush_dense7_patern)
        self.brush_style_fill.addAction(self.action_style_brush_horizontal_patern)
        self.brush_style_fill.addAction(self.action_style_brush_vertical_patern)
        self.brush_style_fill.addAction(self.action_style_brush_cross_patern)
        self.brush_style_fill.addAction(self.action_style_brush_bdiag_patern)
        self.brush_style_fill.addAction(self.action_style_brush_fdiag_patern)
        self.brush_style_fill.addAction(self.action_style_brush_diag_cross_patern)
        self.brush_style_fill.addAction(self.action_style_brush_linear_gradient_patern)
        self.brush_style_fill.addAction(self.action_style_brush_radial_gradient_patern)
        self.brush_style_fill.addAction(self.action_style_brush_conical_gradient_patern)
        self.brush_style_fill.addAction(self.action_style_brush_no_patern)


    # Arborescence Menu Help
        self.menu_help.addAction(self.action_about_us)
        self.menu_help.addAction(self.action_about_qt)
        self.menu_help.addAction(self.action_about_the_application)

     

    def on_triggered_action(self,status,selection):
        print("status:",status,", selection:",selection)

        if (selection == "Line" or selection == "Rectangle" or selection == "Polygon" or selection == "Ellipse" or selection == "Texte" or selection == "Move" or selection == "Erase"):
            self.scene.current_tool = selection
            self.scene.setSceneChanged(True)

        elif selection=="Pen Color" :
            color=self.style_color()
            if color :
                self.scene.set_pen_color(color)
        
        elif selection == "Pen Solid Line" :
            self.scene.pen.setStyle(Qt.SolidLine)

        elif selection == "Pen Dash Line" :
            self.scene.pen.setStyle(Qt.DashLine)

        elif selection == "Pen Dot Line" :
            self.scene.pen.setStyle(Qt.DotLine)

        elif selection == "Pen Dash Dot Line" :
            self.scene.pen.setStyle(Qt.DashDotLine)

        elif selection == "Pen Dash Dot Dot Line" :
            self.scene.pen.setStyle(Qt.DashDotDotLine)
        
        elif (selection == "Pen Width 1" or selection == "Pen Width 2" or selection == "Pen Width 3" or selection == "Pen Width 4" or selection == "Pen Width 5") :
            texte,space,value = selection.rpartition(' ')
            self.scene.pen.setWidth(int(value))

        elif selection=="Brush Color" :
            color=self.style_color()
            if color :
                self.scene.set_brush_color(color)

        elif (selection.find("Brush Fill") != -1) :
            self.style_brush_fill_pattern(selection)

        elif selection == "Font" :
            font = self.style_font()
            if font :
                self.scene.set_used_font(font)

        elif selection == "Undo" :
            self.scene.undoItem()

        elif selection == "Redo" :
            self.scene.redoItem()
           

    def style_color(self):
        color=QColorDialog.getColor(Qt.yellow,self)
        if color.isValid() :
            print("color :",color)
        else :
            color=None
        return color

    def style_font(self):
        (ok, font) = QFontDialog.getFont(QFont("Helvetica [Cronyx]", 10), self)
        if ok :
            print("font :", font)
        else :
            font = None
        return font

    def about(self,status,selection):
        print(status,selection)
        dialog_screen = QDialog()
        dialog_screen.resize(400,150)
        label = QLabel(selection,dialog_screen)
        label.move(50,50)
        dialog_screen.setWindowTitle("Dialog")
        dialog_screen.setWindowModality(Qt.ApplicationModal)
        dialog_screen.exec_()

    def file_new(self):

        if self.scene.scene_changed():
            title = self.tr('New ?')
            text  = self.tr("Do you want to create a new drawing without saving the old one ?")
            msgbox = QMessageBox(QMessageBox.Question, title, text)
            msgbox.setWindowIcon(self.windowIcon())
            no_button = msgbox.addButton(self.tr('No'), QtWidgets.QMessageBox.NoRole)
            yes_button = msgbox.addButton(self.tr('Yes'), QtWidgets.QMessageBox.YesRole)
            msgbox.setDefaultButton(no_button)
            msgbox.exec()
            
            if (msgbox.clickedButton() == no_button):
                self.file_save()
                

        self.scene.clear()
        self.scene.setSceneChanged(False)
    
    

    def file_exit(self):
        print(self.scene.scene_changed(), self.saved)

        if self.saved == True or not(self.scene.scene_changed()):
            exit(0)
        elif self.saved == False  :
            if self.scene.scene_changed() : 
                title = self.tr('Quit ?')
                text  = self.tr("Do you want to quit without saving ?")
                msgbox = QtWidgets.QMessageBox(QMessageBox.Question, title, text)
                msgbox.setWindowIcon(self.windowIcon())
                no_button = msgbox.addButton(self.tr('No'), QMessageBox.NoRole)
                yes_button= msgbox.addButton(self.tr('Yes'), QMessageBox.YesRole)
                msgbox.setDefaultButton(no_button)
                msgbox.exec()

                print("fichier changé mais " ,self.saved)

                if (msgbox.clickedButton() == yes_button) or self.saved == True:
                    exit(0)
                elif (msgbox.clickedButton() == no_button) or self.saved == False:
                    self.file_save()
                    print(self.saved, "condition if no")
                    exit(0)

        else : 
            exit(0)
        
    

        
        
    
    
    def style_brush_fill_pattern(self, selection) :

        if selection == "Brush Fill Solid Patern" :
            self.scene.brush.setStyle(Qt.SolidPattern)

        elif selection == "Brush Fill Dense 1 Patern" :
            self.scene.brush.setStyle(Qt.Dense1Pattern)

        elif selection == "Brush Fill Dense 2 Patern" :
            self.scene.brush.setStyle(Qt.Dense2Pattern)

        elif selection == "Brush Fill Dense 3 Patern" :
            self.scene.brush.setStyle(Qt.Dense3Pattern)

        elif selection == "Brush Fill Dense 4 Patern" :
            self.scene.brush.setStyle(Qt.Dense4Pattern)

        elif selection == "Brush Fill Dense 5 Patern" :
            self.scene.brush.setStyle(Qt.Dense5Pattern)

        elif selection == "Brush Fill Dense 6 Patern" :
            self.scene.brush.setStyle(Qt.Dense6Pattern)

        elif selection == "Brush Fill Dense 7 Patern" :
            self.scene.brush.setStyle(Qt.Dense7Pattern)

        elif selection == "Brush Fill Horizontal Patern" :
            self.scene.brush.setStyle(Qt.HorPattern)

        elif selection == "Brush Fill Vertical Patern" :
            self.scene.brush.setStyle(Qt.VerPattern)

        elif selection == "Brush Fill Cross Patern" :
            self.scene.brush.setStyle(Qt.CrossPattern)

        elif selection == "Brush Fill BDiag Patern" :
            self.scene.brush.setStyle(Qt.BDiagPattern)

        elif selection == "Brush Fill FDiag Patern" :
            self.scene.brush.setStyle(Qt.FDiagPattern)

        elif selection == "Brush Fill DiagCross Patern" :
            self.scene.brush.setStyle(Qt.DiagCrossPattern)

        elif selection == "Brush Fill Linear Gradient Patern" :
            self.scene.brush.setStyle(Qt.LinearGradientPattern)

        elif selection == "Brush Fill Radial Gradient Patern" :
            self.scene.brush.setStyle(Qt.RadialGradientPattern)

        elif selection == "Brush Fill Conical Gradient Patern" :
            self.scene.brush.setStyle(Qt.ConicalPattern)

        else :
            self.scene.brush.setStyle(Qt.NoBrush)

    # adding the functions 

    def file_open(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd(), "JSON files (*.json);; SVG files (*.svg)")
        filename, file_extention = file
        if file_extention == "SVG files (*.svg)":
            fileopen = QFile(filename)
            if fileopen.open(QFile.ReadOnly | QFile.Text):
                self.scene.clear()
                self.scene.setSceneChanged(False)
                svgReader = SvgReader()

                for element in svgReader.getElements(fileopen):
                    self.scene.addItem(element)
                fileopen.close()
                self.srcfile = file
                
        if file_extention == "JSON files (*.json)":
            fileopen = QFile(filename)
            self.scene.clear()
            self.scene.setSceneChanged(False)
            if fileopen.open(QFile.ReadOnly | QFile.Text):
                s = SaveOpen()
                for element in s.open(fileopen):
                    self.scene.addItem(element)
                fileopen.close()
                self.srcfile = file


    def file_save(self):
        print(self.saved)
        self.saved = True
        if (self.srcfile):
            self.save(self.srcfile)
        else:
            self.file_save_as()
            
    def save(self, file):
        filename, file_extention = file
        if file_extention == "SVG files (*.svg)":
            title = self.tr('Save in this format ?')
            text  = self.tr("If you save in this format, only certain properties will be retained (such as shapes and colors, not line and fill styles)")
            msgbox = QMessageBox(QMessageBox.Question, title, text)
            msgbox.setWindowIcon(self.windowIcon())
            no_button = msgbox.addButton(self.tr('No'), QMessageBox.NoRole)
            yes_button= msgbox.addButton(self.tr('Yes'), QMessageBox.YesRole)
            msgbox.setDefaultButton(no_button)
            msgbox.exec()
            
            if (msgbox.clickedButton() == yes_button):
                self.saved = True
                filesave = QFile(filename+".svg")
                filesave.resize(0)
                if filesave.open(QIODevice.WriteOnly | QIODevice.ReadOnly):

                    generator = QtSvg.QSvgGenerator()
                    generator.setFileName(filename+".svg")
                    generator.setTitle("Simply Paint")
                    generator.setDescription("Filed created by Simply Paint.")
                    generator.setSize(QSize(self.scene.width(), self.scene.height()))
                    generator.setViewBox(QRect(0, 0, self.scene.width(), self.scene.height()))
                    
                    painter = QPainter()
                    painter.begin(generator)
                    self.scene.render(painter)
                    painter.end()
                    
                    doc = QDomDocument()
                    doc.setContent(filesave)
                    filesave.close()
                
                filesave = QFile(filename)
                fileStream = QTextStream(filesave)
                if filesave.open(QIODevice.WriteOnly):
                    SVGNode = doc.lastChild()
                    boardNode = SVGNode.lastChild()
                    groupFormNodeList = boardNode.childNodes()

                    count = groupFormNodeList.length()
                    for i in range(count):
                        groupFormNode = groupFormNodeList.item(count-i-1)
                        if not groupFormNode.hasChildNodes():
                            boardNode.removeChild(groupFormNode)
                    
                    groupFormNodeList = boardNode.childNodes()

                    doc.save(fileStream, 2)
                    filesave.close()
                    
                    self.srcfile = file
                    self.scene.setSceneChanged(False)

        if file_extention == "JSON files (*.json)":
            filesave = QFile(filename+".json")
            filesave.resize(0)
            if filesave.open(QIODevice.WriteOnly | QIODevice.ReadOnly):
                s = SaveOpen()
                s.save(filesave, self.scene.items())
                filesave.close()
                self.srcfile = file
            
    
    def file_save_as(self):
        file = QFileDialog.getSaveFileName(self, self.tr('Save File'), os.getcwd(), "JSON files (*.json);; SVG files (*.svg)")
        self.save(file)




if __name__=="__main__" :
    app=QApplication(sys.argv)
    mw=MainWindow()
    mw.show()
    print("initial item_shape : ", mw.scene.item_shape)
    app.exec_()

