default[:chef_package] = "chef-server-core_12.17.33-1.amd64.deb" 
default[:assets_bucket] = "happypathway-assets"


default["chef_server"]["org"] = {
	:short_name => "bootstrap",
	:full_name => "bootstrap",
	:server_url => "https://api.chef.io/organizations/bootstrap"
}