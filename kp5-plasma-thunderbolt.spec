%define		kdeplasmaver	5.23.0
%define		qtver		5.9.0
%define		kpname		plasma-thunderbolt
%define		kf5ver		5.39.0

Summary:	plasma-nm
Name:		kp5-%{kpname}
Version:	5.23.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	62a29bc5381087ea212a541b228b6b77
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.0
BuildRequires:	Qt5DBus-devel >= 5.15.0
BuildRequires:	Qt5Gui-devel >= 5.15.0
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Qml-devel >= 5.15.2
BuildRequires:	Qt5Quick-devel >= 5.15.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.70
BuildRequires:	kf5-kauth-devel >= 5.85.0
BuildRequires:	kf5-kcmutils-devel >= 5.70
BuildRequires:	kf5-kcodecs-devel >= 5.85.0
BuildRequires:	kf5-kconfig-devel >= 5.85.0
BuildRequires:	kf5-kcoreaddons-devel >= 5.85.0
BuildRequires:	kf5-kdbusaddons-devel >= 5.70
BuildRequires:	kf5-kdeclarative-devel >= 5.70
BuildRequires:	kf5-ki18n-devel >= 5.70
BuildRequires:	kf5-knotifications-devel >= 5.70
BuildRequires:	kf5-kpackage-devel >= 5.85.0
BuildRequires:	kf5-kservice-devel >= 5.85.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
This repository contains a Plasma Sytem Settings module and a KDED
module to handle authorization of Thunderbolt devices connected to the
computer. There's also a shared library (libkbolt) that implements
common interface between the modules and the system-wide bolt daemon,
which does the actual hard work of talking to the kernel.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	../
%ninja_build

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
%{_libdir}/libkbolt.so
%{_libdir}/qt5/plugins/kcms/kcm_bolt.so
%{_libdir}/qt5/plugins/kf5/kded/kded_bolt.so
%{_datadir}/knotifications5/kded_bolt.notifyrc
%dir %{_datadir}/kpackage/kcms/kcm_bolt
%dir %{_datadir}/kpackage/kcms/kcm_bolt/contents
%dir %{_datadir}/kpackage/kcms/kcm_bolt/contents/ui
%{_datadir}/kpackage/kcms/kcm_bolt/contents/ui/DeviceList.qml
%{_datadir}/kpackage/kcms/kcm_bolt/contents/ui/DeviceView.qml
%{_datadir}/kpackage/kcms/kcm_bolt/contents/ui/main.qml
%{_datadir}/kpackage/kcms/kcm_bolt/contents/ui/utils.js
%{_datadir}/kpackage/kcms/kcm_bolt/metadata.desktop
%{_datadir}/kpackage/kcms/kcm_bolt/metadata.json
%{_datadir}/kservices5/kcm_bolt.desktop
