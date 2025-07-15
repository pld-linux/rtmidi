#
# Conditional build:
%bcond_without	alsa		# build without ALSA backend
%bcond_without	jack		# build without Jack backend
#
Summary:	Common API for realtime MIDI input/output
Name:		rtmidi
Version:	3.0.0
Release:	1
License:	MIT
Group:		Applications
Source0:	http://www.music.mcgill.ca/~gary/rtmidi/release/%{name}-%{version}.tar.gz
# Source0-md5:	d22e3a5dee972fa0725c420923f1ce65
Patch0:		linking.patch
URL:		http://music.mcgill.ca/%7Egary/rtmidi/
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RtMidi is a set of C++ classes (RtMidiIn, RtMidiOut and API-specific
classes) that provides a common API (Application Programming
Interface) for realtime MIDI input/output across Linux (ALSA & JACK),
Macintosh OS X (CoreMIDI & JACK), and Windows (Multimedia Library)
operating systems. RtMidi significantly simplifies the process of
interacting with computer MIDI hardware and software. It was designed
with the following goals:

- object oriented C++ design
- simple, common API across all supported platforms
- only one header and one source file for easy inclusion in
  programming projects
- MIDI device enumeration

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%patch -P0 -p1

%build
#%%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	%{__with jack} \
	%{__with alsa}

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md doc/html
%attr(755,root,root) %{_libdir}/librtmidi.so.4.*
%ghost %{_libdir}/librtmidi.so.4

%files devel
%defattr(644,root,root,755)
%doc doc/html
%{_libdir}/librtmidi.la
%{_libdir}/librtmidi.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librtmidi.a
