Summary: Analysis plugins for use with setroubleshoot
Name: setroubleshoot-plugins
Version: 1.10.2
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
* Thu Sep  6 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.2-1
	- Change priority on use_nfs_home_dir to 55

* Thu Aug 23 2007 John Dennis <jdennis@redhat.com> - 1.10.1-1
	- add BuildRequires perl-XML-Parser

* Fri Jul 20 2007 John Dennis <jdennis@redhat.com> - 1.10.0-1
        - move all plugins and their translations from setroubleshoot-server
          package to this new independent package to allow easier updating
          of just the plugins

