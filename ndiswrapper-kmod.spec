# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

#global _rc rc1

Summary:	Ndiswrapper kernel module
Name: 		ndiswrapper-kmod
Version: 	1.57
Release: 	2%{?dist}.17
License: 	GPLv2
Group: 		System Environment/Kernel
URL:		http://ndiswrapper.sourceforge.net
Source0: 	http://downloads.sf.net/ndiswrapper/ndiswrapper-%{version}%{?_rc}.tar.gz
Source11:	ndiswrapper-kmodtool-excludekernel-filterfile
Patch0:		ndiswrapper-kmod-nomodinfo.patch
Patch1:         ndiswrapper_3.3_kernel.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The ndiswrapper project makes it possible to use WLAN-Hardware 
with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.  These rpms contain
just the kernel module and loader. You will also need the Windows driver 
for your card.

WARNING: Fedora-Kernels use 4K size stack. Many Windows drivers
will need at least 8K size stacks. For details read the wiki on:
http:/ndiswrapper.sourceforge.net

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
# go
%setup -q -c -T -a 0 -n %{name}-%{version}%{?_rc}
(cd ndiswrapper-%{version} ; 
%patch0 -p1 -b .orig
%patch1 -p1 -b .orig
)
sed -i 's|/sbin/depmod -a|/bin/true|' ndiswrapper-%{version}%{?_rc}/driver/Makefile
for kernel_version  in %{?kernel_versions} ; do
    cp -a ndiswrapper-%{version}%{?_rc} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    make V=1 %{?_smp_mflags} -C _kmod_build_${kernel_version%%___*} KVERS="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KBUILD="${kernel_version##*___}" -C driver 
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version  in %{?kernel_versions} ; do
    make -C _kmod_build_${kernel_version%%___*}/driver KVERS="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KBUILD="${kernel_version##*___}" INST_DIR=$RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
	chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Jun 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.17
- Rebuilt for updated kernel

* Thu Jun 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.16
- Rebuilt for updated kernel

* Sun Jun 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.15
- Rebuilt for updated kernel

* Tue Jun 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.14
- Rebuilt for updated kernel

* Sun May 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.13
- Rebuilt for updated kernel

* Sat May 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.11
- Rebuilt for release kernel

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.10
- Rebuilt for release kernel

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.9
- rebuild for updated kernel

* Wed May 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.8
- rebuild for updated kernel

* Sun May 06 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.7
- rebuild for updated kernel

* Sat May 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.6
- rebuild for updated kernel

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.5
- rebuild for updated kernel

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.4
- rebuild for updated kernel

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.3
- rebuild for updated kernel

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.2
- rebuild for updated kernel

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-2.1
- rebuild for beta kernel

* Fri Mar 30 2012 leigh scott <leigh123linux@googlemail.com> - 1.57-2
- patched for 3.3.0 kernel
- fix release tag

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-1.1
- Rebuild for UsrMove

* Wed Jan 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.57-1
- Update to 1.57

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.57-0.1rc1.1
- Rebuild for F-16 kernel

* Tue Nov 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.57-0.1rc1
- Update to 1.57rc1

* Tue Nov 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.56-2.5
- Rebuild for F-16 kernel

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.56-2.4
- Rebuild for F-16 kernel

* Sun Oct 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.56-2.3
- Rebuild for F-16 kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.56-2.2
- rebuild for F15 release kernel

* Thu May 26 2011 Tristan Moody <tmoody [AT] ku [DOT] edu> - 1.56-1.1
- remove redundant defines that break build on new F-15 kernel

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.15
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.14
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.13
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.12
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.11
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.10
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.9
- rebuild for new kernels

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.8
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.7
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.6
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.5
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.4
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.3
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.2
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-4.1
- rebuild for new kernels

* Sun Apr 23 2009 Xavier lamien <lxtnow@gmail.com> - 1.54.4
- Fix pool_controller against kernel-2.6.29.

* Sun Apr 23 2009 Xavier lamien <lxtnow@gmail.com> - 1.54.3
- Disable iw-event drv patch (inclued by upstream).

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-2.19
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.54-2.18
- rebuild for new F11 features

* Sat Feb 21 2009 Xavier Lamien <lxtnow@gmail.com> - 1.54-1
- Update release.

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.18
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.17
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.16
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.15
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.14
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.13
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.12
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.11
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.10
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.9
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.8
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.3
- rebuild for latest rawhide kernel

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.53-5.2
- rebuild for latest rawhide kernel

* Sat Oct 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.53-5.1
- rebuild for rpm fusion

* Wed Oct 01 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.53-4.1
- rebuild for new kernels

* Sun Sep 07 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.53-3.1
- new release scheme with an additional number in release
- build new akmod package

* Sat Aug 16 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.53-3
- rebuild for new kernels

* Thu Jul 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.53-2
- rebuild for new Fedora kernels

* Tue Jul 15 2008 kwizart < kwizart at gmail.com > - 1.53-1
- Update to 1.53
- Exclude xen (does it really works ?)
- Update for WE

* Tue Jul 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-35
- rebuild for new Fedora kernels

* Wed Jul 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-34
- rebuild for new Fedora kernels

* Fri Jun 13 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-33
- rebuild for new Fedora kernels

* Fri Jun 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-32
- rebuild for new Fedora kernels

* Thu May 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-31
- rebuild for new Fedora kernels

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-30
- build for f9

* Sat Feb 16 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.52-1
- update to 1.52

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.51-2
- rebuild for new kmodtools, akmod adjustments

* Sun Jan 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.51-1
- build akmods package
- update to 1.51

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-18
- rebuilt for 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-17
- rebuilt for 2.6.23.8-63.fc8 2.6.21-2952.fc8xen
- enable debuginfo packages again

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-16
- rebuilt for 2.6.23.1-49.fc8

* Mon Nov 05 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-15
- rebuilt for F8 kernels

* Wed Oct 31 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-14
- rebuilt for latest kernels

* Tue Oct 30 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-13
- rebuilt for latest kernels

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-12
- rebuilt for latest kernels
- adjust to rpmfusion and new kmodtool

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-11
- rebuilt for latest kernels

* Tue Oct 23 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-10
- rebuilt for latest kernels

* Mon Oct 22 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-9
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-8
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-7
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-6
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-5
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.48-4
- rebuilt for latest kernels

* Tue Oct 09 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 1.48-3
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> 
- build for rawhide kernels as of today

* Wed Oct 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.48-1
- Update to 1.48
- update for new kmod-helper stuff
- build for newest kernels

* Tue May 13 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.43-1
- Update to 1.43

* Tue Mar 13 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.38-1
- Update to 1.38

* Sat Oct 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.25-1
- Update to 1.25
- Enable xen

* Mon Jun 26 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.18-2
- disable xen 

* Mon Jun 26 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.18-1
- Update to 1.18

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.13-4
- Invoke kmodtool with bash instead of sh.

* Sun May 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.13-3
- Require version >= of ndiswrapper-kmod-common.
- Provide *-kmod instead of kmod-* to fix upgrade woes (#970).

* Thu Apr 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.13-2
- Provide "kernel-modules" instead of "kernel-module" to match yum's config.

* Sun Apr 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.13-1.1
- KBUILD-hack still needed for *some* kernels :-/

* Sun Apr 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.13-1
- Update to 1.13
- Remove KBUILD-hack again

* Wed Apr 05 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.12-2
- Use KBUILD in addition to KSRC to fix build

* Wed Apr 05 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.12-1
- Update to 1.12

* Tue Mar 27 2006 <fedora[AT]leemhuis.info> - 1.10-4
- small adjustments to kmod specific tasks
- update kmodtool to 0.10.6

* Sat Mar 18 2006 <fedora[AT]leemhuis.info> - 1.10-3
- drop 0.lvn
- use kmodtool from svn
- hardcode kernel and variants

* Mon Feb 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.10-0.lvn.3
- Add URL to kmodtool.

* Sun Feb 12 2006 <fedora[AT]leemhuis.info> - 1.10-0.lvn.2
- split into packages for userland and kmod
- Drop epoch

* Sun Feb 12 2006 <fedora[AT]leemhuis.info> - 0:1.9-0.lvn.1
- Update to 1.10

* Sat Feb 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0:1.9-0.lvn.2
- Fix doc dir modes.

* Sat Feb 11 2006 <fedora[AT]leemhuis.info> - 0:1.9-0.lvn.1
- Update to 1.9

* Sun Feb  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 0:1.8-0.lvn.2
- Temporary hack for 2.6.16/2.6.15 version skew in FC5test* kernels.
- Fix doc file modes.

* Tue Jan 17 2006 <fedora[AT]leemhuis.info> - 0:1.8-0.lvn.1
- Update to 1.8

* Sat Dec 10 2005 <fedora[AT]leemhuis.info> - 0:1.7-0.lvn.1
- Update to 1.7

* Sat Dec 03 2005 <fedora[AT]leemhuis.info> - 0:1.6-0.lvn.1
- Update to 1.6
- New BR: libusb-devel for new file load_fw_ar5523

* Sat Nov 05 2005 <fedora[AT]leemhuis.info> - 0:1.5-0.lvn.1
- Update to 1.5

* Sun Oct 16 2005 <fedora[AT]leemhuis.info> - 0:1.4-0.lvn.1
- Update to 1.4
- strip kernel-module

* Fri Jun 17 2005 <fedora[AT]leemhuis.info> - 0:1.2-0.lvn.3
- Pass KSRC to make install call, too

* Fri Jun 17 2005 Dams <anvil[AT]livna.org> - 0:1.2-0.lvn.2
- Fixed Source0 URL.

* Mon Jun 13 2005 <fedora[AT]leemhuis.info> - 0:1.2-0.lvn.1
- Update to 1.2
- Rework installation
- Rework kernel-devel usage

* Tue Mar 22 2005 <aaron.bennett@olin.edu> - 0:1.1-0.lvn.1
- Updated to version 1.1

* Mon Jan 31 2005  <aaron.bennett@olin.edu> - 0:1.0-0.lvn.1
- updated to version 1.0

* Fri Nov 26 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> 0:0.12-0.lvn.1
- Update to 0.12
- Trim Doc in header
- Trim description and add 4k-Warning 
- Depend on /boot/vmlinuz correctly
- use --without driverp to skip utiliy/core-Package
- Remove the included fedora-kmodhelper
- Make modpath readable for normal users

* Mon Nov 8 2004 <aaron.bennett@olin.edu> 0:0.11-0.lvn.2
- changed make to use %{?_smp_mflags}

* Sun Oct 24 2004 <fedora AT leemhuis DOT info> 0:0.11-0.lvn.1
- Use fedora-kmodhelper like in other rlo packages like ati-fglrx
- Update to 0.11

* Sun Aug 29 2004 <fedora AT leemhuis DOT info> 0:0.10-0.lvn.1
- Integrate fedora-kmodhelper as long as fedora.us version is not ready
- Use correct kernel-headers to build
- Allow separate building of tools and kernel-module
- show fedora-kmodhelper diag
- some minor fixes

* Mon Jun 14 2004 <aaron.bennett@olin.edu> 0:0.8-0.fdr.2
- removed extra kmodhelper stuff
- removed old depmod flag from 2.4 kernel

* Thu Jun 10 2004 <aaron.bennett@olin.edu> 0:0.8-0.fdr.1
- moved /usr/sbin/loadndisdriver to /sbin/loadndisdriver
- revised new build with version 0.8 of ndiswrapper from upstream

* Tue Jun 8 2004 <aaron.bennett@olin.edu> - 0:0.7-0.fdr.2
- changed ndiswrapper.o to ndiswrapper.ko for 2.6 kernel
- added Requires: ndiswrapper to kernel module ndiswrapper

* Thu Jun 3 2004  <aaron.bennett@olin.edu> - 0:0.7-0.fdr.1
- Initial build.


