import subprocess


def handle_kinit():
    """
    Funtion performs kinit
    :return: None
    """

    keytab_file = "/tmp/keytab/redhat.keytab"
    kinit_request = subprocess.Popen(["kinit", "-kt", keytab_file, "ocp-readonly/psi.redhat.com@REDHAT.COM"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = kinit_request.communicate()
    if error:
        print(error)
