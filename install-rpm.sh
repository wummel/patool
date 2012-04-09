python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# 'brp-compress' compresses the manpages without distutils knowing.
# The sed scripts append ".gz", ".bz2" or ".xz" suffixes to the affected
# manpage filenames.

if [ -n "$( ls $RPM_BUILD_ROOT/usr/share/man/man*/*.bz2 2>/dev/null )" ]; then
    # add .bz2 suffix
    sed -i -e 's@man/man\([[:digit:]]\)/\(.\+\.[[:digit:]]\)$@man/man\1/\2.bz2@g' INSTALLED_FILES
elif [ -n "$( ls $RPM_BUILD_ROOT/usr/share/man/man*/*.xz 2>/dev/null )" ]; then
    # add .xz suffix
    sed -i -e 's@man/man\([[:digit:]]\)/\(.\+\.[[:digit:]]\)$@man/man\1/\2.xz@g' INSTALLED_FILES
else
    # assume that man pages have a ".gz" suffix
    sed -i -e 's@man/man\([[:digit:]]\)/\(.\+\.[[:digit:]]\)$@man/man\1/\2.gz@g' INSTALLED_FILES
fi
