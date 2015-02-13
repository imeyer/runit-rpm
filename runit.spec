#
# spec file for package runit (Version 2.1.2)
#
# Copyright (c) 2010 Ian Meyer <ianmmeyer@gmail.com>

## This package understands the following switches:
## --with dietlibc ...  statically links against dietlibc

Name:           runit
Version:        2.1.2
Release:        1%{?_with_dietlibc:diet}%{?dist}

Group:          System/Base
License:        BSD

# Override _sbindir being /usr/sbin
%define _sbindir /sbin

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Url:            http://smarden.org/runit/
Source0:        http://smarden.org/runit/runit-%{version}.tar.gz
Source1:        runsvdir-start.service
Patch:          runit-2.1.2-etc-service.patch
Patch1:         runit-2.1.2-runsvdir-path-cleanup.patch
Patch2:         runit-2.1.2-term-hup-option.patch

Obsoletes: runit <= %{version}-%{release}
Provides: runit = %{version}-%{release}

BuildRequires: make gcc
%if 0%{?rhel} >= 6
BuildRequires:  glibc-static
%endif

%{?_with_dietlibc:BuildRequires:        dietlibc}

Summary:        A UNIX init scheme with service supervision

%description
runit is a cross-platform Unix init scheme with service supervision; a
replacement for sysvinit and other init schemes. It runs on GNU/Linux, *BSD,
Mac OS X, and Solaris, and can easily be adapted to other Unix operating
systems. runit implements a simple three-stage concept. Stage 1 performs the
system's one-time initialization tasks. Stage 2 starts the system's uptime
services (via the runsvdir program). Stage 3 handles the tasks necessary to
shutdown and halt or reboot.

Authors:
---------
    Gerrit Pape <pape@smarden.org>

%prep
%setup -q -n admin/%{name}-%{version}
pushd src
echo "%{?_with_dietlibc:diet -Os }%__cc $RPM_OPT_FLAGS" >conf-cc
echo "%{?_with_dietlibc:diet -Os }%__cc -Os -pipe"      >conf-ld
popd
%patch
%patch1
%patch2

%build
sh package/compile

%install
EXTRA_FILES=$RPM_BUILD_ROOT/extra_files
touch %{EXTRA_FILES}

for i in $(< package/commands) ; do
    %{__install} -D -m 0755 command/$i %{buildroot}%{_sbindir}/$i
done
for i in man/*8 ; do
    %{__install} -D -m 0755 $i %{buildroot}%{_mandir}/man8/${i##man/}
done
%{__install} -d -m 0755 %{buildroot}/etc/service
%{__install} -D -m 0750 etc/2 %{buildroot}%{_sbindir}/runsvdir-start

# For systemd only
%if 0%{?rhel} >= 7
%{__install} -D -p -m 0644 $RPM_SOURCE_DIR/runsvdir-start.service \
                       $RPM_BUILD_ROOT%{_unitdir}/runsvdir-start.service
echo %{_unitdir}/runsvdir-start.service > %{EXTRA_FILES}
%endif

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 = 1 ] ; then
  %if 0%{?rhel} >= 6 <= 7
    rpm --queryformat='%%{name}' -qf /sbin/init | grep -q upstart
    if [ $? -eq 0 ]; then
      cat >/etc/init/runsvdir.conf <<\EOT
# for runit - manage /usr/sbin/runsvdir-start
start on runlevel [2345]
stop on runlevel [^2345]
normal exit 0 111
respawn
exec /sbin/runsvdir-start
EOT
    # tell init to start the new service
      start runsvdir
    fi
  %endif

  %if 0%{?rhel} >= 7
    systemctl enable runsvdir-start
    systemctl start runsvdir-start
  %endif

  %if 0%{?rhel} < 6
    grep -q 'RI:2345:respawn:/sbin/runsvdir-start' /etc/inittab
    if [ $? -eq 1 ]; then
      echo -n "Installing /sbin/runsvdir-start into /etc/inittab.."
      echo "RI:2345:respawn:/sbin/runsvdir-start" >> /etc/inittab
      echo " success."
      # Reload init
      telinit q
    fi
  %endif
fi

%preun
if [ $1 = 0 ]; then
  if [ -f /etc/init/runsvdir.conf ]; then
    stop runsvdir
  fi
fi

%postun
if [ $1 = 0 ]; then
  if [ -f /etc/init/runsvdir.conf ]; then
    rm -f /etc/init/runsvdir.conf
  else
    echo " #################################################"
    echo " # Remove /sbin/runsvdir-start from /etc/inittab #"
    echo " # if you really want to remove runit            #"
    echo " #################################################"
  fi
fi

%files -f %{EXTRA_FILES}
%defattr(-,root,root,-)
%{_sbindir}/chpst
%{_sbindir}/runit
%{_sbindir}/runit-init
%{_sbindir}/runsv
%{_sbindir}/runsvchdir
%{_sbindir}/runsvdir
%{_sbindir}/sv
%{_sbindir}/svlogd
%{_sbindir}/utmpset
%{_sbindir}/runsvdir-start
%{_mandir}/man8/*.8*
%doc doc/* etc/
%doc package/CHANGES package/COPYING package/README package/THANKS package/TODO
%dir /etc/service

%changelog
* Thu Aug 21 2014 Chris Gaffney <gaffneyc@gmail.com> 2.1.2-1
- Initial release of 2.1.2

* Fri Jan 20 2012 Joe Miller <joeym@joeym.net> 2.1.1-6
- modified spec to build on centos-5 (by only requiring glibc-static on centos-6)

* Wed Oct 26 2011 Karsten Sperling <mail@ksperling.net> 2.1.1-5
- Optionally shut down cleanly even on TERM
- Don't call rpm in preun, it can cause problems
- Upstart / inittab tweaks

* Wed Jul 20 2011 Robin Bowes <robin.bowes@yo61.com> 2.1.1-4
-  2.1.1-3 Add BuildRequires
-  2.1.1-4 Support systems using upstart

* Sun Jan 23 2011 ianmmeyer@gmail.com
- Make compatible with Redhat based systems
