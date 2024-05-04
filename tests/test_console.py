#!/usr/bin/python3
"""
Unittest for console

This module contains the required tests for the specified file
"""
import unittest
import os
from io import StringIO
from models.engine.file_storage import FileStorage
from models import storage
from unittest.mock import patch
from console import HBNBCommand


def setUpModule():
    FileStorage._FileStorage__objects = {}
    if os.path.exists("file.json"):
        os.remove("file.json")


def tearDownModule():
    if os.path.exists("file.json"):
        os.remove("file.json")


class TestBasicFunctionality(unittest.TestCase):
    def testQuit(self):
        cmd = 'quit'
        output = ""
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            self.assertEqual(mck.getvalue(), output)

    def testEOF(self):
        cmd = 'EOF'
        output = "\n"
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            self.assertEqual(mck.getvalue(), output)

    def testHelp(self):
        cmd = 'help'
        output = ("\nDocumented commands (type help <topic>):\n"
                  "========================================\n"
                  "EOF  all  count  create  destroy  help  quit  show  "
                  "update\n\n")
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            self.assertEqual(mck.getvalue(), output)

    def testEmptyLine(self):
        cmd = '\n'
        output = ""
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            self.assertEqual(mck.getvalue(), output)


class TestLineLikeCommands(unittest.TestCase):
    def testCreate(self):
        FileStorage._FileStorage__objects = {}
        cmd = 'create BaseModel'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[-1]
            output = "{}\n".format(obj.id)
            self.assertEqual(mck.getvalue(), output)

    def testShow(self):
        FileStorage._FileStorage__objects = {}
        cmd1 = 'create BaseModel'
        HBNBCommand().onecmd(cmd1)
        with patch('sys.stdout', new=StringIO()) as mck:
            obj = list(storage.all().values())[-1]
            cmd2 = f'show BaseModel {obj.id}'
            HBNBCommand().onecmd(cmd2)
            output = "{}\n".format(str(obj))
            self.assertEqual(mck.getvalue(), output)

    def testDestroy(self):
        FileStorage._FileStorage__objects = {}
        cmd = 'destroy BaseModel 1223'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            output = "** no instance found **\n"
            self.assertEqual(mck.getvalue(), output)

    def testAll(self):
        FileStorage._FileStorage__objects = {}
        cmd1 = 'create BaseModel'
        HBNBCommand().onecmd(cmd1)
        with patch('sys.stdout', new=StringIO()) as mck:
            obj = list(storage.all().values())[-1]
            cmd2 = f'all BaseModel'
            HBNBCommand().onecmd(cmd2)
            output = "{}\n".format([str(obj)])
            self.assertEqual(mck.getvalue(), output)

    def testUpdate(self):
        FileStorage._FileStorage__objects = {}
        cmd = 'update BaseModel 123-4'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            output = "** no instance found **\n"
            self.assertEqual(mck.getvalue(), output)
