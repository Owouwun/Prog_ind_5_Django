#!/usr/bin/env python
import sqlite3

from django.db.models import ProtectedError
from django.shortcuts import render
import xml.etree.ElementTree as ET
from Ind5.models import Chemicals, Classes, Colors


def index(request):
    message = ""
    if request.method == "POST":
        object = request.POST.get("object")
        if object:
            if object == "color":
                Color = Colors()
                Color.Name = request.POST.get("name")
                Color.save()
            elif object == "class":
                Class = Classes()
                Class.Name = request.POST.get("name")
                Class.Organic = request.POST.get("organic")
                Class.save()
            elif object == "chemical":
                Chem = Chemicals()
                Chem.Name = request.POST.get("name")
                Chem.Class = Classes.objects.get(id=request.POST.get("class"))
                Chem.Color = Colors.objects.get(id=request.POST.get("color"))
                Chem.save()

        delete = request.POST.get("deleteChemical")
        if delete:
            try:
                Chemicals.objects.filter(id=delete).delete()
            except ProtectedError as e:
                message = str(e)
        delete = request.POST.get("deleteClass")
        if delete:
            try:
                Classes.objects.filter(id=delete).delete()
            except ProtectedError as e:
                message = str(e)
        delete = request.POST.get("deleteColor")
        if delete:
            try:
                Colors.objects.filter(id=delete).delete()
            except ProtectedError as e:
                message = str(e)

    chemicals = Chemicals.objects.all()
    classes = Classes.objects.all()
    colors = Colors.objects.all()
    return render(request, "index.html", {"chemicals": chemicals, "classes": classes, "colors": colors, "message": message})


def addChemical(request):
    classes = Classes.objects.all()
    colors = Colors.objects.all()
    return render(request, "addChemical.html", {"classes": classes, "colors": colors})


def addColor(request):
    return render(request, "addColor.html")


def addClass(request):
    return render(request, "addClass.html")


def writeXML(request):
    root = ET.Element('data')

    for Class in Classes.objects.all():
        root.append(ET.Element('class', Id=str(Class.id), Name=Class.Name, Organic=str(Class.Organic)))
    for Color in Colors.objects.all():
        root.append(ET.Element('color', Id=str(Color.id), Name=Color.Name))
    for Chem in Chemicals.objects.all():
        root.append(ET.Element('chemical', Id=str(Chem.id), Name=Chem.Name, Class=str(Chem.Class.id), Color=str(Chem.Color.id)))

    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    xml_str = str(xml_str)
    xml_str = xml_str[2:-1]
    f = open("chemistry.xml", "w")
    f.write(xml_str)
    f.close()
    return index(request)


def readXML(request):
    root = ET.parse('chemistry.xml').getroot()
    for child in root:
        if child.tag=="class":
            Class = Classes()
            Class.id = child.get("Id")
            Class.Name = child.get("Name")
            Class.Organic = child.get("Organic")
            Class.save()
        elif child.tag=="color":
            Color = Colors()
            Color.id = child.get("Id")
            Color.Name = child.get("Name")
            Color.save()
        elif child.tag=="chemical":
            Chem = Chemicals()
            Chem.id = child.get("Id")
            Chem.Name = child.get("Name")
            Chem.Class = Classes.objects.get(id=child.get("Class"))
            Chem.Color = Colors.objects.get(id=child.get("Color"))
            Chem.save()
    return index(request)
