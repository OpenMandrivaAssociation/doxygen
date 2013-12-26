%bcond_with doc
%bcond_without qt4

Summary:	Documentation system for C/C++
Name:		doxygen
Epoch:		1
Version:	1.8.6
Release:	1
Group:		Development/Other
License:	GPLv2
Url:		http://www.stack.nl/~dimitri/doxygen/
Source0:	ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch
Patch2:		doxygen-1.5.8-mandir.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig(libpng)
%if %with qt4
BuildRequires:	qt4-devel
%endif
%if %with doc
BuildRequires:	ghostscript
BuildRequires:	python
BuildRequires:	tetex-latex
%endif

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
Summary:	A GUI for creating and editing configuration files
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 1:1.5.7.1

%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.
%endif

%prep
%setup -q
%apply_patches

sed -i -e "s|^TMAKE_CFLAGS_RELEASE.*|TMAKE_CFLAGS_RELEASE = %{optflags}|" tmake/lib/linux-g++/tmake.conf
sed -i -e "s|/lib$|/%{_lib}|" tmake/lib/linux-g++/tmake.conf
# XXX configure is going to fail if both 32-bit and 64-bit qt3-devel
# are installed
find -type d -exec %{__chmod} 0755 {} \;
# build with system libpng
rm -rf libpng

%build
./configure \
	--prefix %{_prefix} \
	--make %{_bindir}/make \
%if %with qt4
	--with-doxywizard
%endif

%make LFLAGS="%{?ldflags}"

%if %with doc
%make docs
mv doc/float.sty latex
mv doc/fancyhdr.sty latex
%make pdf
mkdir pdf
mv latex/doxygen_manual.pdf pdf
%endif

%install
make install INSTALL=%{buildroot}%{_prefix}

%files
%if %with doc
%doc html examples pdf
%endif
%{_bindir}/doxygen
%{_mandir}/man1/doxygen.1*

%if %with qt4
%files doxywizard
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard*
%endif

