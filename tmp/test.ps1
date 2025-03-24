
full_capacity = int(subprocess.check_output(cmd, shell=True))
return max(1, min(100, round((full_capacity / design_capacity) * 100)))