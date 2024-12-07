CC = pyinstaller
EXE = weather.sh
DEPS = pip3 install -r weather/.requirements.txt
REQS = pipreqs --savepath weather/.requirements.txt weather
VERS = 1.0.0
HOME = weather-plotter-$(VERS)
DDIR = dist
MAIN = weather/app.py

.PHONY: all dist exec buildir localdeploy install package prep clean

all: clean buildir prep

dist: all localdeploy

exec: all package localdeploy

buildir:
	if test -n $(DDIR)/$(HOME); then mkdir -p $(DDIR)/$(HOME); fi

localdeploy:
	cd $(DDIR); \
	chmod +x $(HOME)/$(EXE); \
	tar czf $(HOME).tgz $(HOME)

install: $(TARGET)
	install $(TARGET) ~/bin

package:
	PYTHONPATH=${PWD} $(DEPS) -t $(DDIR)/$(HOME)/lib/

prep:
#	PYTHONPATH=${PWD} $(REQS)
	cp -r config data weather $(DDIR)/$(HOME)
	cp $(EXE) README.md $(DDIR)/$(HOME)
	mkdir $(DDIR)/$(HOME)/lib
	mkdir $(DDIR)/$(HOME)/logs

clean:
	rm -rf $(DDIR)/$(HOME) 2> /dev/null
