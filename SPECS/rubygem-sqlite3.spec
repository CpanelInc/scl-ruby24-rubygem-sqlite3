%define debug_package %{nil}

# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby24
%global gem_name sqlite3

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%{?scl:%scl_package rubygem-%{gem_name}}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 2

Summary:        Allows Ruby scripts to interface with a SQLite3 database
Name:           %{?scl_prefix}rubygem-%{gem_name}
Version:        1.4.2
Release:        %{release_prefix}%{?dist}.cpanel
Group:          Development/Languages
License:        BSD
URL:            https://github.com/sparklemotion/sqlite3-ruby
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:       %{?scl_prefix}ruby(rubygems)
Requires:       %{?scl_prefix}ruby(release)

BuildRequires:  sqlite-devel
BuildRequires:  scl-utils
BuildRequires:  scl-utils-build
BuildRequires:  %{?scl_prefix}ruby
BuildRequires:  %{?scl_prefix}rubygems-devel
BuildRequires:  %{?scl_prefix}ruby-devel
BuildRequires:  %{?scl_prefix}rubygem(rake)
BuildRequires:  %{?scl_prefix}rubygem(minitest) >= 5.0.0
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
# setup.rb shipped in the -doc subpackage has LGPLv2.1 licensing
License: BSD and LGPLv2
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T

%{?scl:scl enable %{scl} - << \EOF}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%gem_install -n %{SOURCE0}
%{?scl:EOF}

# Permission
find . -name \*.rb -or -name \*.gem | xargs chmod 0644

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
mkdir -p %{buildroot}%{gem_extdir_mri}/sqlite3
mv %{buildroot}%{gem_instdir}/ext/sqlite3/sqlite3_native.so %{buildroot}%{gem_extdir_mri}/sqlite3
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/

%check
# Tests fail on cent 6
%if 0%{rhel} > 6
%{?scl:scl enable %{scl} - << \EOF}
pushd .%{gem_instdir}
ruby -I$(dirs +1)%{gem_extdir_mri}:lib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd
%{?scl:EOF}
%endif

%files
%{gem_extdir_mri}
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/appveyor.yml
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/ext
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/API_CHANGES.rdoc
%doc %{gem_instdir}/CHANGELOG.rdoc
%doc %{gem_instdir}/ChangeLog.cvs
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/setup.rb
%doc %{gem_docdir}
%doc %{gem_instdir}/faq/
%{gem_instdir}/rakelib/
%{gem_instdir}/test/

%changelog
* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 1.4.2-2
- ZC-9589: Update DISABLE_BUILD to match OBS

* Wed Jan 22 2020 Cory McIntire <cory@cpanel.net> - 1.4.2-1
- EA-8847: Update scl-ruby24-rubygem-sqlite3 from v1.3.13 to v1.4.2

* Mon Apr 17 2017 Rishwanth Yeddula <rish@cpanel.net> 2.0.1-1
- initial packaging
