# lineedit: a readline library based on prompt_toolkit which supports multiple modes

[![CircleCI](https://circleci.com/gh/randy3k/lineedit/tree/master.svg?style=shield)](https://circleci.com/gh/randy3k/lineedit/tree/master)
[![Build status](https://ci.appveyor.com/api/projects/status/asy3mr1865kkh12k/branch/master?svg=true)](https://ci.appveyor.com/project/randy3k/lineedit/branch/master)
[![pypi](https://img.shields.io/pypi/v/lineedit.svg)](https://pypi.org/project/lineedit/)

It provides some subclasses inherited from [prompt_toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) to mimic Julia [LineEdit.jl](https://github.com/JuliaLang/julia/blob/master/stdlib/REPL/src/LineEdit.jl) with multiple modal support.

As IPython is blocking the update of prompt_toolkit in python 2.7, we are shipping a copy of prompt-toolkit for python 2 users.
