test = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)"

def collecting_user_agent_from_file():
    file = open("counting.txt", "r")
    in_file = file.readlines()
    in_file = [line.rstrip() for line in in_file]
    user_agents = [line.split("||") for line in in_file]
    file.close()
    return user_agents

    # print(user_agens[4][1])


def write_user_agent_in_file(user_agents):
    file = open("counting.txt", "w")
    for i in range(len(user_agents)):
        for j in range(2):
            if j == 0:
                file.write(user_agents[i][j] + "||")
            else:
                file.write(user_agents[i][j])
                file.write("\n")
    file.close()


def check_for_user_agent_in_file(UserAgent):
    user_agents = collecting_user_agent_from_file()
    in_list = False
    for i in range(len(user_agents)):
        if UserAgent == user_agents[i][0]:
            temp_int = int(user_agents[i][1])
            temp_int += 1
            user_agents[i][1] = str(temp_int)
            in_list = True
    if in_list == 0:
        user_agents.append([UserAgent, 1])
    write_user_agent_in_file(user_agents)


if __name__ == '__main__':
    check_for_user_agent_in_file(test)
