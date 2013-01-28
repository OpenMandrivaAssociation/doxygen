%bcond_with doc
%bcond_without qt4

Name:		doxygen
Version:	1.8.3.1
Release:	1
Epoch:		1
Summary:	Doxygen is THE documentation system for C/C++
Group:		Development/Other
License:	GPL+
URL:		http://www.stack.nl/~dimitri/doxygen/
Source0:	ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch
Patch2:		doxygen-1.5.8-mandir.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:	png-devel
%if %with qt4
BuildRequires:	qt4-devel
%endif
%if %with doc
BuildRequires:	tetex-latex
BuildRequires:	ghostscript python
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
%patch2 -p1 -b .man

%{__perl} -pi -e "s|^TMAKE_CFLAGS_RELEASE.*|TMAKE_CFLAGS_RELEASE = %{optflags}|" tmake/lib/linux-g++/tmake.conf
%{__perl} -pi -e "s|/lib$|/%{_lib}|" tmake/lib/linux-g++/tmake.conf
# XXX configure is going to fail if both 32-bit and 64-bit qt3-devel
# are installed
find -type d -exec %{__chmod} 0755 {} \;
# build with system libpng
%{__rm} -rf libpng

%build
./configure \
    --prefix %{_prefix} \
    --make %{_bindir}/make \
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
make install INSTALL=%{buildroot}%{_prefix}

%files
%if %with doc
%doc html examples pdf
%endif
%doc README
%{_bindir}/doxygen
%{_mandir}/man1/doxygen.1*

%if %with qt4
%files doxywizard
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard*
%endif


%changelog
* Fri Jul 13 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:1.8.1.2-1
+ Revision: 809111
- Update to 1.8.1.2

* Sun May 20 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:1.8.1-1
+ Revision: 799738
- Update to 1.8.1

* Sun Feb 26 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:1.8.0-1
+ Revision: 780797
- Update to 1.8.0
- Remove some obsolete spec file constructs

* Sun Dec 18 2011 Andrey Bondrov <abondrov@mandriva.org> 1:1.7.6.1-1
+ Revision: 743419
- New version 1.7.6.1

* Thu Oct 06 2011 Andrey Bondrov <abondrov@mandriva.org> 1:1.7.5.1-1
+ Revision: 703326
- New version: 1.7.5.1

* Thu May 12 2011 Funda Wang <fwang@mandriva.org> 1:1.7.4-1
+ Revision: 673918
- update to new version 1.7.4

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.7.3-2
+ Revision: 663848
- mass rebuild

* Wed Jan 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.7.3-1mdv2011.0
+ Revision: 628799
- 1.7.3

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.6.3-2mdv2011.0
+ Revision: 604813
- rebuild

* Sun Feb 21 2010 Funda Wang <fwang@mandriva.org> 1:1.6.3-1mdv2010.1
+ Revision: 509120
- New version 1.6.3

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 1:1.6.2-1mdv2010.1
+ Revision: 484030
- update to new version 1.6.2

* Sun Nov 15 2009 Funda Wang <fwang@mandriva.org> 1:1.6.1-1mdv2010.1
+ Revision: 466225
- New version 1.6.1

* Fri May 01 2009 Frederik Himpe <fhimpe@mandriva.org> 1:1.5.9-1mdv2010.0
+ Revision: 369728
- update to new version 1.5.9

* Tue Jan 13 2009 Pixel <pixel@mandriva.com> 1:1.5.8-3mdv2009.1
+ Revision: 328890
- really fix format-error patch

* Mon Jan 12 2009 Pixel <pixel@mandriva.com> 1:1.5.8-2mdv2009.1
+ Revision: 328706
- fix format-error patch

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 1:1.5.8-1mdv2009.1
+ Revision: 320020
- build qt4 doxywizard
- fix qt4 dir
- fix str fmt
- do not build doc now
- New version 1.5.8

* Wed Nov 26 2008 Funda Wang <fwang@mandriva.org> 1:1.5.7.1-2mdv2009.1
+ Revision: 306904
- conflicts wit old packages
- only use pkg-config to find qt3
- use ldflags
- fix manpage dir

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.5.7.1

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Sun May 18 2008 David Walluck <walluck@mandriva.org> 1:1.5.6-1mdv2009.0
+ Revision: 208769
- BuildRequires: bison
- use %%bcond_without for doc building

  + Funda Wang <fwang@mandriva.org>
    - update to new version 1.5.6

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:1.5.5-2mdv2008.1
+ Revision: 170799
- rebuild

* Sun Feb 10 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.5.5-1mdv2008.1
+ Revision: 164911
- update to new version 1.5.5

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Sat Oct 27 2007 Funda Wang <fwang@mandriva.org> 1:1.5.4-1mdv2008.1
+ Revision: 102546
- New version 1.5.4

* Fri Jul 27 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1:1.5.3-1mdv2008.0
+ Revision: 56340
- new version

* Fri Apr 20 2007 Olivier Blin <blino@mandriva.org> 1:1.5.2-1mdv2008.0
+ Revision: 16098
- use system libpng
- remove support for obsolete distros
- 1.5.2

