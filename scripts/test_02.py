
acc_proxy_reply = "[S02, Analyzing Object]"

# Log the reply from the accuracy proxy model to the robot_instance action_space
# Parse the accuracy proxy reply to identify the state
state_code, _ = acc_proxy_reply.strip("[]").split(", ")
state_code = state_code.strip("'")

print(state_code)