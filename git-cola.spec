#
# Conditional build:
%bcond_without	doc	# don't build doc

Summary:	A sleek and powerful git GUI
Name:		git-cola
Version:	2.3
Release:	1
License:	GPL v2+
Source0:	https://github.com/git-cola/git-cola/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0f3c5355eda07e752d1f8f536882a2d0
Group:		Development/Tools
URL:		http://git-cola.github.io/
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	git-core >= 1.5.2
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	sip-PyQt4 >= 4.3
%if %{with doc}
BuildRequires:	sphinx-pdg
BuildRequires:	xmlto
%endif
Requires:	git-core >= 1.5.2
Requires:	hicolor-icon-theme
Requires:	python-inotify
Requires:	sip-PyQt4 >= 4.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
git-cola is a powerful git GUI with a slick and intuitive user
interface.

%package doc
Summary:	Documentation for git-cola
Summary(pl.UTF-8):	Dokumentacja do git-cola
Group:		Documentation

%description doc
Documentation for git-cola.

%description doc -l pl.UTF-8
Dokumentacja do git-cola.

%prep
%setup -q

# fix #!/usr/bin/env python -> #!/usr/bin/python:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' bin/git-* cola/widgets/*.py extras/*/*.py share/git-cola/bin/git*

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%{__make}
%{?with_doc:%{__make} doc}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install %{?with_doc:install-doc install-html} \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT \

# doc sources
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/*.rst
# packaged manually
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/*.html

mv $RPM_BUILD_ROOT%{_localedir}/{id_ID,id}
%find_lang %{name}

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/git-cola-folder-handler.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/git-cola.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/git-dag.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc COPYING COPYRIGHT README.md
%doc share/doc/git-cola/hotkeys.html
%doc %lang(de) share/doc/git-cola/hotkeys_de.html
%doc %lang(zh_CN) share/doc/git-cola/hotkeys_zh_CN.html
%doc %lang(zh_TW) share/doc/git-cola/hotkeys_zh_TW.html
%attr(755,root,root) %{_bindir}/cola
%attr(755,root,root) %{_bindir}/git-cola
%attr(755,root,root) %{_bindir}/git-dag
%{_desktopdir}/git-cola-folder-handler.desktop
%{_desktopdir}/git-cola.desktop
%{_desktopdir}/git-dag.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{?with_doc:%{_mandir}/man1/git*.1*}

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}
%endif
