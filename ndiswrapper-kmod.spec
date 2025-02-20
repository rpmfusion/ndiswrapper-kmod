%if 0%{?fedora} || 0%{?rhel} > 7
%global buildforkernels akmod
%endif
%global debug_package %{nil}

#global pre rc1

Summary:	Ndiswrapper kernel module
Name: 		ndiswrapper-kmod
Version: 	1.63
Release: 	11%{?pre}%{?dist}
License: 	GPLv2
URL:		http://ndiswrapper.sourceforge.net
Source0: 	http://downloads.sf.net/ndiswrapper/ndiswrapper-%{version}%{?pre}.tar.gz
Source11:	ndiswrapper-kmodtool-excludekernel-filterfile
Patch0:		ndiswrapper-kmod-nomodinfo.patch
Patch1:     kernel-5.8.patch
Patch2:     kernel-5.17.patch
Patch3:     kernel-5.18.patch
Patch4:     kernel-pseed.patch

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
%setup -q -c -T -a 0 -n %{name}-%{version}%{?pre}
(cd ndiswrapper-%{version}%{?pre} ; 
%patch -P0 -p1 -b .orig
%patch -P1 -p1 -b .orig
%patch -P2 -p1 -b .orig
%patch -P3 -p1 -b .orig2
%patch -P4 -p1 -b .pseed
)
sed -i 's|/sbin/depmod -a|/bin/true|' ndiswrapper-%{version}%{?pre}/driver/Makefile
for kernel_version  in %{?kernel_versions} ; do
    cp -a ndiswrapper-%{version}%{?pre} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    make V=1 %{?_smp_mflags} -C _kmod_build_${kernel_version%%___*} KVERS="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KBUILD="${kernel_version##*___}" -C driver 
done


%install
for kernel_version  in %{?kernel_versions} ; do
    make -C _kmod_build_${kernel_version%%___*}/driver KVERS="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KBUILD="${kernel_version##*___}" INST_DIR=$RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
	chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
done
%{?akmod_install}


%changelog
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.63-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.63-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.63-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.63-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Oct 14 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.63-7
- Update prandom_seed

* Thu Sep 01 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.63-6
- Update for kernel 5.17 from leigh
- Update for kernel 5.18 from kwizart

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.63-1
- Update to 1.63
- Patch for 5.8 kernel

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 22 2020 Leigh Scott <leigh123linux@gmail.com> - 1.62-1
- Update to 1.62

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.61-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.61-12
- Patch for 5.3 and 5.4 kernel

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.61-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Apr 07 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.61-10
- Patch for 5.0 kernel

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.61-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.61-8
- Package clean-up
- Drop some changelog

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.61-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 11 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.61-6
- Patch for 4.15 kernel

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.61-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 14 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.61-4
- Patch for 4.13 kernel

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.61-2
- Patch for 4.11 kernel

* Tue Jun 27 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.61-1
- Update to 1.61

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 19 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.60-2
- Patch for 4.7 kernel

* Sun Jun 19 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.60-1
- Update to 1.60

* Mon May 25 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.59-8
- Patch for 4.0.0 kernel

* Sun May 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.59-7.25
- Rebuilt for kernel


