#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	CD paranoia CD-DA libraries from libcdio
Summary(pl.UTF-8):	Biblioteki paranoia CD-DA z libcdio
Name:		libcdio-paranoia
%define	paranoia_ver	10.2
%define	libcdio_ver	2.0.1
%undefine	subver
Version:	%{libcdio_ver}_%{paranoia_ver}%{?subver:_%{subver}}
Release:	2
License:	GPL v3+
Group:		Libraries
%if 0%{?subver:1}
Source0:	https://ftp.gnu.org/gnu/libcdio/%{name}-%{paranoia_ver}+%{libcdio_ver}+%{subver}.tar.bz2
%else
Source0:	https://ftp.gnu.org/gnu/libcdio/%{name}-%{paranoia_ver}+%{libcdio_ver}.tar.bz2
# Source0-md5:	98332ca7b2a4fcabf5dec8a57cc98fe9
%endif
Patch0:		%{name}-am.patch
URL:		http://www.gnu.org/software/libcdio/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.8.3
BuildRequires:	help2man
BuildRequires:	libcdio-devel >= 0.90
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	libcdio >= 0.90
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from
the CDROM directly as data, with no analog step between, and writes
the data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

%description -l pl.UTF-8
Ta biblioteka odczytu CDDA (libcdio-cdparanoia) odczytuje dźwięk z
płyt CD bezpośrednio jako dane, bez pośrednictwa sygnału analogowego i
zapisuje te dane do pliku lub strumienia jako .wav, .aifc lub dane
surowe 16-bitowe PCM.

%package devel
Summary:	Header files for libcdio-paranoia libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek libcdio-paranoia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libcdio-devel >= 0.90

%description devel
Header files for libcdio-paranoia libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libcdio-paranoia.

%package static
Summary:	Static libcdio-paranoia libraries
Summary(pl.UTF-8):	Statyczne biblioteki libcdio-paranoia
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcdio-paranoia libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libcdio-paranoia.

%package utils
Summary:	libcdio-paranoia utility: cd-paranoia
Summary(pl.UTF-8):	Narzędzie używające libcdio-paranoia: cd-paranoia
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description utils
libcdio-paranoia utility: cd-paranoia.

%description utils -l pl.UTF-8
Narzędzie używające libcdio-paranoia: cd-paranoia.

%prep
%setup -q -n %{name}-%{paranoia_ver}+%{libcdio_ver}%{?subver:+%{subver}}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-maintainer-mode \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mansubdir=/ja/man1

# compatibility with pre-0.90 libcdio
ln -s paranoia/cdda.h $RPM_BUILD_ROOT%{_includedir}/cdio/cdda.h
ln -s paranoia/paranoia.h $RPM_BUILD_ROOT%{_includedir}/cdio/paranoia.h

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS.md README.md THANKS doc/overlapdef.txt
%attr(755,root,root) %{_libdir}/libcdio_cdda.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcdio_cdda.so.2
%attr(755,root,root) %{_libdir}/libcdio_paranoia.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcdio_paranoia.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio_cdda.so
%attr(755,root,root) %{_libdir}/libcdio_paranoia.so
%{_includedir}/cdio/cdda.h
%{_includedir}/cdio/paranoia.h
%{_includedir}/cdio/paranoia
%{_pkgconfigdir}/libcdio_cdda.pc
%{_pkgconfigdir}/libcdio_paranoia.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcdio_cdda.a
%{_libdir}/libcdio_paranoia.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cd-paranoia
%{_mandir}/man1/cd-paranoia.1*
%lang(ja) %{_mandir}/ja/man1/cd-paranoia.1*
