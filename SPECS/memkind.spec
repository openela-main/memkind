%global gittag0 v1.10.1

Name: memkind
Summary: User Extensible Heap Manager
Version: 1.10.1
Release: 1%{?checkout}%{?dist}
License: BSD
Group: System Environment/Libraries
URL: http://memkind.github.io/memkind
BuildRequires: automake libtool numactl-devel systemd gcc gcc-c++ daxctl-devel

# x86_64 is the only arch memkind will build and work due to
# its current dependency on SSE4.2 CRC32 instruction which
# is used to compute thread local storage arena mappings
# with polynomial accumulations via GCC's intrinsic _mm_crc32_u64
# For further info check: 
# - /lib/gcc/<target>/<version>/include/smmintrin.h
# - https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36095 
# - http://en.wikipedia.org/wiki/SSE4
ExclusiveArch: x86_64

# Source0 creation:
# (1) "git archive git archive --prefix=%%{name}-%%{version}/ --format=tar [githash] | \
#				gzip > [srcdir]/%%{name}-%%{version}-g%%{githash}.tar.gz"; or
# (2) wget https://github.com/%%{name}/%%{name}/archive/%%{gittag0}/%%{name}-%%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

# void nonsensical CFLAGS override done by autotools which invalidates
# the strong stack protection setup
Patch0: configure.ac.patch

%description
The memkind library is an user extensible heap manager built on top of
jemalloc which enables control of memory characteristics and a
partitioning of the heap between kinds of memory.  The kinds of memory
are defined by operating system memory policies that have been applied
to virtual address ranges. Memory characteristics supported by
memkind without user extension include control of NUMA and page size
features. The jemalloc non-standard interface has been extended to
enable specialized arenas to make requests for virtual memory from the
operating system through the memkind partition interface. Through the
other memkind interfaces the user can control and extend memory
partition features and allocate memory while selecting enabled
features. This software is being made available for early evaluation.
Feedback on design or implementation is greatly appreciated.

%package devel
Summary: Memkind User Extensible Heap Manager development lib and tools
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Install header files and development aids to link memkind library 
into applications. The memkind library is an user extensible heap manager 
built on top of jemalloc which enables control of memory characteristics and
heap partitioning on different kinds of memory. This software is being made 
available for early evaluation. The memkind library should be considered 
pre-alpha: bugs may exist and the interfaces may be subject to change prior to 
alpha release. Feedback on design or implementation is greatly appreciated.

%prep
%setup -q -a 0 -n %{name}-%{version}
%patch0 -p1

%build
%set_build_flags

# It is required that we configure and build the jemalloc subdirectory
# before we configure and start building the top level memkind directory.
# To ensure the memkind build step is able to discover the output
# of the jemalloc build we must create an 'obj' directory, and build
# from within that directory.
cd %{_builddir}/%{name}-%{version}
echo %{version} > %{_builddir}/%{name}-%{version}/VERSION
./build.sh --prefix=%{_prefix} --includedir=%{_includedir} --libdir=%{_libdir} \
           --bindir=%{_bindir} --docdir=%{_docdir}/%{name} --mandir=%{_mandir} \
           --sbindir=%{_sbindir}

%install
cd %{_builddir}/%{name}-%{version}
make DESTDIR=%{buildroot} INSTALL='install -p' install
rm -f %{buildroot}/%{_libdir}/lib%{name}.{l,}a
rm -f %{buildroot}/%{_libdir}/libautohbw.{l,}a
rm -f %{buildroot}/%{_docdir}/%{name}/VERSION

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/lib%{name}.so.*
%{_libdir}/libautohbw.so.*
%{_bindir}/%{name}-hbw-nodes
%{_bindir}/%{name}-auto-dax-kmem-nodes
%{_mandir}/man1/%{name}*.1.*
%{_mandir}/man7/autohbw.7.*
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%license %{_docdir}/%{name}/COPYING

%files devel
%{_includedir}/%{name}*.h
%{_includedir}/hbwmalloc.h
%{_includedir}/hbw_allocator.h
%{_includedir}/pmem_allocator.h
%{_libdir}/lib%{name}.so
%{_libdir}/libautohbw.so
%{_libdir}/pkgconfig/memkind.pc
%{_mandir}/man3/%{name}*.3.*
%{_mandir}/man3/hbwmalloc.3.*
%{_mandir}/man3/hbwallocator.3.*
%{_mandir}/man3/pmemallocator.3.*

%changelog
* Mon Dec 14 2020 Rafael Aquini <aquini@redhat.com> - 1.10.1-1
- Update memkind source file to 1.10.1 upstream (1841966)

* Tue Apr 14 2020 Rafael Aquini <aquini@redhat.com> - 1.10.0-10
- Fix: add Tier1 tests for CI gating (1688933)

* Sun Apr 12 2020 Rafael Aquini <aquini@redhat.com> - 1.10.0-1
- Update to memkind source file to 1.10.0 upstream (1780394)
- add Tier1 tests for CI gating (1688933)

* Wed Oct 23 2019 Rafael Aquini <aquini@redhat.com> - 1.9.0-1
- Update to memkind source file to 1.9.0 upstream (1660589)

* Tue Apr  2 2019 Rafael Aquini <aquini@redhat.com> - 1.7.0-6
- Fix: Fix: Adding CI gating basic infrastructure (1680614)

* Tue Apr  2 2019 Rafael Aquini <aquini@redhat.com> - 1.7.0-5
- Fix: Adding CI gating basic infrastructure (1680614)

* Tue Mar 12 2019 Rafael Aquini <aquini@redhat.com> - 1.7.0-4
- Adding CI gating basic infrastructure (1680614)

* Mon Oct  8 2018 Rafael Aquini <aquini@redhat.com> - 1.7.0-3
- Update to upstream 76495a7 to pick up assorted fixes (1631144)

* Tue Oct  2 2018 Rafael Aquini <aquini@redhat.com> - 1.7.0-2
- Fix up annocheck distro flag failures (1630595)

* Fri Mar 23 2018 Rafael Aquini <aquini@linux.com> - 1.7.0-1
- Update memkind source file to 1.7.0 upstream

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Rafael Aquini <aquini@linux.com> - 1.5.0-1
- Update memkind source file to 1.5.0 upstream

* Fri Feb 17 2017 Rafael Aquini <aquini@linux.com> - 1.4.0-1
- Update memkind source file to 1.4.0 upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 16 2016 Rafael Aquini <aquini@linux.com> - 1.3.0-1
- Update memkind source file to 1.3.0 upstream

* Wed Jun 08 2016 Rafael Aquini <aquini@linux.com> - 1.1.0-1
- Update memkind source file to 1.1.0 upstream

* Thu Mar 17 2016 Rafael Aquini <aquini@linux.com> - 1.0.0-1
- Update memkind source file to 1.0.0 upstream

* Sun Feb 07 2016 Rafael Aquini <aquini@linux.com> - 0.3.0-5
- Fix rpmlint error dir-or-file-in-var-run for /var/run/memkind

* Sat Feb 06 2016 Rafael Aquini <aquini@linux.com> - 0.3.0-4
- Update upstream fixes for memkind-0.3.0
- Switch old init.d scripts for systemd unit service
- Fix fc24 build error

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Rafael Aquini <aquini@linux.com> - 0.3.0-2
- Minor clean-ups and adjustments required for the RPM

* Tue Nov 17 2015 Rafael Aquini <aquini@linux.com> - 0.3.0-1
- Update memkind source file to 0.3.0 upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4.20150525git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Rafael Aquini <aquini@linux.com> - 0.2.2-3.20150525git
- Get rid of obsolete m4 macros usage on autotool scripts

* Mon May 18 2015 Rafael Aquini <aquini@linux.com> - 0.2.2-2.20150525git
- Fix to BuildRequires and License Text Marker in spec file (1222709#c1)

* Mon May 18 2015 Rafael Aquini <aquini@linux.com> - 0.2.2-1.20150518git
- Initial RPM packaging for Fedora
