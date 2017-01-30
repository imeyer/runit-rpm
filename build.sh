#!/bin/sh

whereami=$(dirname $0)

if [ ! -f "/etc/rpm/macros.dist" ] && \
   [ ! -f "/etc/rpm/macros.disttag" ];   then echo "please install 'buildsys-macros' rpm and try again" ; exit 1 ; fi
if [ ! -f "$(which rpmbuild)" ];         then echo "please install 'rpm-build' rpm and try again" ; exit 1 ; fi
if [ ! -f "$(which spectool)" ];         then echo "please install 'rpmdevtools' rpm and try again" ; exit 1 ; fi
if [ ! -f "$(which rpmdev-setuptree)" ]; then echo "please install 'rpmdevtools' rpm and try again" ; exit 1 ; fi

# Might create ~/rpmbuild, or it might use an existing build %{_topdir}
# named in ~/.rpmmacros
/usr/bin/rpmdev-setuptree

SPECS=$(rpm --eval "%{_specdir}")
SOURCES=$(rpm --eval "%{_sourcedir}")
cp -f "${whereami}/runit.spec" "$SPECS"
cp -f "${whereami}"/*.patch    "$SOURCES"
cp -f "${whereami}/runsvdir-start.service"    "$SOURCES"
/usr/bin/spectool -C "$SOURCES" -g "${whereami}/runit.spec "

PATH=/usr/bin:/bin
rpmbuild -bb "$SPECS/runit.spec"
