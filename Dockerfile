FROM stibbons31/alpine-s6-python3-twisted

RUN pip install ansible

ENV PYTHONPATH /opt/ansible-vault-online
WORKDIR /opt/ansible-vault-online
COPY . /opt/ansible-vault-online

CMD ["/usr/bin/twistd", "--python=/opt/ansible-vault-online/ansible-vault-online.py", "-n", "--rundir=/opt/ansible-vault-online"]
