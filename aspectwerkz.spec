%include	/usr/lib/rpm/macros.java
Summary:	AOP for Java
Summary(pl.UTF-8):	AOP dla Javy
Name:		aspectwerkz
Version:	2.0
Release:	0.1
License:	BSD-style License
Group:		Development/Languages/Java
Source0:	http://dist.codehaus.org/aspectwerkz/distributions/%{name}-%{version}.zip
# Source0-md5:	d7462b4d76f268e78a3843a28da71990
Patch0:		%{name}2-build_xml.patch
Patch1:		%{name}2-script.patch
URL:		http://aspectwerkz.codehaus.org/
BuildRequires:	ant >= 1.6
BuildRequires:	asm
#BuildRequires:	concurrent
#BuildRequires:	dom4j
#BuildRequires:	gnu.trove
BuildRequires:	rpm-javaprov
#BuildRequires:	jarjar
#BuildRequires:	javassist
BuildRequires:	jdk
BuildRequires:	jpackage-utils
#BuildRequires:	jrexx
BuildRequires:	junit
#BuildRequires:	junitperf
#BuildRequires:	piccolo
#BuildRequires:	qdox
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	concurrent
Requires:	dom4j
Requires:	gnu.trove
Requires:	javassist
Requires:	jrexx
Requires:	piccolo
Requires:	qdox
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AspectWerkz is a dynamic, lightweight and high-performant AOP/AOSD
framework for Java. AspectWerkz utilizes runtime bytecode modification
to weave your classes at runtime. It hooks in and weaves classes
loaded by any class loader except the bootstrap class loader. It has a
rich join point model. Aspects, advices and introductions are written
in plain Java and your target classes can be regular POJOs. You have
the possibility to add, remove and re-structure advices as well as
swapping the implementation of your introductions at runtime. Your
aspects can be defined using either an XML definition file or using
Runtime Attributes.

%description -l pl.UTF-8
AspectWerkz to dynamiczny, lekki i wydajny szkielet AOP/AOSD dla Javy.
Wykorzystuje modyfikowanie bajtkodu do modyfikowania klas w czasie
działania. Przechwytuje i modyfikuje klasy wczytywane przez wszystkie
procedury ładowania klas oprócz startowej. Ma bogady model punktu
łączenia. Aspekty, porady i wprowadzenia są napisane w czystej Javie,
a klasy docelowe mogą być zwykłymi POJO. Istnieje możliwość dodawania,
usuwania i restrukturyzacji porad, a także zamiany implementacji na
własną w trakcie działania. Aspekty mogą być definiowane przy użyciu
pliku definicji XML lub Runtime Attributes.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Requires:	jpackage-utils
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package manual
Summary:	Documents for %{name}
Summary(pl.UTF-8):	Dokumentacja dla pakietu %{name}
Group:		Documentation

%description manual
Documents for %{name}.

%description manual -l pl.UTF-8
Dokumentacja dla pakietu %{name}.

%package demo
Summary:	Samples for %{name}
Summary(pl.UTF-8):	Przykłady dla pakietu %{name}
Group:		Documentation

%description demo
Samples for %{name}.

%description demo -l pl.UTF-8
Przykłady dla pakietu %{name}.

%prep
%setup -q
find -name '*.jar' | xargs rm -vf
chmod +x bin/aspectwerkz
%patch0
%patch1

%build
export ASPECTWERKZ_HOME=$RPM_BUILD_DIR/%{name}-%{version}
build-jar-repository -s -p lib \
jarjar \
asm \
asm-attrs \
asm-util \
dom4j \
gnu.trove \
concurrent \
junit \
jrexx \
javassist \
qdox \
piccolo \
junitperf \

ln -sf %{_prefix}/lib/jvm/java-1.4.2-bea/jre/lib/managementapi.jar lib
ln -sf %{_prefix}/lib/jvm/java-1.4.2-bea/jre/lib/managementserver.jar lib

export JAVA_HOME=%{_prefix}/lib/jvm/java-1.5.0
%ant test cleandist
#export JAVA_HOME=%{_prefix}/lib/jvm/java-1.5.0
#ant test

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p target/%{name}-core-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-core-%{version}.jar
cp -p target/%{name}-extensions-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-extensions-%{version}.jar
cp -p target/%{name}-jdk14-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-jdk14-%{version}.jar
cp -p target/%{name}-jdk5-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-jdk5-%{version}.jar
cp -p target/%{name}-nodeps-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nodeps-%{version}.jar
cp -p target/%{name}-nodeps-jdk14-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nodeps-jdk14-%{version}.jar
cp -p target/%{name}-nodeps-jdk5-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nodeps-jdk5-%{version}.jar

cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}.jar; do
	ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
cd -

install -d $RPM_BUILD_ROOT%{_bindir}
cp -p bin/aspectwerkz $RPM_BUILD_ROOT%{_bindir}

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
rm -rf docs/apidocs

# demo
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/src
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/classes
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/bin
cp -pr target/samples-classes/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/classes
cp -pr src/samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/src

# manual
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -sf %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%attr(755,root,root) %{_bindir}/aspectwerkz
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}-%{version}
