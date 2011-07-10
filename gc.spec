Summary: A garbage collector for C and C++
Name:    gc
Version: 7.1

Release: 10%{?dist}
Group:   System Environment/Libraries
License: BSD
Url:     http://www.hpl.hp.com/personal/Hans_Boehm/gc/
Source0: http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# To be more backward-compatible abi-wise, TODO: upstream ml reference
Patch1: gc-7.1-gcinit.patch
Patch3: gc-7.1-sparc.patch

## upstreamable patches
Patch50: gc-7.1-dup_cpp_headers.patch

## upstream patches
# http://www.hpl.hp.com/hosted/linux/mail-archives/gc/2008-May/002206.html
Patch100: gc-7.1-dont_add_byte.patch

BuildRequires: automake libtool
BuildRequires: libatomic_ops-devel
BuildRequires: pkgconfig

# rpmforge compatibility
Obsoletes: libgc < %{version}-%{release}
Provides:  libgc = %{version}-%{release}

%description
The Boehm-Demers-Weiser conservative garbage collector can be
used as a garbage collecting replacement for C malloc or C++ new.

%package devel
Summary: Libraries and header files for %{name} development
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Obsoletes: libgc-devel < %{version}-%{release}
Provides:  libgc-devel = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

# FIXME? -- Rex
%if 0%{?rhel} < 6 && 0%{?fedora} < 10
%patch1 -p1 -b .gcinit
%endif
%patch3 -p1 -b .sparc

%patch50 -p1 -b .dup_cpp_headers

%patch100 -p1 -b .dont_add_byte

# refresh auto*/libtool to purge rpaths
rm -f libtool libtool.m4
libtoolize --force
autoreconf -i


%build

export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

%configure \
  --disable-dependency-tracking \
  --disable-static \
  --enable-cplusplus \
  --enable-large-config \
%ifarch %{ix86}
  --enable-parallel-mark \
%endif
  --enable-threads=posix

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

install -p -D -m644 doc/gc.man	%{buildroot}%{_mandir}/man3/gc.3

## Unpackaged files
rm -rf %{buildroot}%{_datadir}/gc
rm -f  %{buildroot}%{_libdir}/lib*.la


%check
make check


%clean
rm -rf %{buildroot}


%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc doc/README
%doc doc/README.changes doc/README.contributors
%doc doc/README.environment doc/README.linux
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.html
%{_includedir}/*.h
%{_includedir}/gc/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man?/*


%changelog
* Fri Jun 18 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 7.1-10
- Add -fno-strict-aliasing to CFLAGS/CXXFLAGS (bz 605048)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 7.1-9.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org. - 7.1-8
- FTBFS gc-7.1-7.fc11 (#511365)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-6
- rebuild for pkgconfig deps

* Wed Oct 15 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-5
- forward-port patches (gcinit, sparc)

* Fri Oct 03 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-4
- BR: libatomic_ops-devel

* Mon Sep 08 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-3
- upstream DONT_ADD_BYTE_AT_END patch
- spec cosmetics

* Sat Jul 12 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-2
- --enable-large-config (#453972)

* Sun May 04 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-1
- gc-7.1
- purge rpaths

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 7.0-7
- respin (gcc43)

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-6
- BR: gawk
- fixup compat_header patch to avoid needing auto* tools

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-5
- compat_header patch (supercedes previous pkgconfig patch)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-4
- pkgconfig patch (cflags += -I%%_includedir/gc)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-3
- respin (ppc32)

* Tue Jul 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-2
- gcinit patch, ABI compatibility (#248700)

* Mon Jul 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-1
- gc-7.0

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-3
- Obsoletes/Provides: libgc(-devel) (rpmforge compatibility)

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-2
- fc6 respin

* Thu Jul 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-1
- 6.8

* Fri Mar 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.7-1
- 6.7

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-5
- gcc(4.1) patch

* Thu Dec 01 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-4
- Provides: libgc(-devel)

* Wed Sep 14 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-3
- no-undefined patch, libtool madness (#166344)

* Mon Sep 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-2
- drop opendl patch (doesn't appear to be needed anymore)

* Fri Sep 09 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-1
- 6.6

* Wed May 25 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.5-1
- 6.5

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:6.4-2
- --enable-threads unconditionally
- --enable-parallel-mark only on %%ix86 (#144681)

* Mon Jan 10 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:6.4-1
- 6.4
- update opendl patch

* Fri Jul 09 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.1
- 6.3(final)

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.4.alpha6
- dlopen patch

* Wed May 26 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.3.alpha6
- explictly --enable-threads ('n friends)

* Tue May 25 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.2.alpha6
- 6.3alpha6
- --disable-static
- --enable-parallel-mark

* Wed Dec 17 2003 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.1.alpha2
- 6.3alpha2

* Thu Oct 02 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.3
- OK, put manpage in man3.

* Thu Oct 02 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.2
- drop manpage pending feedback from developer.

* Tue Sep 30 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.1
- fix manpage location
- remove .la file (it appears unnecessary after all, thanks to opendl patch)
- remove cvs tag from description
- touchup -devel desc/summary.
- macro update to support Fedora Core

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.0
- 6.2 release.
- update license (BSD)
- Consider building with: --enable-parallel-mark
  (for now, no).
