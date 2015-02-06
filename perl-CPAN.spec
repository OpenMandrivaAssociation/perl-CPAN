%define upstream_name	CPAN
%define upstream_version 2.05

%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Mac::BuildTools\\)'
%endif

Name:		perl-%{upstream_name}
Version:	%perl_convert_version %{upstream_version}
Release:	3
Epoch:		1

Summary:	%{upstream_name} module for perl

License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{upstream_name}/
Source0:	http://search.cpan.org/%{upstream_name}/authors/id/A/AN/ANDK/%{upstream_name}-%{upstream_version}.tar.gz

BuildRequires:	perl-devel
BuildRequires:	perl(Digest::SHA)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(YAML)
BuildRequires:	perl(YAML::Syck)

BuildArch:	noarch

%description
The CPAN module automates or at least simplifies the make and install of
perl modules and extensions. It includes some primitive searching
capabilities and knows how to use Net::FTP or LWP or some external
download clients to fetch the distributions from the net.

These are fetched from one or more of the mirrored CPAN (Comprehensive
Perl Archive Network) sites and unpacked in a dedicated directory.

The CPAN module also supports the concept of named and versioned
*bundles* of modules. Bundles simplify the handling of sets of related
modules. See Bundles below.

The package contains a session manager and a cache manager. The session
manager keeps track of what has been fetched, built and installed in the
current session. The cache manager keeps track of the disk space
occupied by the make processes and deletes excess space according to a
simple FIFO mechanism.

All methods provided are accessible in a programmer style and in an
interactive shell style.

%prep
%setup -q -n %{upstream_name}-%{upstream_version}

%build
perl Makefile.PL INSTALLDIRS=vendor
%make

%check
# Signature file does not contain debug files signatures, just ignore the file for tests
mv SIGNATURE SIGNATURE_test
# perl(CPAN::Test::Dummy::Perl5::Make::CircDepeOne/Two/Three) issue a warning if not present
# so we just ignore them (they induce a failure if tested)
%make test
mv SIGNATURE_test SIGNATURE

%install
%makeinstall_std
# Temporarily rename the cpan shell in order to wait for perl-5.10
mv %{buildroot}/%{_bindir}/cpan %{buildroot}/%{_bindir}/cpan-%{upstream_version}
mv %{buildroot}/%{_mandir}/man1/cpan.1 %{buildroot}/%{_mandir}/man1/cpan-%{upstream_version}.1

%files
%doc Changes README
%{_bindir}/*
%{perl_vendorlib}
%{_mandir}/*/*



