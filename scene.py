import sys
from PyQt5.QtCore import Qt, QSize, QPoint, QPointF
from PyQt5.QtGui import QIcon,QBrush,QPen, QFont, QTransform, QPainterPath, QPolygonF
from PyQt5.QtWidgets import QApplication, QInputDialog, QGraphicsEllipseItem, QGraphicsLineItem, QMessageBox, QGraphicsPolygonItem, QGraphicsTextItem,QMainWindow, \
QGraphicsScene, QGraphicsView,QGraphicsItem, QGraphicsRectItem

class Scene (QGraphicsScene) :
    def __init__(self,*args,**kwargs):
        super(Scene, self).__init__(*args,**kwargs)
        self.pen=QPen()
        self.pen.setWidth(2)
        self.pen.setColor(Qt.red)
        self.brush=QBrush(Qt.green)
        self.used_font = QFont()
        self.current_tool = "Rectangle"

        # is used to add different shapes to canvas, and above all keep track of them during all there creation process
        self.item_shape = None

        self.mouse_pressed = False

        #item clicked to erase it and move it
        self.item_clicked = None
        self.sceneChanged = None
        self.ctrl_key_pressed = False
        self.liste_items_select = []

        # used to undo and redo
        self.items_list = []
        self.redo_list = []

        #Polygon display managment
        self.polygon_shape_points = QPolygonF()
        self.polygon_drawing_in_process = False
        self.polygon_lines_counter = 0
        self.polygon_temporary_lines = []

        # Used to draw. 
        # If the distance between the starting point and the ending point of a figure is smaller than the margin, the figure is destroyed.
        # The figured is considered as a "missclick figure" here
        self.necessary_margin = 5


        # scene_creation
        self.create()

    def create(self) :
        text=self.addText("Hello World !") # add item in Model 
        text.setPos(0,0)
        text.setVisible(True)
        self.items_list.append(text)
        rect=QGraphicsRectItem(50,100,200,50)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setPen(self.pen)
        rect.setBrush(self.brush)
        self.addItem(rect)                # add item in Model 
        self.items_list.append(rect)
        ellipse = QGraphicsEllipseItem(100, 200, 10, 40)
        ellipse.setPen(self.pen)
        ellipse.setBrush(self.brush)
        self.addItem(ellipse) 
        self.items_list.append(ellipse)


    def scene_changed(self):
        return self.sceneChanged

    def setSceneChanged(self, sceneChanged):
        self.sceneChanged = sceneChanged
    
    def set_pen_color(self,color) :
        self.pen.setColor(color)
    
    def set_brush_color(self,color) :
        self.brush.setColor(color)

    def set_used_font(self,new_font) :
        self.used_font = new_font

    # for multiple select

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_key_pressed = True
        
        elif event.key() == Qt.Key_Escape :
            print("suppression des elements selectionnés") 
            self.clear_items_selection_liste()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_key_pressed = False

    def clear_items_selection_liste(self) :

        self.liste_items_select.clear()


    def mousePressEvent(self, event):

        if event.button()==Qt.LeftButton :
            self.begin = self.end=event.scenePos()
            self.item_clicked = self.itemAt(self.begin,QTransform())
            print("current tool : ", self.current_tool)

            if self.current_tool == "Line" :
                if not self.item_shape:
                    self.sceneChanged = True
                    self.item_shape = self.addLine(self.begin.x(), self.begin.y(),
                                                   self.end.x(), self.end.y(),
                                                   self.pen)
                    self.items_list.append(self.item_shape)

            elif self.current_tool == "Rectangle" :
                if not self.item_shape:
                    self.sceneChanged = True
                    self.item_shape = self.addRect(self.begin.x(), self.begin.y(),
                                                   0, 0, self.pen)
                    self.items_list.append(self.item_shape)

            elif self.current_tool == "Polygon" : 
                if not self.item_shape and not self.polygon_drawing_in_process and self.polygon_lines_counter == 0:
                    self.sceneChanged = True
                    self.polygon_drawing_in_process = True
                    self.polygon_lines_counter += 1
                    self.polygon_shape_points.append(QPoint(event.scenePos().x(), event.scenePos().y())) 
                    self.item_shape = self.addLine(self.begin.x(), self.begin.y(),
                                                   self.end.x(), self.end.y(),
                                                   self.pen)
                    print("polyPoints : ", self.polygon_shape_points.value)
                    self.polygon_temporary_lines.append(self.item_shape)
                    

                elif self.polygon_lines_counter != 0 and self.polygon_drawing_in_process and isinstance(self.item_shape, QGraphicsLineItem) :

                    self.polygon_lines_counter += 1
                    self.item_shape = None
                    self.polygon_shape_points.append(QPoint(event.scenePos().x(), event.scenePos().y())) 
                    self.item_shape = self.addLine(self.begin.x(), self.begin.y(),
                                                   self.end.x(), self.end.y(),
                                                   self.pen)
                    self.polygon_temporary_lines.append(self.item_shape)
                    print("polyPoints : ", self.polygon_shape_points.value)


            elif self.current_tool == "Ellipse" :
                if not self.item_shape:
                    self.sceneChanged = True
                    self.item_shape = self.addEllipse(self.begin.x(), self.begin.y(),
                                                      0, 0, self.pen)
                    self.items_list.append(self.item_shape)

            elif self.current_tool == "Texte" :
                text_input, ok = QInputDialog.getText(None, "Elément textuel", "Quel texte voulez-vous afficher ?")
                self.item_shape = QGraphicsTextItem(text_input)
                self.sceneChanged = True
                self.item_shape.setPos(event.scenePos())
                self.item_shape.setFont(self.used_font)
                self.addItem(self.item_shape)
                self.items_list.append(self.item_shape)
                self.item_shape = None

            elif self.current_tool == "Erase" and self.item_clicked : 
                title = self.tr(' Erase')
                text  = self.tr("Do you want to erase this element ?")
                msgbox = QMessageBox(QMessageBox.Question, title, text)
                no_button = msgbox.addButton(self.tr('No'), QMessageBox.NoRole)
                yes_button = msgbox.addButton(self.tr('Yes'), QMessageBox.YesRole)
                msgbox.setDefaultButton(no_button)
                msgbox.exec()
            
                if (msgbox.clickedButton() == yes_button):
                    self.sceneChanged = True
                    self.removeItem(self.item_clicked)
                    self.items_list.pop(self.items_list.index(self.item_clicked))

            elif self.current_tool == "Move" and self.item_clicked : 
                self.sceneChanged = True
                self.offset = self.begin - self.item_clicked.pos()

            elif self.current_tool == "Move" and self.liste_items_select  : 
                self.sceneChanged = True
                print(self.liste_items_select.__len__())
                for element in self.liste_items_select : 
                    self.offset = self.begin - element.scenePos()
        
            else :
                print("unknown object type")

            self.mouse_pressed = True

        # multiple_selection
        if event.button()==Qt.LeftButton and self.ctrl_key_pressed and self.item_clicked and (self.item_clicked not in self.liste_items_select)  : 
            self.liste_items_select.append(self.item_clicked)
            #print(self.liste_items.__len__())
   
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton :
            self.end=event.scenePos()
            if self.current_tool == "Line" and self.mouse_pressed and self.item_shape :   
                self.item_shape.setLine(self.begin.x(), self.begin.y(),
                                        self.end.x(), self.end.y()
                                        )

            elif (self.current_tool == "Rectangle" or self.current_tool == "Ellipse") and self.mouse_pressed and self.item_shape :
                self.item_shape.setRect(self.begin.x(), self.begin.y(),
                self.end.x()-self.begin.x(),
                self.end.y()-self.begin.y()
                )

            elif self.current_tool == "Move" and self.item_clicked : 
                self.item_clicked.setPos(event.scenePos() - self.offset)

            elif self.current_tool =="Move" and self.liste_items_select : 
                for element in self.liste_items_select : 
                    element.setPos(event.scenePos() - self.offset)

            self.update()

        elif self.current_tool == "Polygon" and self.polygon_drawing_in_process and isinstance(self.item_shape, QGraphicsLineItem) and not self.mouse_pressed :
                self.end=event.scenePos()
                self.item_shape.setLine(self.begin.x(), self.begin.y(),
                                        self.end.x(), self.end.y()
                                        )
                self.update()
    
    def mouseReleaseEvent(self, event):
        self.end=event.scenePos()
        self.mouse_pressed = False

        if self.current_tool == "Polygon" :
            return

        if self.item_shape :

            if (abs(self.end.x() - self.begin.x()) <= self.necessary_margin and abs(self.end.y() - self.begin.y()) <= self.necessary_margin) and not isinstance(self.item_shape, QGraphicsTextItem) :
                self.removeItem(self.item_shape)
                self.items_list.pop(self.items_list.index(self.item_shape))
                self.item_shape = None

                return


            if self.current_tool == "Rectangle" or self.current_tool == "Ellipse" :
                self.item_shape.setBrush(self.brush)

            self.item_shape = None

            print("Items : \n")

            for item in self.items_list :
                print("\n Item : ", item)

            self.update()

    def mouseDoubleClickEvent(self,event) :
        print("item_shape : ", self.item_shape)
        if event.buttons() & Qt.LeftButton and self.current_tool == "Polygon" and self.polygon_lines_counter != 0 and self.polygon_drawing_in_process and isinstance(self.item_shape, QGraphicsLineItem) :
            self.polygon_shape_points.append(QPoint(event.scenePos().x(), event.scenePos().y()))
            
            i = 1
            while i <= self.polygon_lines_counter :
                self.removeItem(self.polygon_temporary_lines[- i])
                i += 1

            self.item_shape = self.addPolygon(self.polygon_shape_points, self.pen, self.brush)
            self.items_list.append(self.item_shape)
            self.polygon_shape_points.clear()
            self.polygon_temporary_lines.clear()
            self.polygon_lines_counter = 0
            self.polygon_drawing_in_process = False
            self.item_shape = None

            self.items_test = self.items()
            for item in self.items_test :
                print ("\n Items on canva after operations : ", item)



    def undoItem(self) :
        if self.items_list :
            self.redo_list.append(self.items_list.pop())
            self.removeItem(self.redo_list[-1])
            self.update()

    def redoItem(self) :
        if self.redo_list :
            self.items_list.append(self.redo_list.pop())
            self.addItem(self.items_list[-1])
            self.update()
        

if __name__=="__main__" :
    app=QApplication(sys.argv)
    mw=QMainWindow()
    mw.setGeometry(400,300,300,400)
    view=QGraphicsView()   # View 
    scene=Scene(mw)        # Model (graphics item container)
    view.setScene(scene)   #  View-Model connection
    mw.setCentralWidget(view) #  Mainwindow Client Area
    mw.show()
    app.exec_()
