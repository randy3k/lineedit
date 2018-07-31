all:

update-deps:
	cd lineedit/deps && \
	rm -rf prompt_toolkit && \
	svn export https://github.com/jonathanslenders/python-prompt-toolkit/tags/2.0.4/prompt_toolkit

clean:
	find . -d -name __pycache__ -exec rm -rf {} \; &&\
	find . -d -name *.pyc -exec rm -rf {} \;
