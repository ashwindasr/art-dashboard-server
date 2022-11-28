import subprocess


def handle_kinit():
    """
    This function tests whether kinit is required. The current policy is to do kinit after
    every hour.
    :return: None
    """

    keytab_file = "/tmp/keytab/redhat.keytab"
    print(keytab_file)
    kinit_request = subprocess.Popen(["kinit", "-kt", keytab_file, "ocp-readonly/psi.redhat.com@REDHAT.COM"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = kinit_request.communicate()
    if error:
        print(error)
