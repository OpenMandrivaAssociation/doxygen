%bcond_with doc
%bcond_without qt4

Name:		doxygen
Version:	1.5.8
Release:	%mkrel 1
Epoch:		1
Summary:	Doxygen is THE documentation system for C/C++
Group:		Development/Other
License:	GPL+
URL:		http://www.stack.nl/~dimitri/doxygen/
Source0:	ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch
Patch1:		doxygen-1.5.8-syspng.patch
Patch2:		doxygen-1.5.8-mandir.patch
Patch3:		doxygen-1.5.8-fix-str-fmt.patch
BuildRequires:  bison
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:  png-devel
%if %with qt4
BuildRequires:  qt4-devel
%endif
%if %with doc
BuildRequires:	tetex-latex
BuildRequires:	ghostscript python
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Doxygen is a documentation system for C, C++ and IDL. It can generate
an on-line class browser (in HTML) and/or an off-line reference manual
(in LaTeX) from a set of documented source files. There is also
support for generating man lpages and for converting the generated
output into Postscript, hyperlinked PDF or compressed HTML. The
documentation is extracted directly from the sources.

Doxygen can also be configured to extract the code-structure from
undocumented source files. This can be very useful to quickly find
your way in large source distributions.

%if %with qt4
%package doxywizard
Summary: A GUI for creating and editing configuration files
Group: Development/Other
Requires: %{name} = %{epoch}:%{version}
Conflicts: %{name} < 1:1.5.7.1

%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .syspng
%patch2 -p1 -b .man
%patch3 -p0 -b .str

%{__perl} -pi -e "s|^TMAKE_CFLAGS_RELEASE.*|TMAKE_CFLAGS_RELEASE = %{optflags}|" tmake/lib/linux-g++/tmake.conf
%{__perl} -pi -e "s|/lib$|/%{_lib}|" tmake/lib/linux-g++/tmake.conf
# XXX configure is going to fail if both 32-bit and 64-bit qt3-devel
# are installed
find -type d -exec %{__chmod} 0755 {} \;
# build with system libpng
%{__rm} -rf libpng

%build
unset QTDIR
./configure --prefix %_prefix \
%if %with qt4
	--with-doxywizard
%endif

%make LFLAGS="%{?ldflags}"

%if %with doc
%{__make} docs
%{__mv} doc/float.sty latex
%{__mv} doc/fancyhdr.sty latex
%{__make} pdf
mkdir pdf
%{__mv} latex/doxygen_manual.pdf pdf
%endif

%install
%{__rm} -rf %{buildroot}
make install INSTALL=%{buildroot}%{_prefix}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%if %with doc
%doc html examples pdf
%endif
%doc README
%{_bindir}/doxygen
%{_bindir}/doxytag
%{_mandir}/man1/doxygen.1*
%{_mandir}/man1/doxytag.1*

%if %with qt4
%files doxywizard
%defattr(-,root,root)
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard*
%endif
