# Copyright (C) 2013-2014 Bastian Kleineidam
"""
Define basic configuration data like version or application name.
"""
import _Patool_configdata as configdata

Version = configdata.version
ReleaseDate = configdata.release_date
AppName = configdata.name
App = AppName+" "+Version
Author = configdata.author
Maintainer = configdata.maintainer
Copyright = "Copyright (C) 2004-2014 " + Author
Url = configdata.url
SupportUrl = Url + "issues"
Email = configdata.author_email
