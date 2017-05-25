%bcond_with doc
%bcond_without qt5

Summary:	Documentation system for C/C++
Name:		doxygen
Epoch:		1
Version:	1.8.12
Release:	2
Group:		Development/Other
License:	GPLv2
Url:		http://www.stack.nl/~dimitri/doxygen/
Source0:	ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(libpng)
BuildRequires:	cmake
BuildRequires:	clang-devel
%if %{with qt5}
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Xml)
%endif
%if %{with doc}
BuildRequires:	ghostscript
BuildRequires:	python
BuildRequires:	tetex-latex
BuildRequires:	texlive-epstopdf
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

%if %with qt5
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

%build
%cmake	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_STATIC_LIBS:BOOL=ON \
	-Duse_libclang=ON \
%if %{with doc}
	-Dbuild_doc=ON \
%endif
%if %{with qt5}
	-Dbuild_wizard=ON
%endif

%make LFLAGS="%{?ldflags}" all

%if %{with doc}
%make docs
%endif

%install
%makeinstall_std -C build

%if !%{with doc}
install -m644 doc/doxygen.1 -D %{buildroot}%{_mandir}/man1/doxygen.1
%if %{with qt5}
install -m644 doc/doxywizard.1 -D %{buildroot}%{_mandir}/man1/doxywizard.1
%endif
%endif

%files
%if %with doc
%doc html examples pdf
%endif
%{_bindir}/doxygen
%{_mandir}/man1/doxygen.1*

%if %{with qt5}
%files doxywizard
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard.1*
%endif
