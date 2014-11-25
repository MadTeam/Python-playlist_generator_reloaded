#!/usr/bin/python3
# -*- coding: utf-8 -*-

def argparse():
	import argparse

	parser = argparse.ArgumentParser(prog="Personal playlist generator", add_help=False, description="Permet de généner une playlist au format désiré avec différentes options", epilog="note : le générateur accepte les expressions régulieres dans les arguments optionnels", prefix_chars='-')
	obli = parser.add_argument_group("Arguments obligatoires ", "Obligatoires pour générer la playlist")
	opt = parser.add_argument_group("Arguments optionnels ", "Ils permettent d'obtenir un pourcentage sur un critère spécifique (ex: --genre rock 70 => 70% de la playlist sera composée de rock)")

	#arguments positionnels
	obli.add_argument("nom", help="nom du fichier de sortie")
	obli.add_argument("format", help="format du fichier (xspf, m3u ou pls)", choices=["xspf", "m3u", "pls"])
	obli.add_argument("temps", help="durée totale de la playlist en minute")

	#arguments optionnels
	opt.add_argument("-h", "--help", "--aide", help="affiche l'aide", action="help")
	opt.add_argument("-v", "--verbeux", help="affiche l'ensemble des informations", action="store_true")
	opt.add_argument("-i", "--intersection", "--and", help="permet d'obtenir l'intersection des demandes de la playlist", action="store_true")
	opt.add_argument("-G", "--genre", nargs=2, action="append", help="nom et pourcentage du genre")
	opt.add_argument("-g", "--sousgenre", nargs=2, action="append", help="nom et pourcentage du sous-genre")
	opt.add_argument("-a", "--artiste", nargs=2, action="append", help="nom et pourcentage de l'artiste")
	opt.add_argument("-A", "--album", nargs=2, action="append", help="nom et pourcentage de l'album")
	opt.add_argument("-t", "--titre", nargs=2, action="append", help="nom et pourcentage du titre")

	return parser

def logging(pathFile, stdOut=False, fmt=None, datefmt=None):
	import logging

	#logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	#formatter
	formatter = logging.Formatter(fmt, datefmt)

	#handler
	if stdOut:
		handlerStdout = logging.StreamHandler()
		handlerStdout.setFormatter(formatter)
		logger.addHandler(handlerStdout)

	handlerFile = logging.FileHandler(pathFile)
	handlerFile.setFormatter(formatter)
	logger.addHandler(handlerFile)

	return logger

class functions:
	def init(self, logger):
		self._log = logger

	def diffType(value, typeOfValue): #compare le type d'une variable avec une autre
		if type(value) is type(typeOfValue):
			return True
		else:
			return False

	def convert(self, variable, typeOfVariable): #convertit une variable a un type choisi (returne une exception si la conversion echoue)
		try:
			if type(typeOfVariable) is type(666):
				variable = int(variable)
				return variable
		except ValueError:
			self._log.error("converting of "+str(variable)+" to integer failed")
			return False

	def chkValue(self, variable, minValue, maxValue): #verifie si la valeur absolue d'une variable est comprise strictement entre deux valeur
		try:
			variable = abs(variable)
			if minValue < variable < maxValue:
				self._log.info("the argument value of "+str(variable)+" is accepted")
				return True
			else:
				variable = None
				self._log.warning("the argument value of "+str(variable)+" is invalid")
				return False
		except ValueError:
			self._log.error("converting of "+str(variable)+" to absolute integer failed")
			return False

	def getSqlBdd(self, user, addr, bdd, where=None):
		import sqlalchemy as sql
	
		try:
			engine = sql.create_engine('postgresql://'+user+'@'+addr+'/'+bdd)
			bdd = engine.connect()
			metadata = sql.MetaData()
			morceaux = sql.Table('morceaux', metadata,
				sql.Column('chemin', sql.String, primary_key=True),
				sql.Column('titre', sql.String),
				sql.Column('artiste', sql.String),
				sql.Column('album', sql.String),
				sql.Column('genre', sql.String),
				sql.Column('sousgenre', sql.String),
				sql.Column('duree', sql.String),
			)
			
			if where != None:
				query = sql.select([morceaux]).where(where)
			else:
				query = sql.select([morceaux])

			result = bdd.execute(query)
			return result
		except:
			self._log.error("connection to "+addr+'/'+bdd+' with '+user+' failed')
			quit()

	def toXML(self, music_list, filename):
		import getpass
		from lxml import etree

		root = etree.Element('playlist', version='1', xmlns='http://xspf.org/ns/0/')
		doc = etree.ElementTree(root)

		title = etree.SubElement(root, 'title')
		title.text = str(filename)
		creator = etree.SubElement(root, 'creator')
		creator.text = str(getpass.getuser())
		trackList = etree.SubElement(root, 'trackList')

		for elem in music_list:
			track = etree.SubElement(trackList, 'track')
			location = etree.SubElement(track, 'location')
			location.text = str(elem[0])
			trTitle = etree.SubElement(track, 'title')
			trTitle.text = str(elem[1])
			trCreator = etree.SubElement(track, 'creator')
			trCreator.text = str(elem[2])
			annot = etree.SubElement(track, 'annotation')
			annot.text = "genre : "+ str(elem[4]) +"\nsous-genre : "+ str(elem[5])
			album = etree.SubElement(track, 'album')
			album.text = str(elem[3])

		doc.write(str(filename), xml_declaration=False, encoding='utf-16')


	def generateOut(self, music_list, filename, outFormat):
		filename = filename+'.'+outFormat
		outFile = open(filename, 'w')

		if outFormat == "m3u":
			outFile.write("#EXTM3U\n\n")
			for elem in music_list:
				outFile.write("#EXTINF:"+ str(elem[6]) +','+ str(elem[1]) +'\n')
				outFile.write(str(elem[0]) +'\n\n')
		elif outFormat == "pls":
			i = 0
			outFile.write("[playlist]\n\n")	
			for elem in music_list:
				i += 1
				outFile.write("File"+ str(i) +"="+ str(elem[0]) +'\n')
				outFile.write("Title"+ str(i) +"="+ str(elem[1]) +'\n')
				outFile.write("Length"+ str(i) +"="+ str(elem[6]) +'\n\n')
			outFile.write("NumberOfEntries="+ str(i) +'\n')
			outFile.write("Version=2")
		elif outFormat == "xspf":
			self.toXML(music_list, filename)

		outFile.close()

	init = classmethod(init)
	diffType = classmethod(diffType)
	convert = classmethod(convert)
	chkValue = classmethod(chkValue)
	getSqlBdd = classmethod(getSqlBdd)
	toXML = classmethod(toXML)
	generateOut = classmethod(generateOut)
