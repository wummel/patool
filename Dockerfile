FROM ubuntu:16.04

# Pre-requisites. System and python
RUN apt-get update && apt-get install -y \
    python-pip \
    python3-pip
RUN pip install \
    pytest

# Setup star.
# Done early so that we very rarely need to redo this.
# Commented out because star is currently failing.
# ADD https://downloads.sourceforge.net/project/s-tar/star-1.5.3.tar.bz2 /star-1.5.3.tar.bz2
# RUN set -x \
# && tar xvf /star-1.5.3.tar.bz2 \
# && cd /star-1.5.3 \
# && make \
# && make install \
# && ln -s /opt/schily/bin/star /bin/star

# Required python archive modules
RUN pip install \
    pylzma

# Required system archive modules.
# Commented out packages are currently broken.
RUN apt-get update && apt-get install -y \
    arc \
    #archmage \
    arj \
    bsdcpio \
    #bsdtar \
    cabextract \
    clzip \
    cpio \
    #flac \
    genisoimage \
    lbzip2 \
    lcab \
    lhasa \
    lrzip \
    lzip \
    lzma \
    lzop \
    # ncompress provides:
    #  - uncompress.real
    #  - compress
    #  - tar_z
    ncompress \
    nomarch \
    p7zip \
    p7zip-full \
    p7zip-rar \
    pbzip2 \
    pdlzip \
    pigz \
    plzip \
    rar \
    rpm \
    rzip \
    sharutils \
    # unace \
    unadf \
    unalz \
    unrar \
    unzip \
    xdms \
    zip \
    zoo \
    #zopfli \
    zpaq

COPY . /patool

RUN pip install -e /patool

WORKDIR /patool

CMD ["pytest", "-v", "./tests"]


