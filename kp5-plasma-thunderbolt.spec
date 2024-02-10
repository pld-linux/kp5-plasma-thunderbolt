#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.93.0
%define		qtver		5.15.2
%define		kpname		plasma-thunderbolt
%define		kf6ver		5.39.0

Summary:	plasma-nm
Name:		kp5-%{kpname}
Version:	5.93.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	a9407fcfeb522bfc273491ca0249ff23
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.0
BuildRequires:	Qt6DBus-devel >= 5.15.0
BuildRequires:	Qt6Gui-devel >= 5.15.0
BuildRequires:	Qt6Network-devel >= 5.15.2
BuildRequires:	Qt6Qml-devel >= 5.15.2
BuildRequires:	Qt6Quick-devel >= 5.15.0
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.70
BuildRequires:	kf6-kauth-devel >= 5.85.0
BuildRequires:	kf6-kcmutils-devel >= 5.70
BuildRequires:	kf6-kcodecs-devel >= 5.85.0
BuildRequires:	kf6-kconfig-devel >= 5.85.0
BuildRequires:	kf6-kcoreaddons-devel >= 5.85.0
BuildRequires:	kf6-kdbusaddons-devel >= 5.70
BuildRequires:	kf6-kdeclarative-devel >= 5.70
BuildRequires:	kf6-ki18n-devel >= 5.70
BuildRequires:	kf6-knotifications-devel >= 5.70
BuildRequires:	kf6-kpackage-devel >= 5.85.0
BuildRequires:	kf6-kservice-devel >= 5.85.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
This repository contains a Plasma Sytem Settings module and a KDED
module to handle authorization of Thunderbolt devices connected to the
computer. There's also a shared library (libkbolt) that implements
common interface between the modules and the system-wide bolt daemon,
which does the actual hard work of talking to the kernel.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkbolt.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/kded_bolt.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_bolt.so
%{_desktopdir}/kcm_bolt.desktop
%{_datadir}/knotifications6/kded_bolt.notifyrc
