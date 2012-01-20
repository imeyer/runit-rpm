#!/bin/sh

whereami=$(dirname $0)

if [ ! -f "$(which rpmbuild)" ];         then echo "please install 'rpm-build' package and try again" ; exit 1 ; fi
if [ ! -f "$(which spectool)" ];         then echo "please install 'rpmdevtools' package and try again" ; exit 1 ; fi
if [ ! -f "$(which rpmdev-setuptree)" ]; then echo "please install 'rpmdevtools' package and try again" ; exit 1 ; fi

# creates ~/rpmbuild
/usr/bin/rpmdev-setuptree

cp -f ${whereami}/runit.spec ~/rpmbuild/SPECS/
cp -f ${whereami}/*.patch    ~/rpmbuild/SOURCES/
/usr/bin/spectool -C ~/rpmbuild/SOURCES/ -g ${whereami}/runit.spec 

rpmbuild -bb ~/rpmbuild/SPECS/runit.spec
