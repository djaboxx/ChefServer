default[:consul][:packages] = [
    {
        :pkg => "https://releases.hashicorp.com/consul/1.1.0/consul_1.1.0_linux_amd64.zip",
        :pkg_name => "consul.zip"
    },
    {
        :pkg => "https://releases.hashicorp.com/vault/0.10.1/vault_0.10.1_linux_amd64.zip",
        :pkg_name => "vault.zip"
    }
]