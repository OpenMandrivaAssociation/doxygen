%define builddoc 1
%{?_without_doc: %{expand: %%global builddoc 0}}

Name:		doxygen
Version:	1.5.5
Release:	%mkrel 1
Summary:	Doxygen is THE documentation system for C/C++
Group:		Development/Other
License:	GPL
URL:		http://www.stack.nl/~dimitri/doxygen/
Source0:	ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.bz2
Patch0:		doxygen-1.2.12-fix-latex.patch
Patch1:		doxygen-1.5.2-syspng.patch
BuildRequires:	X11-devel
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:  png-devel
BuildRequires:  qt3-devel

%if %builddoc
BuildRequires:	tetex-latex
BuildRequires:	ghostscript python
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Epoch:		1

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .syspng
%{__perl} -pi -e "s|^TMAKE_CFLAGS_RELEASE.*|TMAKE_CFLAGS_RELEASE = %{optflags}|" tmake/lib/linux-g++/tmake.conf
%{__perl} -pi -e "s|/lib$|/%{_lib}|" tmake/lib/linux-g++/tmake.conf
# always use threaded version of qt
%{__perl} -pi -e 's/^f_thread=NO/f_thread=YES/' configure
# XXX configure is going to fail if both 32-bit and 64-bit qt3-devel
# are installed
find -type d -exec %{__chmod} 0755 {} \;
# build with system libpng
%{__rm} -rf libpng

%build
./configure --with-doxywizard

%make
%if %builddoc
%{__make} docs
%{__mv} doc/float.sty latex
%{__mv} doc/fancyhdr.sty latex
%{__make} pdf
mkdir pdf
%{__mv} latex/doxygen_manual.pdf pdf
%endif

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -s bin/doxy* %{buildroot}%{_bindir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%if %builddoc
%doc html examples pdf
%endif
%doc README
%{_bindir}/doxygen
%{_bindir}/doxytag
%{_bindir}/doxywizard
