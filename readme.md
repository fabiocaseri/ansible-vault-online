## Online way to work with ansible-vault
* Easy to use: your password manager can easy auto-fill form
* Bash, editor plugins not required 
* Uses ansible to encrypt/decrpyt your settings
![alt text](https://raw.githubusercontent.com/xxbbxb/ansible-vault-online/master/vault-screenshot.png)

### Running in Docker container

To run it listening on port `8000`:

```shell
docker run -d -p 8000:8081 fabiocaseri/ansible-vault-online
```
