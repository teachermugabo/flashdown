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
	@echo "Building Bootstrap Custom Extensions (bootstrap.css)"
	@echo "${HR}\n"
	@recess --compile ${BOOTSTRAP_LESS} > ${BOOTSTRAP}
	@echo "Compiling LESS with Recess...               ${CHECK} Done\n"

watch:
	echo "Watching less files..."; \
	watchr -e "watch('.*\.less') { system 'make' }"

.PHONY: clean less
