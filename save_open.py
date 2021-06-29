import re

from PyQt5 import QtCore, QtGui, QtWidgets

class SaveOpen():

    def __findParams(self, regex, testValue):
        results = []
        matches = re.finditer(regex, testValue)
        # récupération des paramètres depuis notre regex
        for matchNum, match in enumerate(matches):
            results.append(match.group())
        return results

    def save(self, filesave, data):
        xmlWriter = QtCore.QXmlStreamWriter(filesave)
        xmlWriter.setAutoFormatting(True)

        xmlWriter.writeStartDocument()
        xmlWriter.writeStartElement("Scene")                # Start Scene Root Element
        xmlWriter.writeAttribute("version", "v1.0")
        xmlWriter.writeStartElement("GraphicsItemList")
        items = data

        for i  in range(len(items)) :
            xmlWriter.writeStartElement("GraphicsItem")
            item = items[i]
            if item.type() == 3: # rect
                xmlWriter.writeAttribute("type", "rect")
                xmlWriter.writeStartElement("shape")
                xmlWriter.writeAttribute("x", str(item.rect().x()))
                xmlWriter.writeAttribute("y", str(item.rect().y()))
                xmlWriter.writeAttribute("width", str(item.rect().width()))
                xmlWriter.writeAttribute("height", str(item.rect().height()))
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("style")
                xmlWriter.writeAttribute("pen-color", str(item.pen().color().name()))
                xmlWriter.writeAttribute("pen-line", str(item.pen().style()))
                xmlWriter.writeAttribute("pen-width", str(item.pen().width()))
                xmlWriter.writeAttribute("brush-color", str(item.brush().color().name()))
                xmlWriter.writeAttribute("brush-fill", str(item.brush().style()))
                xmlWriter.writeEndElement()
            elif item.type() == 6: # line
                xmlWriter.writeAttribute("type", "line")
                xmlWriter.writeStartElement("shape")
                xmlWriter.writeAttribute("x1", str(item.line().x1()))
                xmlWriter.writeAttribute("y1", str(item.line().y1()))
                xmlWriter.writeAttribute("x2", str(item.line().x2()))
                xmlWriter.writeAttribute("y2", str(item.line().y2()))
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("style")
                xmlWriter.writeAttribute("pen-color", str(item.pen().color().name()))
                xmlWriter.writeAttribute("pen-line", str(item.pen().style()))
                xmlWriter.writeAttribute("pen-width", str(item.pen().width()))
                xmlWriter.writeEndElement()
            elif item.type() == 4: # ellipse
                xmlWriter.writeAttribute("type", "ellipse")
                xmlWriter.writeStartElement("shape")
                xmlWriter.writeAttribute("x", str(item.rect().x()))
                xmlWriter.writeAttribute("y", str(item.rect().y()))
                xmlWriter.writeAttribute("width", str(item.rect().width()))
                xmlWriter.writeAttribute("height", str(item.rect().height()))
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("style")
                xmlWriter.writeAttribute("pen-color", str(item.pen().color().name()))
                xmlWriter.writeAttribute("pen-line", str(item.pen().style()))
                xmlWriter.writeAttribute("pen-width", str(item.pen().width()))
                xmlWriter.writeAttribute("brush-color", str(item.brush().color().name()))
                xmlWriter.writeAttribute("brush-fill", str(item.brush().style()))
                xmlWriter.writeEndElement()
            elif item.type() == 5: # polygon
                xmlWriter.writeAttribute("type", "polygon")
                shape_path = item.shape()
                shape_path = shape_path.simplified()
                points = []
                for i in range(shape_path.elementCount()):
                    p = "({},{})".format(float(shape_path.elementAt(i).x), float(shape_path.elementAt(i).y))
                    points.append(p)
                xmlWriter.writeStartElement("shape")
                xmlWriter.writeAttribute("points", ' '.join(points))
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("style")
                xmlWriter.writeAttribute("pen-color", str(item.pen().color().name()))
                xmlWriter.writeAttribute("pen-line", str(item.pen().style()))
                xmlWriter.writeAttribute("pen-width", str(item.pen().width()))
                xmlWriter.writeAttribute("brush-color", str(item.brush().color().name()))
                xmlWriter.writeAttribute("brush-fill", str(item.brush().style()))
                xmlWriter.writeEndElement()
            elif item.type() == 8: # text
                xmlWriter.writeAttribute("type", "text")
                xmlWriter.writeStartElement("shape")
                xmlWriter.writeAttribute("x", str(item.pos().x()))
                xmlWriter.writeAttribute("y", str(item.pos().y()))
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("text-data")
                xmlWriter.writeAttribute("text", str(item.toPlainText()))
                xmlWriter.writeAttribute("font-family", str(item.font().family()))
                xmlWriter.writeAttribute("font-size", str(item.font().pointSize()))
                xmlWriter.writeAttribute("font-style", str(item.font().style()))
                xmlWriter.writeAttribute("font-weight", str(item.font().weight()))
                xmlWriter.writeEndElement()
            xmlWriter.writeEndElement()
        xmlWriter.writeEndElement()
        xmlWriter.writeEndElement()

    def open(self, fileopen):
        data = []

        xmlReader=QtCore.QXmlStreamReader(fileopen)
        xmlReader.setDevice(fileopen)
        while not xmlReader.atEnd() :
            if xmlReader.name() != "" :
                print("name",xmlReader.name() )
                if xmlReader.isStartElement() :
                    if xmlReader.name()== "GraphicsItem" :
                        print("GraphicsItem start")
                        if xmlReader.attributes().value("type") == "rect" :
                            rect = QtWidgets.QGraphicsRectItem()
                            while  xmlReader.readNextStartElement() :
                                if xmlReader.name()== "shape" :
                                    x=float(xmlReader.attributes().value("x"))
                                    y=float(xmlReader.attributes().value("y"))
                                    w=float(xmlReader.attributes().value("width"))
                                    h=float(xmlReader.attributes().value("height"))
                                    rect.setRect(x,y,w,h)
                                if xmlReader.name()== "style" :
                                    p_color = xmlReader.attributes().value("pen-color")
                                    line    = float(xmlReader.attributes().value("pen-line"))
                                    width   = float(xmlReader.attributes().value("pen-width"))
                                    b_color = xmlReader.attributes().value("brush-color")
                                    fill    = float(xmlReader.attributes().value("brush-fill"))

                                    pen = QtGui.QPen(QtGui.QColor(p_color))
                                    pen.setWidth(int(width))
                                    pen.setStyle(int(line))
                                    brush = QtGui.QBrush(QtGui.QColor(b_color))
                                    brush.setStyle(int(fill))
                                    rect.setPen(pen)
                                    rect.setBrush(brush)
                                xmlReader.readNext()
                            data.append(rect)
                            print("RECT ADDED")
                        elif xmlReader.attributes().value("type") == "ellipse":
                            ellipse = QtWidgets.QGraphicsEllipseItem()
                            while  xmlReader.readNextStartElement() :
                                if xmlReader.name()== "shape" :
                                    x=float(xmlReader.attributes().value("x"))
                                    y=float(xmlReader.attributes().value("y"))
                                    w=float(xmlReader.attributes().value("width"))
                                    h=float(xmlReader.attributes().value("height"))
                                    ellipse.setRect(x,y,w,h)
                                if xmlReader.name()== "style" :
                                    p_color = xmlReader.attributes().value("pen-color")
                                    line    = float(xmlReader.attributes().value("pen-line"))
                                    width   = float(xmlReader.attributes().value("pen-width"))
                                    b_color = xmlReader.attributes().value("brush-color")
                                    fill    = float(xmlReader.attributes().value("brush-fill"))

                                    pen = QtGui.QPen(QtGui.QColor(p_color))
                                    pen.setWidth(int(width))
                                    pen.setStyle(int(line))
                                    brush = QtGui.QBrush(QtGui.QColor(b_color))
                                    brush.setStyle(int(fill))
                                    ellipse.setPen(pen)
                                    ellipse.setBrush(brush)
                                xmlReader.readNext()
                            data.append(ellipse)
                            print("ELLIPSE ADDED")
                        elif xmlReader.attributes().value("type") == "line":
                            line = QtWidgets.QGraphicsLineItem()
                            while  xmlReader.readNextStartElement() :
                                if xmlReader.name()== "shape" :
                                    x1=float(xmlReader.attributes().value("x1"))
                                    y1=float(xmlReader.attributes().value("y1"))
                                    x2=float(xmlReader.attributes().value("x2"))
                                    y2=float(xmlReader.attributes().value("y2"))
                                    line.setLine(x1,y1,x2,y2)
                                if xmlReader.name()== "style" :
                                    p_color = xmlReader.attributes().value("pen-color")
                                    l       = float(xmlReader.attributes().value("pen-line"))
                                    width   = float(xmlReader.attributes().value("pen-width"))
                                    
                                    pen = QtGui.QPen(QtGui.QColor(p_color))
                                    pen.setWidth(int(width))
                                    pen.setStyle(int(l))
                                    line.setPen(pen)
                                xmlReader.readNext()
                            data.append(line)
                            print("LINE ADDED")
                        elif xmlReader.attributes().value("type") == "polygon":
                            polygon = QtWidgets.QGraphicsPolygonItem()
                            while  xmlReader.readNextStartElement() :
                                if xmlReader.name()== "shape" :                   
                                    points = self.__findParams(r"([-?+?0-9.,]+)", xmlReader.attributes().value("points"))
                                    graphPoints = []
                                    for point in points:
                                        p = point.split(',')
                                        graphPoints.append(QtCore.QPointF(float(p[0]), float(p[1])))
                                    poly = QtGui.QPolygonF(graphPoints)
                                    polygon.setPolygon(poly)
                                if xmlReader.name()== "style" :
                                    p_color = xmlReader.attributes().value("pen-color")
                                    l       = float(xmlReader.attributes().value("pen-line"))
                                    width   = float(xmlReader.attributes().value("pen-width"))
                                    
                                    b_color = xmlReader.attributes().value("brush-color")
                                    fill    = float(xmlReader.attributes().value("brush-fill"))

                                    pen = QtGui.QPen(QtGui.QColor(p_color))
                                    pen.setWidth(int(width))
                                    pen.setStyle(int(l))
                                    brush = QtGui.QBrush(QtGui.QColor(b_color))
                                    brush.setStyle(int(fill))
                                    polygon.setPen(pen)
                                    polygon.setBrush(brush)
                                xmlReader.readNext()
                            data.append(polygon)
                            print("polygon ADDED")
                        elif xmlReader.attributes().value("type") == "text":
                            text = QtWidgets.QGraphicsTextItem()
                            while  xmlReader.readNextStartElement() :
                                if xmlReader.name()== "shape" :
                                    x=float(xmlReader.attributes().value("x"))
                                    y=float(xmlReader.attributes().value("y"))
                                    text.setPos(x,y)
                                if xmlReader.name()== "text-data" :
                                    t = xmlReader.attributes().value("text")
                                    font_family = xmlReader.attributes().value("font-family")
                                    font_size   = int(xmlReader.attributes().value("font-size"))
                                    font_weight = int(xmlReader.attributes().value("font-weight"))
                                    font_style  = int(xmlReader.attributes().value("font-style"))

                                    font = QtGui.QFont()
                                    font.setFamily(font_family)
                                    font.setPointSize(font_size)
                                    font.setWeight(font_weight)
                                    font.setStyle(font_style)

                                    text.setPlainText(t)
                                    text.setFont(font)
                                xmlReader.readNext()
                            data.append(text)
                            print("TEXT ADDED")
            xmlReader.readNext() 
        return data