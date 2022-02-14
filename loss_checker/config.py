import ovcfg

sc = {
    'server_ip': '0.0.0.0',
    'ip_check_list': [],
    'server_port': 800,
}
cfg = ovcfg.Config(std_config=sc, file='loss_checker.json', cfg_dir_name='.').import_config()
