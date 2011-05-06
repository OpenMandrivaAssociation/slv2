%define major 9
%define libname %mklibname %{name} _%{major}
%define develname %mklibname -d %{name}

Summary:    A library for simple use of LV2 plugins
Name:       slv2
Version:    0.6.6
Release:    %mkrel 5
Group:      System/Libraries
License:    GPLv2+
URL:        http://wiki.drobilla.net/SLV2
Source0:    http://download.drobilla.net/%{name}-%{version}.tar.bz2
Patch0:        slv2-0.6.6-ladspa2lv2_fix.diff
BuildRequires:  doxygen
BuildRequires:  libjack-devel
BuildRequires:  liblrdf-devel
BuildRequires:  libtool
BuildRequires:  lv2core-devel >= 3.0
BuildRequires:  pkgconfig
BuildRequires:  raptor-devel
BuildRequires:  rasqal-devel
BuildRequires:  redland-devel >= 1.0.6
BuildRequires:  libjack-devel >= 0.107.0
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
Requires:   lv2core-devel >= 3.0

%description -n %{develname}
Files required for compiling programs which use SLV2, and developer
documentation.

%prep

%setup -q -n %{name}-%version
%patch0 -p0

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

install -d %{buildroot}%{_libdir}/lv2

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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
%dir %{_libdir}/lv2/
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
