# vim: syntax=spec

%global libdir %{_prefix}/lib

Name: rpkg-macros
Version: 2.0
Release: 1
Summary: Set of preproc macros for rpkg utility
License: GPLv2+
URL: https://pagure.io/rpkg-util.git

# Source is created by:
# git clone https://pagure.io/rpkg-util.git
# cd rpkg-util/macros
# git checkout rpkg-macros-2.0-1
# ./rpkg spec --sources
Source0: rpkg-util-macros-28034317.tar.gz
Patch1: allow_protocol_file.patch

BuildArch: noarch

BuildRequires: bash
BuildRequires: preproc
BuildRequires: git
BuildRequires: coreutils
BuildRequires: findutils
BuildRequires: rpm-git-tag-sort

Requires: bash
Requires: git
Requires: coreutils
Requires: findutils
Requires: rpm-git-tag-sort

%description
Set of preproc macros to be used by rpkg utility. They
are designed to dynamically generate certain parts
of rpm spec files. You can use those macros also without
rpkg by:

   $ cat <file_with_the_macros> | preproc -s /usr/lib/rpkg.macros.d/all.bash -e INPUT_PATH=<file_with_the_macros>

INPUT_PATH env variable is passed to preproc to inform
macros about the input file location. The variable is used
to derive INPUT_DIR_PATH variable which rpkg macros use.

If neither INPUT_PATH nor INPUT_DIR_PATH are specified,
INPUT_PATH will stay empty and INPUT_DIR_PATH will default
to '.' (the current working directory).

Another option to experiment with the macros is to source
/usr/lib/rpkg.macros.d/all.bash into your bash environment
Then you can directly invoke the macros on your command-line
as bash functions. See content in /usr/lib/rpkg.macros.d to
discover available macros.

Please, see man rpkg-macros for more information.

%prep
%setup -T -b 0 -q -n rpkg-util-macros
%autopatch -p1

%check
git config --global protocol.file.allow always
PATH=bin/:$PATH tests/run

%install
install -d %{buildroot}%{libdir}
install -d %{buildroot}%{libdir}/rpkg.macros.d
cp -ar macros.d/* %{buildroot}%{libdir}/rpkg.macros.d

install -d %{buildroot}%{_bindir}
install -p -m 755 bin/pack_sources %{buildroot}%{_bindir}/pack_sources

install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man/rpkg-macros.1 %{buildroot}/%{_mandir}/man1/

%files
%{!?_licensedir:%global license %doc}
%license LICENSE
%{libdir}/rpkg.macros.d
%{_bindir}/pack_sources
%{_mandir}/man1/rpkg-macros.1*

%changelog
* Mon May 22 2023 lichaoran <pkwarcraft@hotmail.com> - 2.0-1
- Init package
