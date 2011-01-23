# What the?

I like [runit](http://smarden.org/runit/). A lot. I also like [Redhat](http://www.redhat.com). A lot. What I didn't like was the lack of widely distributed RPMs for [runit](http://smarden.org/runit/). [Scott Likens](http://likens.us/runit/) made an RPM for version 2.0, so I thought I'd be a pal and take his RPM, update it to 2.1.1 and put it on Github for everyone to fork/clone/make fun of.

So, thanks to Scott for the RPMs and thanks to [SuSE](http://www.opensuse.org/) for the original spec/RPMs

## Building

1. Clone the repo
1. `cd $RPMBUILD_DIR` (On RHEL <= 5 this will be `/usr/src/redhat`, anything later will be `~/rpmbuild`)
1. copy `runit.spec` to your `SPECS` directory
1. copy `runit-2.1.1-etc-service.patch` and `runit-2.1.1-runsvdir-path-cleanup.patch` to the `SOURCES` directory
1. `cd $RPMBUILD_DIR/SPECS; rpmbuild -bb runit.spec`
1. Install the RPM
1. PROFIT!