# - hh_combination Makefile

all : build

build : RooStatTools


RooStatTools :
	cd ./submodules/RooStatTools/; make
