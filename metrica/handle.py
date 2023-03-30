def collecting_user_agent_from_file(filename):
    file = open(filename, "r")
    in_file = file.readlines()
    in_file = [line.rstrip() for line in in_file]
    user_agents = [line.split("||") for line in in_file]
    file.close()
    return user_agents

    # print(user_agens[4][1])


def write_user_agent_in_file(user_agents, filename):
    file = open(filename, "w")
    for i in range(len(user_agents)):
        for j in range(2):
            if j == 0:
                file.write(user_agents[i][j] + " || ")
            else:
                file.write(str(user_agents[i][j]))
                file.write("\n")
    file.close()


def check_for_user_agent_in_file(UserAgent, filename):
    user_agents = collecting_user_agent_from_file(filename)
    in_list = False
    for i in range(len(user_agents)):
        if UserAgent == user_agents[i][0]:
            temp_int = int(user_agents[i][1])
            temp_int += 1
            user_agents[i][1] = str(temp_int)
            in_list = True
    if in_list == 0:
        user_agents.append([UserAgent, 1])
    write_user_agent_in_file(user_agents, filename)


def counting_all_visit(filename):
    user_agents = collecting_user_agent_from_file(filename)
    counter_visit = 0
    for i in range(len(user_agents)):
        counter_visit += user_agents[i][1]
    return counter_visit


def counting_all_unique_visitor(filename):
    user_agents = collecting_user_agent_from_file(filename)
    counter_visitor = len(user_agents)
    return counter_visitor
