#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''importation des bibliotheques nécessaires'''
from config import *

'''argparse'''
parser = argparse() #contient le parser définit dans config
scan = parser.parse_args() #la variable 'scan' conservera l'ensemble des arguments

'''logging'''
fmt = "%(levelname)s %(asctime)s : %(message)s"
datefmt="%d/%m/%Y - %H:%M:%S"
log = logging('playlist.log', scan.verbeux, fmt, datefmt) #permet de conçevoir un logging dépendant du mode verbose

functions.init(log) #initialise le logging pour les fonctions de config

for ARG in ['nom', 'format', 'temps']:
	elem = getattr(scan, ARG)
	if elem is not None:
		log.debug(ARG+" -> "+elem)

scan.format = scan.format.lower()
scan.temps = functions.convert(scan.temps, 666)
if scan.temps == False:
	print("le temps spécifié n'est pas au format valide")
	quit()
#configuration de base et logging
##############################
dict_args = dict() #contiendra uniquement les arguments optionnels
for ARGS in ['genre', 'sousgenre', 'artiste', 'album', 'titre']:
	if getattr(scan, ARGS) is not None:
		arg_list = getattr(scan, ARGS)
		dict_args[ARGS] = arg_list
		for elem in dict_args[ARGS]:
			elem[1] = functions.convert(elem[1], 666)

log.debug(dict_args)

pourcentage = dict() #contiendra les pourcentages selon l'argument
for ARGS in dict_args:
	pourcentage[ARGS] = dict_args
	for elem in dict_args[ARGS]:
		if elem[1] != False:
			pourcentage[ARGS] = elem[1]
		else:
			print("Le pourcentage de "+ ARGS +" n'est pas au format valide")
			quit()

log.debug(pourcentage)
#récupération des arguments et factorisation des pourcentages
##################################
where = str() #contiendra la requête SQL (condition uniquement)
i = 0

for ARGS in dict_args:
	for elem in dict_args[ARGS]:
		if i == 1:
			if scan.intersection:
				where += " AND " + ARGS + " ~ '"+ elem[0] +"'"
			else:
				where += " OR " + ARGS + " ~ '"+ elem[0] +"'"
		else:
			where += ARGS + " ~ '"+ elem[0] +"'"
			i = 1


log.debug("conditions SQL (regex compris) : WHERE "+where)

sql = functions.getSqlBdd('etudiant:passe', '172.16.99.2:5432', 'radio_libre', where) #contiendra le résultat de la requête
music_list = list(sql)

for elem in music_list:
	log.info(elem)
#récupération de la liste des musiques exigées
###################################

functions.generateOut(music_list, scan.nom, scan.format)

#génération de la playlist
###############################
