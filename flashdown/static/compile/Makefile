BOOTSTRAP = ../css/bootstrap.css
BOOTSTRAP_LESS = bootstrap.less
CHECK=\033[32m✔\033[39m
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#

less: custom
	@echo "\n${HR}"
	@echo "Building non-bootstrap less files"
	@echo "${HR}\n"
	@recess --compile markdown-editor.less > ../css/markdown-editor.css
	@echo "Compiling LESS with Recess...               ${CHECK} Done\n"

custom: 
	@echo "\n${HR}"
	@echo "Building Bootstrap Custom Extensions (site.css)"
	@echo "${HR}\n"
	@recess --compile ${BOOTSTRAP_LESS} > ${BOOTSTRAP}
	@echo "Compiling LESS with Recess...               ${CHECK} Done\n"

# build bootstrap, copy the files we need -- rarely, if ever need to do this
bootstrap:
	cd bootstrap && make
	cp -r bootstrap/img/* ../img
	cp bootstrap/docs/assets/js/bootstrap.js ../js/bootstrap.js
	cp bootstrap/docs/assets/js/bootstrap.min.js ../js/bootstrap.min.js 

all: bootstrap custom

watch:
	echo "Watching less files..."; \
	watchr -e "watch('.*\.less') { system 'make' }"

.PHONY: bootstrap clean less
