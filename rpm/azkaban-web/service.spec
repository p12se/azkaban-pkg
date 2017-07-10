%{!?_release: %define _release 0}
%{!?_version: %define _version 0.0.0}

%define product azkaban
%define service web

Name:             %{product}-%{service}
Summary:          Campaign management: Java API.
Version:          %{_version}
Release:          %{_release}
License:          (c) 2017 Thumbtack Technology, LLC
#Group:            Dataswitch/Campaign Management
Vendor:           Thumbtack Technology, LLC
#URL:              http://thumbtack.net/skills/dataswitch.html
Packager:         Thumbtack DevOps Team, <devops-team@thumbtack.net>
BuildArch:        noarch
Requires(pre):    /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Prefix:           /opt/%{product}

%define __jar_repack %{nil}

# Define home, log and data directories as well as
# an owner for installed services
%define home  /opt/%{product}-%{service}
%define logs  %{_localstatedir}/log/%{product}-%{service}
%define owner %{product}

%description
  This package provides Azkaban WebUI.

%prep
# Clean all old content from the BUILD directory
rm -rf *
ln -fs $RPM_SOURCE_DIR/* .

%build
export AZ_SVC_OWNER=%{owner} AZ_SVC_NAME=%{product}-%{service}
export AZ_SVC_HOME=%{home} AZ_SVC_LOGS=%{logs}
envsubst '${AZ_SVC_OWNER},${AZ_SVC_HOME},${AZ_SVC_NAME},${AZ_SVC_LOGS}' < rpm/systemd.service.tp > %{product}-%{service}.service
envsubst '${AZ_SVC_HOME},${AZ_SVC_NAME},${AZ_SVC_LOGS}' < rpm/log4j.properties > log4j.properties

%install
rm -rf %{buildroot}
# Create home and log directories
%{__install} -m 755 -d %{buildroot}/%{home}/bin %{buildroot}/%{home}/lib %{buildroot}/%{home}/conf %{buildroot}/%{home}/extlib %{buildroot}/%{home}/plugins %{buildroot}/%{logs} %{buildroot}/%{home}/web
%{__ln_s} -f %{logs} %{buildroot}/%{home}/log

# Install  binaries, libraries and configuration files
cp azkaban/azkaban-web-server/build/install/azkaban-web-server/bin/* %{buildroot}/%{home}/bin/
cp azkaban/azkaban-web-server/build/install/azkaban-web-server/lib/* %{buildroot}/%{home}/lib/
cp -r azkaban/azkaban-web-server/build/install/azkaban-web-server/web/* %{buildroot}/%{home}/web/
%{__install} -m 644 -D rpm/azkaban-web/azkaban-users.xml %{buildroot}/%{home}/conf/
%{__install} -m 644 -D rpm/azkaban-web/azkaban.properties %{buildroot}/%{home}/conf/
%{__install} -m 644 -D rpm/global.properties %{buildroot}/%{home}/conf/
%{__install} -m 644 -D %{product}-%{service}.service %{buildroot}%{_prefix}/lib/systemd/system/%{product}-%{service}.service
%{__install} -m 664 -D rpm/log4j.properties %{buildroot}/%{home}/conf/log4j.properties

%files
%defattr(-,%{owner},%{owner},-)
%{home}
%{logs}
%defattr(-,root,root,-)
%{_prefix}/lib/systemd/system/%{product}-%{service}.service

%pre
getent group %{owner} >/dev/null || groupadd -r %{owner}
getent passwd %{owner} >/dev/null || useradd -r -g %{owner} %{owner} -s /sbin/nologin >/dev/null

%post
systemctl enable %{service}

%preun
systemctl disable %{service}
systemctl stop %{service}

%postun
#TODO: Need to understand this behaviour when you upgrade pacckage
#      It may be a reason why owner disappears while upgrading package
#/usr/sbin/userdel %{owner}

%clean
rm -rf *

#%changelog


