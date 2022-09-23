FROM registry.redhat.io/ubi7/python-36:latest
USER root
LABEL name="art-dash" \
  description="art-dash container image" \
  maintainer="OpenShift Automated Release Tooling (ART) Team <aos-team-art@redhat.com>"

RUN yum -y --setopt skip_missing_names_on_install=False \
    krb5-workstation git rsync \
    # development dependencies
    gcc krb5-devel \
    # other tools
    bash-completion vim tmux wget curl iputils procps-ng psmisc net-tools iproute \
    # install brewkoji
    koji brewkoji \
    mariadb-connector-c-devel openssl-devel \
 && yum clean all

ARG OC_VERSION=candidate
# include oc client
RUN wget -O /tmp/openshift-client-linux-"$OC_VERSION".tar.gz https://mirror.openshift.com/pub/openshift-v4/clients/ocp/"$OC_VERSION"/openshift-client-linux.tar.gz \
  && tar -C /usr/local/bin -xzf  /tmp/openshift-client-linux-"$OC_VERSION".tar.gz oc kubectl \
  && rm /tmp/openshift-client-linux-"$OC_VERSION".tar.gz


# Create a non-root user - see https://aka.ms/vscode-remote/containers/non-root-user.
ARG USERNAME=dev
# On Linux, replace with your actual UID, GID if not the default 1000
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the "dev" user
RUN groupadd --gid "$USER_GID" "$USERNAME" \
 && useradd --uid "$USER_UID" --gid "$USER_GID" -m "$USERNAME" \
 # give access to its files
 && mkdir -p /workspaces/art-dash \
 && mkdir -p /workspaces/{elliott,doozer}{,-working-dir} \
 && mkdir -p /home/"$USERNAME"/.config/{elliott,doozer,art-dash} \
 && mkdir -p /home/"$USERNAME"/.docker \
 && chown -R "${USER_UID}:${USER_GID}" /home/"$USERNAME" /workspaces \
 && chmod -R 0755 /home/"$USERNAME" \
 && chmod -R 0777 /workspaces \
 # and allow it passwordless sudo
 && echo "$USERNAME" ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/"$USERNAME" \
 && chmod 0440 /etc/sudoers.d/"$USERNAME"

USER "$USER_UID"
WORKDIR /workspaces/art-dash

# install dependencies (allow even openshift's random user to see)
ENV PATH=/home/"$USERNAME"/.local/bin:/home/"$USERNAME"/bin:"$PATH"
COPY requirements.txt ./
RUN umask a+rx && pip3 install --upgrade \
    git+https://github.com/openshift/doozer.git#egg=rh-doozer \
    git+https://github.com/openshift/elliott.git#egg=rh-elliott \
    -r ./requirements.txt

# install art-dash and default configs
COPY conf/krb5-redhat.conf /etc/krb5.conf
COPY . /tmp/art-dash
USER 0
RUN cp -r /tmp/art-dash/umb . \
 && cp /tmp/art-dash/container/doozer-settings.yaml /home/"$USERNAME"/.config/doozer/settings.yaml \
 && cp /tmp/art-dash/container/elliott-settings.yaml /home/"$USERNAME"/.config/elliott/settings.yaml \
# && cp /tmp/art-dash/settings.yaml /home/"$USERNAME"/.config/art-dash/settings.yaml \
 && rm -rf /tmp/art-dash
USER "$USER_UID"
EXPOSE 8080
CMD ["./start-cmd.sh"]