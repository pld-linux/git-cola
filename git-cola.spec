Summary:	A highly caffeinated git gui
Name:		git-cola
Version:	1.3.7.60
Release:	1
License:	GPL v2+
Group:		Development/Tools
Source0:	http://cola.tuxfamily.org/releases/cola-%{version}-src.tar.gz
# Source0-md5:	b7bd6c8a4410be84d885bf7debd49aab
Patch0:		%{name}-shebang.patch
URL:		http://cola.tuxfamily.org/
BuildRequires:	asciidoc
BuildRequires:	git-core
BuildRequires:	python-PyQt4
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xmlto
Requires:	git-core >= 1.5.2
Requires:	python >= 1:2.4
Requires:	python-PyQt4 >= 4.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A sweet, carbonated git gui known for its sugary flavour and
caffeine-inspired features.

%prep
%setup -q -n cola-%{version}
%patch0 -p0

%build
export INSTALL_GIT_DIFFTOOL=1
%{__python} setup.py build
%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 \
	--skip-build \
	--root $RPM_BUILD_ROOT \
	--prefix=%{_prefix}

%{__make} install-doc install-html \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%files
%defattr(644,root,root,755)
%doc COPYRIGHT LICENSE README
%attr(755,root,root) %{_bindir}/git-cola
%attr(755,root,root) %{_bindir}/git-difftool
%attr(755,root,root) %{_bindir}/git-difftool--helper
%{_desktopdir}/cola.desktop
%{_datadir}/git-cola
%{_docdir}/git-cola
%{_mandir}/man1/git-cola.1*
%{py_sitescriptdir}/*.egg-info
