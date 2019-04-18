# SSH Config manager

A simple way to manage hosts from your ~/.ssh/config file.

Config:
```
Host *
IdentityFile ~/.ssh/id_rsa
UseKeyChain yes
AddKeysToAgent yes

Host project-sandbox
HostName vps-1.example-project.com
User devops

Host project-prod
HostName vps-2.example-project.com
User devops

Host container
HostName project-containers.com
User devops
Port 2228
```

SSHC List:
```
[user:~]$ sshc
*               (key: ~/.ssh/id_rsa)
project-sandbox [ devops@vps-1.example-project.com ]
project-prod    [ devops@vps-2.example-project.com ]
container       [ devops@project-containers.com ]:2228
```

Adding a new host
```
[user:~]$ sshc add container2 devops@project-containers.com:2229
```

Using it:
```
[user:~]$ ssh container2
```
