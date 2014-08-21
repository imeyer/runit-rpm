# What the?

I like [runit](http://smarden.org/runit/). A lot. I also like [Redhat](http://www.redhat.com). A lot. What I didn't like was the lack of widely distributed RPMs for [runit](http://smarden.org/runit/). [Scott Likens](http://likens.us/runit/) made an RPM for version 2.0, so I thought I'd be a pal and take his RPM, update it to 2.1.2 and put it on Github for everyone to fork/clone/make fun of.

So, thanks to Scott for the RPMs and thanks to [SuSE](http://www.opensuse.org/) for the original spec/RPMs

## Building

```
yum -q -y install rpmdevtools git glibc-static
yum -q -y groupinstall "Development Tools"
git clone https://github.com/imeyer/runit-rpm runit-rpm
cd ./runit-rpm
./build.sh
sudo rpm -i ~/rpmbuild/RPMS/*/*.rpm
```
