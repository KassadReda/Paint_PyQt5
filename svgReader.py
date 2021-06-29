from PyQt5 import QtCore, QtGui, QtWidgets, QtXml
import re

class SvgReader():

    def __findParams(self, regex, testValue):
        results = []
        matches = re.finditer(regex, testValue)
        # récupération des paramètres depuis notre regex
        for matchNum, match in enumerate(matches):
            results.append(match.group())
        return results

    def __getAttributes(self, nodeElement, attributeName, defautValue=''):
        # Trouve la valeur d'un attribut d'un element du fichier SVG.
        # Si on ne trouve pas de valeur à l'element et que celui-ci fait
        # partie d'un groupe, on recherchera l'existance de cette même
        # valeur sinon, on renvoie la valeur par défault.

        value = None
        node = nodeElement
        
        while(value == None):
            if node.hasAttribute(attributeName):
                v = node.attribute(attributeName)
                value = v if (v != 'none') else defautValue
            else:
                node = node.parentNode().toElement()
                if node.tagName() != 'g':
                    value = defautValue
        return value

    def __getTransforms(self, nodeElement):
        transforms = []
        node = nodeElement
        while(True):
            if node.hasAttribute('transform'):
                v = node.attribute('transform')
                if (v != 'none'):
                    transforms += self.__findParams(r"([a-zA-Z]+\(((\D?[0-9., ]+)+\)))", v)
                        
            node = node.parentNode().toElement()
            if node.tagName() != 'g':
                return transforms

    def __applyMatrixTransforms(self, elementItem, transform):
        t_matrix = transform
        t_params = []
        q_transform = QtGui.QTransform()
        if t_matrix.startswith("matrix"):
            t_params = self.__findParams(r"([-?+?0-9.]+)", transform)
            
            m11 = q_transform.m11()
            m12 = q_transform.m12()
            m13 = q_transform.m13()
            m21 = q_transform.m21()
            m22 = q_transform.m22()
            m23 = q_transform.m23()
            m31 = q_transform.m31()
            m32 = q_transform.m32()
            m33 = q_transform.m33()

            m11 = float(t_params[0])
            m12 = float(t_params[1])
            m21 = float(t_params[2])
            m22 = float(t_params[3])
            m31 = float(t_params[4])
            m32 = float(t_params[5])
            q_transform.setMatrix(m11,m12,m13,m21,m22,m23,m31,m32,m33)
            elementItem.setTransform(q_transform)
        return elementItem

    def __applyRotationTransforms(self, elementItem, transform):
        t_rotate = transform
        t_params = []
        if t_rotate.startswith("rotate"):
            t_params = self.__findParams(r"([-?+?0-9.]+)", transform)
            if len(t_params):
                a = float(t_params[0])
                if len(t_params)>1:
                    x = float(t_params[1])
                    y = float(t_params[2])
                    elementItem.setTransformOriginPoint(x,y)
                elementItem.setRotation(a)
                elementItem.setTransformOriginPoint(elementItem.x(),elementItem.y())
        return elementItem

    def __applyScaleTransforms(self, elementItem, transform):
        t_scale = transform
        t_params = []
        q_transform = QtGui.QTransform()
        if t_scale.startswith("scale"):
            t_params = self.__findParams(r"([-?+?0-9.]+)", transform)
            if len(t_params):
                x = float(t_params[0])
                y = float(t_params[1] if (len(t_params)>1) else x)
                q_transform.scale(x,y)
                elementItem.setTransform(q_transform)
        return elementItem
    
    def __applyTranslateTransform(self, elementItem, transform):
        t_translate = transform
        t_params = []
        q_transform = QtGui.QTransform()
        if t_translate.startswith("translate"):
            t_params = self.__findParams(r"([-?+?0-9.]+)", transform)
            if len(t_params):
                x = float(t_params[0])
                y = float(t_params[1] if (len(t_params)>1) else 0)
                q_transform.translate(x,y)
                elementItem.setTransform(q_transform)
        return elementItem  

    def __applyAllTransforms(self, elementItem, transforms):
        eItem = elementItem
        for transform in transforms:
            if transform.startswith('matrix'):
                eItem = self.__applyMatrixTransforms(eItem, transform)
            elif transform.startswith('rotate'):
                eItem = self.__applyRotationTransforms(eItem, transform)
            elif transform.startswith('scale'):
                eItem = self.__applyScaleTransforms(eItem, transform)
            elif transform.startswith('translate'):
                eItem = self.__applyTranslateTransform(eItem, transform)
        return eItem

    def __getRectangles(self, docDOM):
        rectGraphicsList = []
        
        SVGNode = docDOM.elementsByTagName('svg')
        if len(SVGNode):
            SVGNodeElement = SVGNode.at(0).toElement()
            rectNodeList = SVGNodeElement.elementsByTagName('rect')

            graphicsRectItem = QtWidgets.QGraphicsRectItem()
            for i in range(rectNodeList.size()):
                rectElementItem = rectNodeList.item(i).toElement()
                graphicsRectItem = QtWidgets.QGraphicsRectItem(
                    int(rectElementItem.attribute("x")),
                    int(rectElementItem.attribute("y")),
                    int(rectElementItem.attribute("width")),
                    int(rectElementItem.attribute("height"))
                )
                fillColor = QtGui.QColor(self.__getAttributes(rectElementItem, 'fill', '#ffffff'))
                fillColor.setAlphaF(float(self.__getAttributes(rectElementItem, 'fill-opacity', '0')))
                brush   = QtGui.QBrush(fillColor)

                strokeColor = QtGui.QColor(self.__getAttributes(rectElementItem, 'stroke', '#000000'))
                strokeColor.setAlphaF(float(self.__getAttributes(rectElementItem, 'stroke-opacity', '1')))
                pen     = QtGui.QPen(strokeColor)
                pen.setWidth(int(self.__getAttributes(rectElementItem, 'stroke-width', '1')))

                self.__applyAllTransforms(graphicsRectItem, self.__getTransforms(rectElementItem))

                graphicsRectItem.setPen(pen)
                graphicsRectItem.setBrush(brush)
                rectGraphicsList.append(graphicsRectItem)
        return rectGraphicsList

    def __getEllipses(self, docDOM):
        ellipseGraphicsList = []

        SVGNode = docDOM.elementsByTagName('svg')
        if len(SVGNode)>0:
            SVGNodeElement = SVGNode.at(0).toElement()
            ellipseNodeList = SVGNodeElement.elementsByTagName('ellipse')

            for i in range(ellipseNodeList.size()):
                ellipseElementItem = ellipseNodeList.item(i).toElement()
                cx = float(ellipseElementItem.attribute("cx"))
                cy = float(ellipseElementItem.attribute("cy"))
                rx = float(ellipseElementItem.attribute("rx"))
                ry = float(ellipseElementItem.attribute("ry"))
                graphicsEllipseItem = QtWidgets.QGraphicsEllipseItem(cx-rx, cy-ry, rx*2.0, ry*2.0)


                fillColor = QtGui.QColor(self.__getAttributes(ellipseElementItem, 'fill', '#ffffff'))
                fillColor.setAlphaF(float(self.__getAttributes(ellipseElementItem, 'fill-opacity', '0')))
                brush   = QtGui.QBrush(fillColor)

                strokeColor = QtGui.QColor(self.__getAttributes(ellipseElementItem, 'stroke', '#000000'))
                strokeColor.setAlphaF(float(self.__getAttributes(ellipseElementItem, 'stroke-opacity', '1')))
                pen     = QtGui.QPen(strokeColor)
                pen.setWidth(int(self.__getAttributes(ellipseElementItem, 'stroke-width', '1')))

                self.__applyAllTransforms(graphicsEllipseItem, self.__getTransforms(ellipseElementItem))

                graphicsEllipseItem.setPen(pen)
                graphicsEllipseItem.setBrush(brush)
                ellipseGraphicsList.append(graphicsEllipseItem)
        return ellipseGraphicsList

    def __getCircles(self, docDOM):
        circleGraphicsList = []

        SVGNode = docDOM.elementsByTagName('svg')
        if len(SVGNode)>0:
            SVGNodeElement = SVGNode.at(0).toElement()
            circleNodeList = SVGNodeElement.elementsByTagName('circle')

            for i in range(circleNodeList.size()):
                circleElementItem = circleNodeList.item(i).toElement()
                cx = float(circleElementItem.attribute("cx"))
                cy = float(circleElementItem.attribute("cy"))
                r  = float(circleElementItem.attribute("r"))
                graphicsCircleItem = QtWidgets.QGraphicsEllipseItem(cx-r, cy-r, r*2.0, r*2.0)

                fillColor = QtGui.QColor(self.__getAttributes(circleElementItem, 'fill', '#ffffff'))
                fillColor.setAlphaF(float(self.__getAttributes(circleElementItem, 'fill-opacity', '0')))
                brush   = QtGui.QBrush(fillColor)

                strokeColor = QtGui.QColor(self.__getAttributes(circleElementItem, 'stroke', '#000000'))
                strokeColor.setAlphaF(float(self.__getAttributes(circleElementItem, 'stroke-opacity', '1')))
                pen     = QtGui.QPen(strokeColor)
                pen.setWidth(int(self.__getAttributes(circleElementItem, 'stroke-width', '1')))

                self.__applyAllTransforms(graphicsCircleItem, self.__getTransforms(circleElementItem))


                graphicsCircleItem.setPen(pen)
                graphicsCircleItem.setBrush(brush)
                circleGraphicsList.append(graphicsCircleItem)
        return circleGraphicsList


    def __getLines(self, docDOM):
        lineGraphicsList = []

        SVGNode = docDOM.elementsByTagName('svg')
        if len(SVGNode)>0:
            SVGNodeElement = SVGNode.at(0).toElement()
            lineNodeList = SVGNodeElement.elementsByTagName('polyline')

            for i in range(lineNodeList.size()):
                lineElementItem = lineNodeList.item(i).toElement()
                points = self.__findParams(r"([-?+?0-9.,]+)", lineElementItem.attribute('points'))
                graphicsPoints = []
                if len(points) == 2:
                    for point in points:
                        p = point.split(',')
                        graphicsPoints.append(QtCore.QPoint(float(p[0]), float(p[1])))

                    line = QtCore.QLineF(graphicsPoints[0], graphicsPoints[1])
                    graphicsLineItem = QtWidgets.QGraphicsLineItem(line)
                    
                    strokeColor = QtGui.QColor(self.__getAttributes(lineElementItem, 'stroke', '#000000'))
                    strokeColor.setAlphaF(float(self.__getAttributes(lineElementItem, 'stroke-opacity', '1')))
                    pen     = QtGui.QPen(strokeColor)
                    pen.setWidth(int(self.__getAttributes(lineElementItem, 'stroke-width', '1')))

                    self.__applyAllTransforms(graphicsLineItem, self.__getTransforms(lineElementItem))
                    
                    graphicsLineItem.setPen(pen)
                    lineGraphicsList.append(graphicsLineItem)
        return lineGraphicsList

    def __getPolygons(self, docDOM):
        polygonGraphicsList = []

        polygonGraphicsList += self.__getPolygonsByTag(docDOM, 'polygon', 'points')
        # support pour la balise path
        polygonGraphicsList += self.__getPolygonsByTag(docDOM, 'path', 'd')

        return polygonGraphicsList


    def __getPolygonsByTag(self, docDOM, tag, tagAttribute):
        polygonGraphicsList = []

        SVGNode = docDOM.elementsByTagName('svg')
        if len(SVGNode)>0:
            SVGNodeElement = SVGNode.at(0).toElement()
            polyNodeList = SVGNodeElement.elementsByTagName(tag)

            for i in range(polyNodeList.size()):
                polyElementItem = polyNodeList.item(i).toElement()
                points = self.__findParams(r"([-?+?0-9.,]+)", polyElementItem.attribute(tagAttribute))
                graphicsPoints = []
                if len(points) > 2 and points[0] == points[len(points)-1]:
                    for point in points:
                        p = point.split(',')
                        graphicsPoints.append(QtCore.QPoint(float(p[0]), float(p[1])))
                    polygon = QtGui.QPolygonF(graphicsPoints)
                    graphicsPolyItem = QtWidgets.QGraphicsPolygonItem(polygon)

                    fillColor = QtGui.QColor(self.__getAttributes(polyElementItem, 'fill', '#ffffff'))
                    fillColor.setAlphaF(float(self.__getAttributes(polyElementItem, 'fill-opacity', '0')))
                    brush   = QtGui.QBrush(fillColor)

                    strokeColor = QtGui.QColor(self.__getAttributes(polyElementItem, 'stroke', '#000000'))
                    strokeColor.setAlphaF(float(self.__getAttributes(polyElementItem, 'stroke-opacity', '1')))
                    pen     = QtGui.QPen(strokeColor)
                    pen.setWidth(int(self.__getAttributes(polyElementItem, 'stroke-width', '1')))

                    self.__applyAllTransforms(graphicsPolyItem, self.__getTransforms(polyElementItem))
                    
                    graphicsPolyItem.setPen(pen)
                    graphicsPolyItem.setBrush(brush)
                    polygonGraphicsList.append(graphicsPolyItem)
        return polygonGraphicsList
        
    def __getTexts(self, docDOM):
        textGraphicsList = []

        SVGNode = docDOM.elementsByTagName('svg')
        if len(SVGNode)>0:
            SVGNodeElement = SVGNode.at(0).toElement()
            textNodeList = SVGNodeElement.elementsByTagName('text')

            for i in range(textNodeList.size()):
                textElementItem = textNodeList.item(i).toElement()
                x = float(textElementItem.attribute("x"))
                y = float(textElementItem.attribute("y"))
                text = textElementItem.text()
                graphicsTextItem = QtWidgets.QGraphicsTextItem(text)
                graphicsTextItem.setX(x)
                graphicsTextItem.setY(y)
                font = QtGui.QFont()
                font.setFamily(self.__getAttributes(textElementItem, 'font-family'))
                font.setWeight(int(self.__getAttributes(textElementItem, 'font-weight')))
                font.setPointSize(float(self.__getAttributes(textElementItem, 'font-size')))
                style = self.__getAttributes(textElementItem, 'font-style')
                if style == 'normal':
                    style = QtGui.QFont.StyleNormal
                elif style == 'italic':
                    style = QtGui.QFont.StyleItalic
                elif style == 'oblique':
                    style = QtGui.QFont.StyleOblique
                font.setStyle(style)
                graphicsTextItem.setFont(font)

                self.__applyAllTransforms(graphicsTextItem, self.__getTransforms(textElementItem))
                textGraphicsList.append(graphicsTextItem)
        return textGraphicsList


    def getElements(self, fileopen):        
        doc = QtXml.QDomDocument()
        if not doc.setContent(fileopen):
            return []
        
        rectangles = self.__getRectangles(doc)
        ellipses = self.__getEllipses(doc)
        circles = self.__getCircles(doc)
        lines = self.__getLines(doc)
        polygons = self.__getPolygons(doc)
        texts = self.__getTexts(doc)

        return rectangles + ellipses + circles + lines + polygons + texts
        
    def getSize(self, fileopen):
        doc = QtXml.QDomDocument()
        if not doc.setContent(fileopen):
            return QtCore.QRectF(0, 0, 200, 200)

        SVGNode = doc.elementsByTagName('svg')
        if len(SVGNode)>0:
            SVGNodeElement = SVGNode.at(0).toElement()
            viewBoxParams = self.__findParams(r"([-?+?0-9.,]+)", SVGNodeElement.attribute('viewBox'))
            return QtCore.QRectF(
                int(viewBoxParams[0]),
                int(viewBoxParams[1]),
                int(viewBoxParams[2]),
                int(viewBoxParams[3])
            )
        else:
            return QtCore.QRectF(0, 0, 200, 200)
                


if __name__ == "__main__":

    params_list = []
    # r"(([\"][\w ]+[\"])|([\w\/]+))"
    matches = re.finditer(r"([a-zA-Z]+\(((\D?[0-9. ]+)+\)))", "matrix(0.999302,0,0,0.999302,310.283,336.765)")

    # récupération des paramètres depuis notre regex
    for matchNum, match in enumerate(matches):
        params_list.append(match.group())

    print(params_list)
    print(params_list[1].startswith("rotate"))