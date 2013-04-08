# Copyright (C) 2013 Bastian Kleineidam
"""
Define basic configuration data like version or application name.
"""
import _Patool_configdata as configdata

Version = configdata.version
ReleaseDate = configdata.release_date
AppName = configdata.name
App = AppName+u" "+Version
Author = configdata.author
Maintainer = configdata.maintainer
Copyright = u"Copyright (C) 2004-2008 " + Author
Url = configdata.url
SupportUrl = Url + u"issues"
Email = configdata.author_email
