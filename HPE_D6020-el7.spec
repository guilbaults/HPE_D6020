Name:	  HPE_D6020
Version:  0.0.2
%global gittag 0.0.2
Release:  1%{?dist}
Summary:  Script to identify slots in a HPE D6020 JBOD

License:  Apache License 2.0
URL:      https://github.com/guilbaults/HPE_D6020
Source0:  https://github.com/guilbaults/%{name}/archive/v%{gittag}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
This script is used to identify slots in a HPE D6020 JBOD

%prep
%autosetup -n %{name}-%{gittag}
%setup -q

%build

%install
mkdir -p %{buildroot}/opt/HPE_D6020

install -m 0755 HPE_D6020.py %{buildroot}/opt/HPE_D6020/HPE_D6020.py
install -m 0755 HPE_D6020_cli.py %{buildroot}/opt/HPE_D6020/HPE_D6020_cli.py
install -m 0755 __init__.py %{buildroot}/opt/HPE_D6020/__init__.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
/opt/HPE_D6020/HPE_D6020.py
/opt/HPE_D6020/HPE_D6020_cli.py
/opt/HPE_D6020/__init__.py

%exclude /opt/HPE_D6020/*.pyc
%exclude /opt/HPE_D6020/*.pyo

%changelog
* Wed Jul 3 2019 Simon Guilbault <simon.guilbault@calculquebec.ca> 0.0.2-1
- Support for missing disks
* Tue Jul 2 2019 Simon Guilbault <simon.guilbault@calculquebec.ca> 0.0.1-1
- Initial release

