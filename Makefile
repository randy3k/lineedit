update-deps:
	cd lineedit/deps && \
	rm -rf prompt_toolkit && \
	svn export https://github.com/jonathanslenders/python-prompt-toolkit/tags/2.0.2/prompt_toolkit

clean-cache:
	find . -d -name __pycache__ -exec rm -rf {} \; &&\
	find . -d -name *.pyc -exec rm -rf {} \;
