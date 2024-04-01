from environment import BlackJackEnv

env = BlackJackEnv()
observation = env.reset()
episode_count = 0

while episode_count < 1:


    # observation[0] elemanını kontrol ederek yazdırma işlemi
    if isinstance(observation[0], list):
        for obj in observation[0]:
            print(obj)
    else:
        print(observation[0])
        print(observation[1])


    print("0 - Stand")
    print("1 - Hit")
    print("2 - Double")
    print("3 - Split")
    action = int(input("Lütfen bir seçenek için ilgili numarayı girin (0-3 arası): "))
    observation, reward, done, _, info = env.step(action)




    if done:
        print(observation[0])
        print(observation[1])
        print("reward =", reward)
        print("Win" if reward > 0 else ("Lose" if reward < 0 else "Draw"))
        episode_count += 1
        observation = env.reset()


env.close()
