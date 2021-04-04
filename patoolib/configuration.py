# Copyright (C) 2013-2015 Bastian Kleineidam
"""
Define basic configuration data like version or application name.
"""
try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore

meta = metadata.metadata("patool")

Version = metadata.version("patool")
ReleaseDate = "17.1.2016"  # from first line of doc/changelog.txt
AppName = meta["Name"]
App = AppName+" "+Version
Author = meta["Author"]
Maintainer = meta["Maintainer"]
Copyright = "Copyright (C) 2004-2015 " + Author
Url = meta["Home-page"]
SupportUrl = "https://github.com/wummel/patool/issues/"
Email = meta["Author-email"]
