Name: test
Version: 0.0.1
Release: 1%{?dist}

Summary: template for test project example 
License: GPLv3
Group: Development/Libraries
Url: https://github.com/cnangel/build-rpm-action
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
Vendor: Cnangel <cnangel@gmail.com>
Packager: Cnangel <cnangel@gmail.com>
BuildRequires: cppunit-devel 
BuildRequires: gtest-devel 

%description
%{name} is a template for automake.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%check
if [ $(grep -c test Makefile) -gt 0 ]
then
	make test
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}

%changelog
* Sat Sep 02 2023 Cnangel <cnangel@gmail.com> 1.0.0-1
- create the first spec file.

# -fin-
