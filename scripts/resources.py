import json

import ansible
from twisted.web import static, resource
from ansible.parsing.vault \
    import format_vaulttext_envelope, parse_vaulttext_envelope, VaultSecret, CIPHER_MAPPING, to_bytes


class Root(static.File):
    isLeaf = False

    def __init__(self, path, defaultType="text/html", ignoredExts=(), registry=None, allowExt=0):
        static.File.__init__(self, path)


class Crypt(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setResponseCode(405)
        return b"Crypt service accepts only POST requests!"

    def render_POST(self, request):

        request.setHeader("Content-Type", "application/json; charset=utf-8")
        version, cipher, vault_id = '1.1', 'AES256', ''
        is_source_encrypted = True
        try:
            body = json.loads(request.content.read())
        except:
            request.setResponseCode(400)
            return json.dumps({"value": "bad input object"}).encode('utf-8')

        if body.get("password"):
            secret = VaultSecret(to_bytes(body["password"], "utf-8", errors='strict'))

            source = body.get("source", "")
            source = to_bytes(source, "utf-8", errors='strict')
            try:
                (payload, version, cipher, vault) = parse_vaulttext_envelope(source)
            except ansible.errors.AnsibleError:
                # maybe not encrypted
                is_source_encrypted = False
                payload = source

            try:
                this_cipher = CIPHER_MAPPING[cipher]()
            except Exception as e:
                request.setResponseCode(400)
                response_text = e.message
                return json.dumps({"value": "error in %s" % response_text}).encode('utf-8')

            try:
                if is_source_encrypted:
                    response_text = this_cipher.decrypt(payload, secret=secret)
                else:
                    response_text = format_vaulttext_envelope(this_cipher.encrypt(payload, secret=secret), cipher,
                                                              version, vault_id).strip()
            except ansible.errors.AnsibleError as e:
                request.setResponseCode(400)
                response_text = e.message
                return json.dumps({"value": response_text}).encode('utf-8')

        else:
            request.setResponseCode(400)
            response_text = b"password not specified"

        return json.dumps({"value": response_text.decode('utf-8')}).encode('utf-8')
