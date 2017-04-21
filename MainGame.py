#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, os, random
import logging
import olpcgames
from pygame.locals import *
from src.Juego import Juego

def main():
	Juego().launch()

if __name__ == "__main__":
    main()