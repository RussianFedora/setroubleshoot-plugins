Summary: Analysis plugins for use with setroubleshoot
Name: setroubleshoot-plugins
Version: 2.0.1
Release: 1%{?dist}
License: GPLv2+
Group: Applications/System
URL: https://hosted.fedoraproject.org/projects/setroubleshoot
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: perl-XML-Parser
BuildRequires: intltool gettext python
Requires: dbus
Requires: setroubleshoot >= 2.0.0

%define pkgdocdir %{_datadir}/doc/%{name}-%{version}

%description
This package provides a set of analysis plugins for use with
setroubleshoot. Each plugin has the capacity to analyze SELinux AVC
data and system data to provide user friendly reports describing how
to interpret SELinux AVC denials.

%prep
%setup -q

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

