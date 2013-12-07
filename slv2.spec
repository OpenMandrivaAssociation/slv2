%define major 9
%define libname %mklibname %{name} _%{major}
%define develname %mklibname -d %{name}

Summary:    A library for simple use of LV2 plugins
Name:       slv2
Version:    0.6.6
Release:    10
Group:      System/Libraries
License:    GPLv2+
URL:        http://wiki.drobilla.net/SLV2
Source0:    http://download.drobilla.net/%{name}-%{version}.tar.bz2
Patch0:        slv2-0.6.6-ladspa2lv2_fix.diff
Patch1:        slv2-0.6.6-gcc46linking.diff
BuildRequires:  doxygen
BuildRequires:  jackit-devel
BuildRequires:  liblrdf-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(lv2core)
BuildRequires:  raptor-devel
BuildRequires:  rasqal-devel
BuildRequires:  redland-devel >= 1.0.6
BuildRequires:  python
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SLV2 is a library geared towards music and audio applications which makes the
use of LV2 plugins <http://lv2plug.in> as simple as possible.

This binary package contains various binaries:

 o lv2_inspect - Display information about an LV2 plugin.
 o lv2_jack_host - SLV2 Jack Host.
 o lv2_list - List system installed LV2 plugins.
 o lv2_simple_jack_host - SLV2 Simple Jack Host Example.

%package -n %{libname}
Summary:    A library for simple use of LV2 plugins
Group:          System/Libraries

%description -n %{libname}
SLV2 is a library geared towards music and audio applications which makes the
use of LV2 plugins <http://lv2plug.in> as simple as possible.

%package -n %{develname}
Summary:    Development files (headers) for SLV2
Group:      Development/C
Requires:   %{libname} = %{version}
Provides:   %{name}-devel = %{version}

%description -n %{develname}
Files required for compiling programs which use SLV2, and developer
documentation.

%prep

%setup -q -n %{name}-%version
%patch0 -p0
%patch1 -p0

# antiborker
perl -pi -e "s|/sbin/ldconfig|/bin/true|g" *.py

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" *.py

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

python ./waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}/ \
    --mandir=%{_mandir} \
    --build-docs

python ./waf build --verbose


%install
rm -rf %{buildroot}

DESTDIR=%{buildroot} python ./waf install --verbose
strip %{buildroot}/%{_libdir}/libslv2.so.%{major}*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/ladspa2lv2
%{_bindir}/lv2_inspect
%{_bindir}/lv2_jack_host
%{_bindir}/lv2_list
%{_bindir}/lv2_simple_jack_host
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS README
%attr(0755,root,root) %{_libdir}/libslv2.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc build/default/doc/html/*
%{_includedir}/slv2/*.h
%attr(0755,root,root) %{_libdir}/*.so
%{_libdir}/pkgconfig/slv2.pc
%{_mandir}/man3/*


%changelog
* Wed Apr 25 2012 Frank Kober <emuse@mandriva.org> 0.6.6-6
+ Revision: 793250
- added gcc46 linking wscript patch and strip library
- rebuild with new lv2 specification 1.0.0

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.6-5
+ Revision: 669989
- mass rebuild

* Sun Feb 13 2011 Frank Kober <emuse@mandriva.org> 0.6.6-4
+ Revision: 637435
- rebuild for fixed redland

* Sat Dec 04 2010 Frank Kober <emuse@mandriva.org> 0.6.6-3mdv2011.0
+ Revision: 609142
- fix manpage suffix

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Thu Apr 22 2010 Frank Kober <emuse@mandriva.org> 0.6.6-1mdv2010.1
+ Revision: 537981
- move to version 0.6.6, rediff patch, include manpages

* Sun Feb 28 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.6.1-3mdv2010.1
+ Revision: 512806
- rebuild for new rasqal

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.6.1-2mdv2010.0
+ Revision: 427196
- rebuild

* Tue Nov 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdv2009.1
+ Revision: 304225
- 0.6.1

* Sat Oct 25 2008 Götz Waschk <waschk@mandriva.org> 0.6.0-1mdv2009.1
+ Revision: 297135
- new version
- drop extra sources
- fix devel deps
- fix file list
- update license

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 0.6.0-0.r1162.1mdv2009.0
+ Revision: 217195
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-0.r1162.1mdv2008.1
+ Revision: 182965
- import slv2


* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-0.r1162.1mdv2008.1
- initial Mandriva release
