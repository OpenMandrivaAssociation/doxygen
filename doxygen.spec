%undefine _debugsource_files

%bcond_with doc

# Disabled temporarily because of
# https://bugs.llvm.org/show_bug.cgi?id=47117
# https://github.com/doxygen/doxygen/issues/7956
%bcond_without libclang

Summary:	Documentation system for C/C++
Name:		doxygen
Version:	1.16.1
Release:	1
Group:		Development/Other
License:	GPLv2
Url:		https://doxygen.nl
Source0:	http://doxygen.nl/files/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch
Patch1:		doxygen-1.8.19-linkage.patch
Patch2:		doxygen-1.14.0-clang-21.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	git
BuildRequires:	pkgconfig(libpng)
BuildRequires:	cmake
BuildRequires:	pkgconfig(spdlog)
BuildRequires:	pkgconfig(fmt)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libzstd)
%if %{with libclang}
BuildRequires:	cmake(LLVM)
BuildRequires:	pkgconfig(z3)
# For lit-cpuid, referenced by LLVMExports.cmake
BuildRequires:	lldb
# For llvm-mt, referenced by LLVMExports.cmake
BuildRequires:	lld
BuildRequires:	clang-devel
BuildRequires:	clang-analyzer
BuildRequires:	cmake(MLIR)
BuildRequires:	llvm-static-devel
BuildRequires:	spirv-llvm-translator
BuildRequires:	llvm-bolt
BuildRequires:	llvm-polly
BuildRequires:	llvm-polly-devel
# For llvm-mlir-tools, referenced by LLVMExports.cmake
BuildRequires:	llvm-mlir-tools
BuildRequires:	%{_lib}gpuruntime
%endif
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Xml)
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

%package doxywizard
Summary:	A GUI for creating and editing configuration files
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 1.5.7.1

%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.

%prep
export LC_ALL=C.UTF-8
%autosetup -p1

%build
# Just because we use clang doesn't mean we also want to use libc++ (yet)
# Especially with libraries used by doxygen (Qt, clang) built against
# libstdc++, that's asking for trouble
%cmake	\
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_STATIC_LIBS:BOOL=ON \
	-Duse_libc++:BOOL=OFF \
%if %{with libclang}
	-Duse_libclang=ON \
%else
	-Duse_libclang=OFF \
%endif
	-Duse_sys_spdlog=ON \
	-Duse_sys_fmt=ON \
	-Duse_sys_sqlite3=ON \
	-Dforce_qt=Qt6 \
%if %{with doc}
	-Dbuild_doc=ON \
%endif
	-Dbuild_wizard=ON

%make_build LFLAGS="%{?build_ldflags}" all

%if %{with doc}
%make_build docs
%endif

%install
%make_install -C build

%if !%{with doc}
install -m644 doc/doxygen.1 -D %{buildroot}%{_mandir}/man1/doxygen.1
install -m644 doc/doxywizard.1 -D %{buildroot}%{_mandir}/man1/doxywizard.1
%endif

# FIXME workaround for gdb 8.3.1 hang
strip --strip-unneeded %{buildroot}%{_bindir}/doxygen

%files
%if %with doc
%doc html examples pdf
%endif
%{_bindir}/doxygen
%doc %{_mandir}/man1/doxygen.1*

%files doxywizard
%{_bindir}/doxywizard
%doc %{_mandir}/man1/doxywizard.1*
