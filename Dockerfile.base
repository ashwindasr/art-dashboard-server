FROM registry.fedoraproject.org/fedora:33
LABEL name="art-dash" \
  description="art-dash container image" \
  maintainer="OpenShift Automated Release Tooling (ART) Team <aos-team-art@redhat.com>"

# the build will need to run inside the firewall to access internal resources.
# install Red Hat IT Root CA and RCM repos
RUN curl -o /etc/pki/ca-trust/source/anchors/RH-IT-Root-CA.crt --fail -L \
    https://password.corp.redhat.com/RH-IT-Root-CA.crt \
 && update-ca-trust extract \
 && curl -o /etc/yum.repos.d/rcm-tools-fedora.repo https://download.devel.redhat.com/rel-eng/RCMTOOLS/rcm-tools-fedora.repo \
 && dnf install -y \
    # runtime dependencies
    krb5-workstation git rsync \
    python3.6 python3-certifi python3-rpm python3-rhmsg \
    # development dependencies
    gcc krb5-devel python3-devel python3-pip \
    # other tools
    bash-completion vim tmux wget curl iputils procps-ng psmisc net-tools iproute \
    # install brewkoji
    koji brewkoji \
    mariadb-connector-c-devel openssl-devel \
 && dnf clean all

ARG OC_VERSION=candidate
# include oc client
RUN wget -O /tmp/openshift-client-linux-"$OC_VERSION".tar.gz https://mirror.openshift.com/pub/openshift-v4/clients/ocp/"$OC_VERSION"/openshift-client-linux.tar.gz \
  && tar -C /usr/local/bin -xzf  /tmp/openshift-client-linux-"$OC_VERSION".tar.gz oc kubectl \
  && rm /tmp/openshift-client-linux-"$OC_VERSION".tar.gz


USER 0
COPY requirements.txt ./
RUN umask a+rx && pip3 install --upgrade \
    git+https://github.com/openshift/doozer.git#egg=rh-doozer \
    git+https://github.com/openshift/elliott.git#egg=rh-elliott \
    -r ./requirements.txt

RUN mkdir -p /root/.config/doozer
COPY . /tmp/art-dash
RUN cp -r /tmp/art-dash/umb . \
 && cp /tmp/art-dash/container/doozer-settings.yaml /root/.config/doozer/settings.yaml \
 && rm -rf /tmp/art-dash

# install art-dash and default configs
COPY conf/krb5-redhat.conf /etc/krb5.conf