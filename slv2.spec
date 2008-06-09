%define	snap r1162

%define	major 9
%define libname	%mklibname %{name} _%{major}
%define develname %mklibname -d %{name}

Summary:	A library for simple use of LV2 plugins
Name:		slv2
Version:	0.6.0
Release:	%mkrel 0.%{snap}.1
Group:		System/Libraries
License:	GPL
URL:		http://wiki.drobilla.net/SLV2
Source0:	%{name}-%{version}-%{snap}.tar.gz
Source1:	ac_python_devel.m4
Source2:	lv2_uri_map.h
Source3:	lv2_event.h
Source4:	lv2_event_helpers.h
BuildRequires:	autoconf
BuildRequires:	doxygen
BuildRequires:	libjack-devel
BuildRequires:	liblrdf-devel
BuildRequires:	libtool
BuildRequires:	lv2core-devel
BuildRequires:	pkgconfig
BuildRequires:	raptor-devel
BuildRequires:	rasqal-devel
BuildRequires:	redland-devel >= 1.0.6
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SLV2 is a library geared towards music and audio applications which makes the
use of LV2 plugins <http://lv2plug.in> as simple as possible.

This binary package contains various binaries:

 o lv2_inspect - Display information about an LV2 plugin.
 o lv2_jack_host - SLV2 Jack Host.
 o lv2_list - List system installed LV2 plugins.
 o lv2_simple_jack_host - SLV2 Simple Jack Host Example.

%package -n	%{libname}
Summary:	A library for simple use of LV2 plugins
Group:          System/Libraries

%description -n	%{libname}
SLV2 is a library geared towards music and audio applications which makes the
use of LV2 plugins <http://lv2plug.in> as simple as possible.

%package -n	%{develname}
Summary:	Development files (headers) for SLV2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n	%{develname}
Files required for compiling programs which use SLV2, and developer
documentation.

%prep

%setup -q -n %{name}

rm -rf m4
mkdir -p m4
cp %{SOURCE1} m4/

rm -f hosts/lv2_uri_map.h
rm -f hosts/lv2_event.h
rm -f hosts/lv2_event_helpers.h

cp %{SOURCE2} hosts/
cp %{SOURCE3} hosts/
cp %{SOURCE4} hosts/


%build
sh ./autogen.sh

%configure2_5x \
    --disable-bindings \
    --enable-jack

make

%install
rm -rf %{buildroot}

%makeinstall_std

install -m0755 utils/ladspa2lv2 %{buildroot}%{_bindir}/

install -d %{buildroot}%{_libdir}/lv2
install -m0644 slv2.ttl %{buildroot}%{_libdir}/lv2/

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

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/*.so.*
%{_libdir}/lv2/slv2.ttl

%files -n %{develname}
%defattr(-,root,root)
%doc doc/html/*
%{_includedir}/slv2/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/slv2.pc
%{_mandir}/man3/*

