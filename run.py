from ip_tester_2_0 import ip_validator
from gp_operations import gp_operator

cur_valid_path = "Python_scripts/valid_ip_list.txt"
cur_raw_path = "Python_scripts/raw_ip_list.txt"
cur_agents_path = "Python_scripts/static_agents_list.txt"
storage_path = "/mnt/s01/praktyki/"
overwrite = True

validator = ip_validator(cur_valid_path, cur_raw_path, overwrite)
gp_op = gp_operator(cur_valid_path, cur_agents_path, storage_path, True, True)

validator.ip_validate()
gp_op.audio_extraction()
