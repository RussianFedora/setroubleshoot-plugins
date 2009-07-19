Summary: Analysis plugins for use with setroubleshoot
Name: setroubleshoot-plugins
Version: 2.0.18
Release: 2%{?dist}
License: GPLv2+
Group: Applications/System
URL: https://fedorahosted.org/setroubleshoot
Source0: %{name}-%{version}.tar.gz
Patch: setroubleshoot-plugins-2.0.18-global_ssp.patch 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: perl-XML-Parser
BuildRequires: intltool gettext python
Requires: dbus
Requires: setroubleshoot-server >= 2.0.4
%{?fc9:Requires: policycoreutils >= 2.0.35-2}

%define pkgdocdir %{_datadir}/doc/%{name}-%{version}

%description
This package provides a set of analysis plugins for use with
setroubleshoot. Each plugin has the capacity to analyze SELinux AVC
data and system data to provide user friendly reports describing how
to interpret SELinux AVC denials.

%prep
%setup -q
%patch -p1 -b .global_ssp

%build
%configure
make

%install 
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
%find_lang %{name}

%post
dbus-send --system /com/redhat/setroubleshootd com.redhat.SEtroubleshootdIface.restart string:'rpm install' >/dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ]; then
    dbus-send --system /com/redhat/setroubleshootd com.redhat.SEtroubleshootdIface.restart string:'rpm install' >/dev/null 2>&1 || :
fi

%clean 
rm -rf %{buildroot}

%files -f %{name}.lang 
%defattr(-,root,root,-)
%doc %{pkgdocdir}
%{_datadir}/setroubleshoot/plugins

%changelog
* Sun Jun 19 2009  <dwalsh@redhat.com> - 2.0.18-2
- Fix global_ssp to report correct boolean name

* Fri Jun 5 2009  <dwalsh@redhat.com> - 2.0.18-1
	- Execute catchall_boolean.py before allow_daemons_use_tty
	- Fix chcon lines to match current policy

* Mon Apr 13 2009  <dwalsh@redhat.com> - 2.0.16-1
- Change priority on restorecon plugin to happen before public_content

* Fri Apr 3 2009  <dwalsh@redhat.com> - 2.0.15-1
- Update po files

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009  <dwalsh@redhat.com> - 2.0.14-1
- Fix allow_smbd_anon_write typo
- Remove catchall_file plugin

* Wed Dec 3 2008  <dwalsh@redhat.com> - 2.0.12-1
- Fix restorecon plugin

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.11-2
- Rebuild for Python 2.6

* Wed Nov 5 2008  <dwalsh@redhat.com> - 2.0.11-1
- Fix catchall_booleans
- Fix priority on samba plugins

* Thu Oct 23 2008  <dwalsh@redhat.com> - 2.0.10-1
- Add qemu plugins for real

* Wed Oct 15 2008  <dwalsh@redhat.com> - 2.0.9-1
- Fix catchall_plugin

* Wed Sep 10 2008  <dwalsh@redhat.com> - 2.0.8-1
- Add qemu plugins

* Tue Sep 9 2008  <dwalsh@redhat.com> - 2.0.7-1
- Add catchall_booleans plugin, fix spelling

* Fri Apr  4 2008 John Dennis <jdennis@redhat.com> - 2.0.4-5
	- bump rev for build

* Mon Mar  3 2008 John Dennis <jdennis@redhat.com> - 2.0.4-4
	- Resolve bug #435644: change requires setroubleshoot to requires setroubleshoot-server

* Fri Feb 22 2008  <jdennis@redhat.com> - 2.0.4-3
	- bump rev for build

* Mon Feb 18 2008 John Dennis <jdennis@redhat.com> - 2.0.4-2
	- Fix policycoreutils dependency, should only be F-9

* Thu Jan 31 2008  <jdennis@redhat.com> - 2.0.4-1
	- Resolve bug #416351: setroubleshoot does not escape regex chars in suggested cmds
	- add new template substitution $SOURCE, a friendly name, $SOURCE_PATH still exists
	  and is the full path name of $SOURCE

* Tue Jan 15 2008  <dwalsh@redhat.com> - 2.0.2-1
	- Add catchall_boolean.py plugin

* Fri Jan 11 2008  <jdennis@redhat.com> - 2.0.1-1
	- Resolve bug #332281: remove obsolete translation
	- Resolve bug #426586: Renaming translation po file from sr@Latn to sr@latin

* Fri Dec 28 2007  <jdennis@redhat.com> - 2.0.0-1
	- prepare for v2 test release

* Tue Nov 13 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.4-1
	- Add allow_postfix_local_write_mail_spool plugin
	- Fix execute typo

* Wed Oct 10 2007 John Dennis <jdennis@redhat.com> - 1.10.3-1
	- rewrite all plugins to use new v2 audit data

* Mon Sep 24 2007 John Dennis <jdennis@redhat.com> - 1.10.3-1
	- Resolves bug #231762: Original PO strings bugs

* Thu Sep  6 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.2-1
	- Change priority on use_nfs_home_dir to 55

* Thu Aug 23 2007 John Dennis <jdennis@redhat.com> - 1.10.1-1
	- add BuildRequires perl-XML-Parser

* Fri Jul 20 2007 John Dennis <jdennis@redhat.com> - 1.10.0-1
        - move all plugins and their translations from setroubleshoot-server
          package to this new independent package to allow easier updating
          of just the plugins

