%define module	CPAN
%define name	perl-%{module}
%define version 1.9205
%define release %mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{module} module for perl
License:	GPL or Artistic
Group:		Development/Perl
Source:		ftp.perl.org/pub/CPAN/modules/by-module/%{module}-%{version}.tar.bz2
Url:		http://search.cpan.org/dist/%{module}/

#BuildRequires:	perl(CPAN::Test::Dummy::Perl5::Make::CircDepeOne)
#BuildRequires:	perl(CPAN::Test::Dummy::Perl5::Make::CircDepeTwo)
#BuildRequires:	perl(CPAN::Test::Dummy::Perl5::Make::CircDepeThree)
BuildRequires:	perl(Digest::SHA)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(YAML)
BuildRequires:	perl(YAML::Syck)

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-root

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
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make}

%check
# Signature file does not contain debug files signatures, just ignore the file for tests
%{__mv} SIGNATURE SIGNATURE_test
# perl(CPAN::Test::Dummy::Perl5::Make::CircDepeOne/Two/Three) issue a warning if not present
# so we just ignore them (they induce a failure if tested)
%{__make} test
%{__mv} SIGNATURE_test SIGNATURE

%clean 
rm -rf %{buildroot}

%install
rm -rf %{buildroot}
%makeinstall_std
# Temporarily rename the cpan shell in order to wait for perl-5.10
%{__mv} %{buildroot}/%{_bindir}/cpan %{buildroot}/%{_bindir}/cpan-%{version}

%files
%defattr(-,root,root)
%{_bindir}/*
%doc Changes README
%{perl_vendorlib}
%{_mandir}/*/*

