%bcond_with doc
%bcond_without qt5

# Disabled temporarily because of
# https://bugs.llvm.org/show_bug.cgi?id=47117
# https://github.com/doxygen/doxygen/issues/7956
%bcond_with libclang

Summary:	Documentation system for C/C++
Name:		doxygen
Epoch:		1
Version:	1.9.1
Release:	1
Group:		Development/Other
License:	GPLv2
Url:		http://doxygen.nl
Source0:	http://doxygen.nl/files/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch
Patch1:		doxygen-1.8.19-linkage.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	git
BuildRequires:	pkgconfig(libpng)
BuildRequires:	cmake
%if %{with libclang}
BuildRequires:	cmake(LLVM)
# For lit-cpuid, referenced by LLVMExports.cmake
BuildRequires:	lldb
# For llvm-mt, referenced by LLVMExports.cmake
BuildRequires:	lld
BuildRequires:	clang-devel
BuildRequires:	clang-analyzer
# For llvm-mlir-tools, referenced by LLVMExports.cmake
BuildRequires:	llvm-mlir-tools
BuildRequires:	%{_lib}mlir_test_cblas11
BuildRequires:	%{_lib}mlir_test_cblas_interface11
BuildRequires:	%{_lib}gpuruntime
%endif
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
%autosetup -p1

%build
# Just because we use clang doesn't mean we also want to use libc++ (yet)
# Especially with libraries used by doxygen (Qt, clang) built against
# libstdc++, that's asking for trouble
%cmake	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_STATIC_LIBS:BOOL=ON \
	-Duse_libc++:BOOL=OFF \
%if %{with libclang}
	-Duse_libclang=ON \
%else
	-Duse_libclang=OFF \
%endif
%if %{with doc}
	-Dbuild_doc=ON \
%endif
%if %{with qt5}
	-Dbuild_wizard=ON
%endif

%make_build LFLAGS="%{?ldflags}" all

%if %{with doc}
%make_build docs
%endif

%install
%make_install -C build

%if !%{with doc}
install -m644 doc/doxygen.1 -D %{buildroot}%{_mandir}/man1/doxygen.1
%if %{with qt5}
install -m644 doc/doxywizard.1 -D %{buildroot}%{_mandir}/man1/doxywizard.1
%endif
%endif

# FIXME workaround for gdb 8.3.1 hang
strip --strip-unneeded %{buildroot}%{_bindir}/doxygen

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
