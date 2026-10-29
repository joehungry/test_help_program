import time, os, winsound
from background import opnum, prints

passed_time: float = 0.0

time_limit: int = 0
problem_num: int = 0
solved_problem: int = 0
problem_time_limit: float = 0

def secondsToHMS(seconds: int) -> tuple[int, int, int]:
    done_hr: int = seconds // 3600
    done_min: int = (seconds % 3600) // 60
    done_sec: int = seconds % 60
    return done_hr, done_min, done_sec

if __name__ == '__main__':
    os.system("title " + '適性検査計測')
    os.system('cls')
    problem_sound = 'background/sound/problem_ding.wav'

    while True:
        input_string = prints.ask('試験の時間は何分ですか')
        if opnum.is_int(input_string) == True:
            time_limit = int(input_string) * 60
            break
        else:
            os.system('cls')
            prints.err('整数を入力してください')

    while True:
        input_string = prints.ask('問題数は何個ですか')
        if opnum.is_int(input_string) == True:
            problem_num = int(input_string)
            break
        else:
            os.system('cls')
            prints.err('整数を入力してください')

    problem_time_limit = time_limit / problem_num
    #一問当たりのタイムリミット

    there_is_change = True
    start_time: float = time.time()
    now_time: float = start_time
    time_seconds: int = 0
    while True:
        now_time = time.time()
        passed_time = now_time - start_time
        hour, minute, seconds = secondsToHMS(int(passed_time))

        #this sees if a second has passed and handles it accordingly
        if int(passed_time) > time_seconds:
            there_is_change = True
            time_seconds = int(passed_time)

        #一問のタイムリミットが終わったら、次の問題へのタイムリミットが始まる
        temp_solved_problem = int(passed_time // problem_time_limit)
        if temp_solved_problem > solved_problem:
            winsound.PlaySound(problem_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
            there_is_change = True
            solved_problem = temp_solved_problem

        if there_is_change == True:
            os.system('cls')
            print(f'{hour}時間{minute}分{seconds}秒経過')
            print(f'{solved_problem}問目完了')
            there_is_change = False

            solved_problem = min(temp_solved_problem, problem_num)
