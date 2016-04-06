#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	doc	# don't build doc

Summary:	A sleek and powerful Git GUI
Name:		git-cola
Version:	2.5
Release:	1
License:	GPL v2+
Group:		Development/Tools
Source0:	https://github.com/git-cola/git-cola/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	39ffee2dd5d42f0dd9574af1ee8516b2
Patch0:		disable-live-tests.patch
URL:		http://git-cola.github.io/
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
BuildRequires:	git-core >= 1.5.2
BuildRequires:	python-PyQt4
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python-nose
%endif
%if %{with doc}
BuildRequires:	rsync
BuildRequires:	sphinx-pdg-2
%endif
Requires:	desktop-file-utils
Requires:	git-core >= 1.5.2
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	python-PyQt4 >= 4.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
git-cola is a powerful Git GUI with a slick and intuitive user
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
%patch0 -p1

# fix #!/usr/bin/env python -> #!/usr/bin/python:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' bin/git-* cola/widgets/*.py extras/*/*.py share/git-cola/bin/git*

# requires X for test
rm test/qtutils_test.py

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%{__make}
%{?with_tests:%{__make} test NOSETESTS=nosetests-%{py_ver}}
%{?with_doc:%{__make} doc SPHINXBUILD=sphinx-build-2}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 %{?with_doc:install-doc install-html} \
	prefix=%{_prefix} \
	SPHINXBUILD=sphinx-build-2 \
	DESTDIR=$RPM_BUILD_ROOT \

%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_postclean %{_datadir}/%{name}

# doc sources
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/*.rst
# packaged manually
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/*.html

mv $RPM_BUILD_ROOT%{_localedir}/{id_ID,id}
mv $RPM_BUILD_ROOT%{_localedir}/{tr_TR,tr}
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
