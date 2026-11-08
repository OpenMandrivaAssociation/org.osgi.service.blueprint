Name:		org.osgi.service.blueprint
Version:	1.0.2
Release:	1
Summary:	OSGi Blueprint Container API
Group:		Development/Java
License:	ASL 2.0
URL:		https://docs.osgi.org/
Source0:	https://repo1.maven.org/maven2/org/osgi/org.osgi.service.blueprint/%{version}/org.osgi.service.blueprint-%{version}-sources.jar

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.osgi:osgi.core)
BuildRequires:	mvn(org.osgi:org.osgi.annotation.versioning)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
OSGi Blueprint Container 1.0.2. The container package version is 1.0.2
and the reflect package version is 1.0.1. BlueprintEvent uses Bundle,
and ServiceUnavailableException extends ServiceException, both from
OSGi Core 6. ProviderType annotations are compile-time only. This
build targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
rm -rf META-INF
python - <<'PY'
from pathlib import Path

res = Path("src/main/resources")
for info in Path("org").rglob("packageinfo"):
    dest = res / info
    dest.parent.mkdir(parents=True, exist_ok=True)
    info.rename(dest)
Path("src/main/java").mkdir(parents=True)
Path("org").rename("src/main/java/org")

root = Path("src/main/java")
names = sorted(str(path.relative_to(root)) for path in root.rglob("*.java"))
expect = [
    "org/osgi/service/blueprint/container/BlueprintContainer.java",
    "org/osgi/service/blueprint/container/BlueprintEvent.java",
    "org/osgi/service/blueprint/container/BlueprintListener.java",
    "org/osgi/service/blueprint/container/ComponentDefinitionException.java",
    "org/osgi/service/blueprint/container/Converter.java",
    "org/osgi/service/blueprint/container/EventConstants.java",
    "org/osgi/service/blueprint/container/NoSuchComponentException.java",
    "org/osgi/service/blueprint/container/ReifiedType.java",
    "org/osgi/service/blueprint/container/ServiceUnavailableException.java",
    "org/osgi/service/blueprint/container/package-info.java",
    "org/osgi/service/blueprint/reflect/BeanArgument.java",
    "org/osgi/service/blueprint/reflect/BeanMetadata.java",
    "org/osgi/service/blueprint/reflect/BeanProperty.java",
    "org/osgi/service/blueprint/reflect/CollectionMetadata.java",
    "org/osgi/service/blueprint/reflect/ComponentMetadata.java",
    "org/osgi/service/blueprint/reflect/IdRefMetadata.java",
    "org/osgi/service/blueprint/reflect/MapEntry.java",
    "org/osgi/service/blueprint/reflect/MapMetadata.java",
    "org/osgi/service/blueprint/reflect/Metadata.java",
    "org/osgi/service/blueprint/reflect/NonNullMetadata.java",
    "org/osgi/service/blueprint/reflect/NullMetadata.java",
    "org/osgi/service/blueprint/reflect/PropsMetadata.java",
    "org/osgi/service/blueprint/reflect/RefMetadata.java",
    "org/osgi/service/blueprint/reflect/ReferenceListMetadata.java",
    "org/osgi/service/blueprint/reflect/ReferenceListener.java",
    "org/osgi/service/blueprint/reflect/ReferenceMetadata.java",
    "org/osgi/service/blueprint/reflect/RegistrationListener.java",
    "org/osgi/service/blueprint/reflect/ServiceMetadata.java",
    "org/osgi/service/blueprint/reflect/ServiceReferenceMetadata.java",
    "org/osgi/service/blueprint/reflect/Target.java",
    "org/osgi/service/blueprint/reflect/ValueMetadata.java",
    "org/osgi/service/blueprint/reflect/package-info.java",
]
if names != expect:
    raise SystemExit("java files " + " ".join(names))
versions = {
    "org/osgi/service/blueprint/container/package-info.java": '@Version("1.0.2")',
    "org/osgi/service/blueprint/reflect/package-info.java": '@Version("1.0.1")',
}
for rel, marker in versions.items():
    text = (root / rel).read_text(encoding="utf-8")
    if marker not in text:
        raise SystemExit("package-info version changed " + rel)
infos = {
    "org/osgi/service/blueprint/container/packageinfo": b"version 1.0.2\n",
    "org/osgi/service/blueprint/reflect/packageinfo": b"version 1.0.1\n",
}
found = sorted(str(path.relative_to(res)) for path in res.rglob("packageinfo"))
if found != sorted(infos):
    raise SystemExit("packageinfo set " + " ".join(found))
for rel, blob in infos.items():
    got = (res / rel).read_bytes()
    if got != blob:
        raise SystemExit("packageinfo " + rel + " " + repr(got))
if list(root.rglob("packageinfo")):
    raise SystemExit("packageinfo still beside the sources")
if "Apache License" not in Path("LICENSE").read_text(encoding="utf-8"):
    raise SystemExit("LICENSE is not the Apache license")
if not Path("about.html").is_file():
    raise SystemExit("missing about.html")
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.class")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>org.osgi.service.blueprint</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>org.osgi:org.osgi.service.blueprint</name>
  <description>OSGi Blueprint Container.</description>
  <url>https://docs.osgi.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.core</artifactId>
      <version>6.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.annotation.versioning</artifactId>
      <version>1.1.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>org.osgi.service.blueprint</artifactId>",
    "<artifactId>osgi.core</artifactId>",
    "<version>6.0.0</version>",
    "<artifactId>org.osgi.annotation.versioning</artifactId>",
    "<version>1.1.0</version>",
    "<scope>provided</scope>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "</project.build.sourceEncoding>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
if pom.count("<version>1.0.2</version>") != 1:
    raise SystemExit("project version count")
if pom.count("<version>1.1.0</version>") != 1:
    raise SystemExit("annotation version count")
if pom.count("<version>6.0.0</version>") != 1:
    raise SystemExit("core version count")
for needle in (
    "junit",
    "SNAPSHOT",
    "<source>",
    "<target>",
    "<parent>",
    "felix",
    "maven-bundle-plugin",
    "<artifactId>osgi.annotation</artifactId>",
    "<artifactId>org.osgi.framework</artifactId>",
    "<version>1.0.1</version>",
    "<version>8.0.1</version>",
    "<version>8.1.0</version>",
    "projectbuild.sourceEncoding",
):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.osgi.service.blueprint-%{version}.jar --describe-module org.osgi.service.blueprint > module-describe.txt
grep -q '^org.osgi.service.blueprint' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
python - <<'PY'
import zipfile
from pathlib import Path
jar = Path("target/org.osgi.service.blueprint-%{version}.jar")
with zipfile.ZipFile(jar) as zf:
    names = set(zf.namelist())
    infos = {
        "org/osgi/service/blueprint/container/packageinfo": b"version 1.0.2\n",
        "org/osgi/service/blueprint/reflect/packageinfo": b"version 1.0.1\n",
    }
    for rel, blob in infos.items():
        if zf.read(rel) != blob:
            raise SystemExit("jar packageinfo " + rel)
required = {
    "org/osgi/service/blueprint/container/BlueprintContainer.class",
    "org/osgi/service/blueprint/container/BlueprintEvent.class",
    "org/osgi/service/blueprint/container/BlueprintListener.class",
    "org/osgi/service/blueprint/container/ComponentDefinitionException.class",
    "org/osgi/service/blueprint/container/Converter.class",
    "org/osgi/service/blueprint/container/EventConstants.class",
    "org/osgi/service/blueprint/container/NoSuchComponentException.class",
    "org/osgi/service/blueprint/container/ReifiedType.class",
    "org/osgi/service/blueprint/container/ServiceUnavailableException.class",
    "org/osgi/service/blueprint/container/package-info.class",
    "org/osgi/service/blueprint/reflect/BeanArgument.class",
    "org/osgi/service/blueprint/reflect/BeanMetadata.class",
    "org/osgi/service/blueprint/reflect/BeanProperty.class",
    "org/osgi/service/blueprint/reflect/CollectionMetadata.class",
    "org/osgi/service/blueprint/reflect/ComponentMetadata.class",
    "org/osgi/service/blueprint/reflect/IdRefMetadata.class",
    "org/osgi/service/blueprint/reflect/MapEntry.class",
    "org/osgi/service/blueprint/reflect/MapMetadata.class",
    "org/osgi/service/blueprint/reflect/Metadata.class",
    "org/osgi/service/blueprint/reflect/NonNullMetadata.class",
    "org/osgi/service/blueprint/reflect/NullMetadata.class",
    "org/osgi/service/blueprint/reflect/NullMetadata$1.class",
    "org/osgi/service/blueprint/reflect/PropsMetadata.class",
    "org/osgi/service/blueprint/reflect/RefMetadata.class",
    "org/osgi/service/blueprint/reflect/ReferenceListMetadata.class",
    "org/osgi/service/blueprint/reflect/ReferenceListener.class",
    "org/osgi/service/blueprint/reflect/ReferenceMetadata.class",
    "org/osgi/service/blueprint/reflect/RegistrationListener.class",
    "org/osgi/service/blueprint/reflect/ServiceMetadata.class",
    "org/osgi/service/blueprint/reflect/ServiceReferenceMetadata.class",
    "org/osgi/service/blueprint/reflect/Target.class",
    "org/osgi/service/blueprint/reflect/ValueMetadata.class",
    "org/osgi/service/blueprint/reflect/package-info.class",
}
missing = sorted(required - names)
if missing:
    raise SystemExit("missing " + " ".join(missing))
extra = sorted(name for name in names if name.endswith(".class") and name not in required)
if extra:
    raise SystemExit("extra " + " ".join(extra))
PY

%files -f .mfiles
%doc LICENSE about.html
