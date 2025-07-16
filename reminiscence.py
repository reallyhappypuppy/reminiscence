import os
import random
import time

# 기본 설정
DUNGEON_WIDTH = 10
DUNGEON_HEIGHT = 10
ROOM_W = 7
ROOM_H = 6

room_x, room_y = 0, 0
player_px = ROOM_W // 2
player_py = ROOM_H // 2
guardian_talked = False

memory_fragments = set(random.sample([(x, y) for x in range(10) for y in range(10)], 10))
memory_collected = 0
memory_messages = [
    [
        "어렴풋이 들리는 목소리...",
        "'괜찮아, 내가 널 지켜줄게.'",
        "그 따뜻한 말이 귓가에 메아리친다.",
    ],
    [
        "햇살 가득한 오후, 마당에 그네가 있었다.",
        "나는 웃으며 그네를 타고 있었고,",
        "누군가가 등을 밀어주며 말했다. '더 높이, 더 멀리!'",
    ],
    [
        "차가운 겨울날, 얼어붙은 손을 누군가가 감쌌다.",
        "그 온기, 그 손길... 기억난다.",
        "지금은 사라진 그 사람의 손.",
    ],
    [
        "문득 떠오른 이름, '아리엘...'.",
        "그 이름에 심장이 요동쳤다.",
        "잊고 있었던, 하지만 너무나도 소중한 사람.",
    ],
    [
        "깊은 밤, 별이 쏟아지던 하늘 아래.",
        "누군가와 나란히 누워 별을 세고 있었다.",
        "'다음 생에도... 함께일 수 있을까?'",
    ],
    [
        "책 속에서 발견한 오래된 편지 한 장.",
        "'이 편지를 보게 된다면, 나는 이미...'으로 시작되던 문장.",
        "끝맺지 못한 말이 마음을 후벼 팠다.",
    ],
    [
        "비가 내리던 날, 우산은 하나뿐이었다.",
        "우산 아래 두 사람이 가까이 붙어 걸었다.",
        "'비 맞는 것도 나쁘지 않네.' 그 사람의 웃음이 떠오른다.",
    ],
    [
        "거울 속 얼굴은 낯설었다.",
        "하지만 눈동자만큼은, 분명 나였다.",
        "나는 누구였을까? 아니, 나는 누구인가?",
    ],
    [
        "손끝으로 피아노를 누르던 감각.",
        "직접 만든 멜로디가 방 안을 가득 채웠다.",
        "그 음악은 이제 내 안에만 남았다.",
    ],
    [
        "마침내, 모든 조각이 맞춰졌다.",
        "이 여정은 나를 위한 것이었다.",
        "'기억한다. 나는... 나였어.'",
        "'나를 기다리는 사람이 있어!'",
    ]
]

soul_messages = [
    "혼: '기억은 존재의 증명일까, 고통의 잔재일까...'",
    "혼: '잊는다는 건, 살아가기 위한 방편일지도 몰라.'",
    "혼: '여기 있는 우리는 모두, 누군가의 꿈이었지.'",
    "혼: '과거를 붙잡는 건, 앞으로 나아가길 두려워하기 때문이야.'",
    "혼: '너는 너라는 것을 어떻게 증명할 수 있을까?'",
    "혼: '이 세계도 언젠가 사라질 거야. 그땐 무엇이 남을까?'",
    "혼: '끝이란 존재할까? 혹은 그저 다른 시작일 뿐일까.'",
    "혼: '말해줘. 네가 찾고 있는 건 정말 기억일까, 아니면 진실일까?'",
    "혼: '삶과 죽음의 경계, 그 어딘가에 우리가 있어.'",
    "혼: '모든 것은 연결되어 있어. 잊혀진 것조차도.'",
]

DOOR_POS = {
    "up":    (ROOM_W // 2, 0),
    "down":  (ROOM_W // 2, ROOM_H - 1),
    "left":  (0, ROOM_H // 2),
    "right": (ROOM_W - 1, ROOM_H // 2),
}
GUARDIAN_POS = (ROOM_W // 2, ROOM_H // 2 - 1)
ESCAPE_POS = (ROOM_W - 2, ROOM_H - 2)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_title():
    clear()
    print(r"""
██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗███████╗ ██████╗███████╗███╗   ██╗ ██████╗███████╗
██╔═██║ ██╔════╝████╗ ████║██║████╗  ██║██║██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝
█████╔╝ █████╗  ██╔████╔██║██║██╔██╗ ██║██║███████╗██║     █████╗  ██╔██╗ ██║██║     █████╗  
██╔═██╗ ██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║╚════██║██║     ██╔══╝  ██║╚██╗██║██║     ██╔══╝  
██║ ╚██╗███████╗██║ ╚═╝ ██║██║██║ ╚████║██║███████║╚██████╗███████╗██║ ╚████║╚██████╗███████╗
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝

                        A Text-Based Journey of Forgotten Memories
    """)
    print("1. 게임 시작")
    print("2. 종료")
    choice = input("\n>> 선택 (1/2): ")
    if choice != '1':
        exit()

def show_prologue():
    clear()
    prologue_lines = [
        "…",
        "어둠 속에서 눈을 떴다.",
        "여기가 어디지…? 왜 아무것도 기억나지 않는 거지?",
        "주변엔 낯선 방들이 끝없이 이어지고 있었다.",
        "무언가를… 되찾아야 해. 반드시."
    ]
    for line in prologue_lines:
        print(line)
        print()
        time.sleep(1.8)
    input("\n[엔터를 눌러 시작하세요]")

class Room:
    def __init__(self, rx, ry):
        self.rx = rx
        self.ry = ry
        self.map = [['.' for _ in range(ROOM_W)] for _ in range(ROOM_H)]
        self.guardian = (rx == 9 and ry == 9)
        self.has_memory = (rx, ry) in memory_fragments
        self.fragment_pos = None
        self.escape_open = False

        self.has_soul = False
        self.soul_pos = None
        self.soul_talked = False

        self.has_self = False
        self.self_pos = None

        self.self_absorbed = False  # 자아 흡수 상태

        self.add_walls_and_doors()

    def add_walls_and_doors(self):
        for y in range(ROOM_H):
            for x in range(ROOM_W):
                if x == 0 or x == ROOM_W - 1 or y == 0 or y == ROOM_H - 1:
                    self.map[y][x] = '#'

        if self.ry > 0:
            x, y = DOOR_POS["up"]
            self.map[y][x] = ' '
        if self.ry < DUNGEON_HEIGHT - 1:
            x, y = DOOR_POS["down"]
            self.map[y][x] = ' '
        if self.rx > 0:
            x, y = DOOR_POS["left"]
            self.map[y][x] = ' '
        if self.rx < DUNGEON_WIDTH - 1:
            x, y = DOOR_POS["right"]
            self.map[y][x] = ' '

        if self.guardian:
            gx, gy = GUARDIAN_POS
            self.map[gy][gx] = 'G'

        if self.has_memory:
            while True:
                fx = random.randint(1, ROOM_W - 2)
                fy = random.randint(1, ROOM_H - 2)
                if self.map[fy][fx] == '.':
                    self.fragment_pos = (fx, fy)
                    self.map[fy][fx] = '✦'
                    break

    def open_escape_door(self):
        self.map[ESCAPE_POS[1]][ESCAPE_POS[0]] = '🚪'
        self.escape_open = True

    def add_self(self):
        # 0,0방 자아 생성
        for y in range(1, ROOM_H - 1):
            for x in range(1, ROOM_W - 1):
                if self.map[y][x] == '.':
                    self.self_pos = (x, y)
                    self.map[y][x] = 'Ω'
                    self.has_self = True
                    self.self_absorbed = False
                    return

    def remove_self(self):
        if self.has_self and self.self_pos:
            x, y = self.self_pos
            self.map[y][x] = '.'
            self.has_self = False
            self.self_pos = None
            self.self_absorbed = True  # 흡수 완료

dungeon = [[Room(x, y) for x in range(DUNGEON_WIDTH)] for y in range(DUNGEON_HEIGHT)]

soul_positions = random.sample([(x,y) for x in range(10) for y in range(10)], 10)
for sx, sy in soul_positions:
    room = dungeon[sy][sx]
    while True:
        px = random.randint(1, ROOM_W - 2)
        py = random.randint(1, ROOM_H - 2)
        if room.map[py][px] == '.':
            room.has_soul = True
            room.soul_pos = (px, py)
            room.map[py][px] = 'ψ'
            room.soul_talked = False
            break

soul_talk_index = 0

def draw_current_room():
    clear()
    room = dungeon[room_y][room_x]
    for y in range(ROOM_H):
        for x in range(ROOM_W):
            if x == player_px and y == player_py:
                print('@', end='')
            elif room.has_self and room.self_pos == (x,y) and not room.self_absorbed:
                print('Ω', end='')
            else:
                print(room.map[y][x], end='')
        print()
    print(f"현재 방: ({room_x}, {room_y})  위치: ({player_px}, {player_py})")
    print(f"✦ 기억 조각: {memory_collected} / 10")

    if room.guardian and not guardian_talked:
        gx, gy = GUARDIAN_POS
        if abs(player_px - gx) + abs(player_py - gy) == 1:
            print("G가 당신 앞에 있습니다. 'E' 키로 대화할 수 있습니다.")

    if room.has_soul and not room.soul_talked:
        sx, sy = room.soul_pos
        if abs(player_px - sx) + abs(player_py - sy) == 1:
            print("👻 혼이 당신 근처에 있습니다. 'E' 키로 대화할 수 있습니다.")

    if room.has_self and not room.self_absorbed:
        sx, sy = room.self_pos
        if abs(player_px - sx) + abs(player_py - sy) == 1:
            print("Ω 상처받은 자아가 당신 근처에 있습니다. 'E' 키로 대화할 수 있습니다.")

def handle_movement(cmd):
    global player_px, player_py, room_x, room_y, memory_collected

    dx, dy = 0, 0
    if cmd == 'w': dy = -1
    elif cmd == 's': dy = 1
    elif cmd == 'a': dx = -1
    elif cmd == 'd': dx = 1
    else: return

    nx, ny = player_px + dx, player_py + dy
    room = dungeon[room_y][room_x]

    if 0 <= nx < ROOM_W and 0 <= ny < ROOM_H:
        target = room.map[ny][nx]
        if target in ['.', ' ', 'G', '✦', '🚪', 'ψ']:
            player_px, player_py = nx, ny

            # 기억 조각 수집
            if target == '✦':
                print("\n" + "=" * 50)
                print("✦ 기억 조각을 회수했습니다!\n")
                if memory_collected < len(memory_messages):
                    message = memory_messages[memory_collected]
                    for line in message:
                        print(f"🧩 {line}\n")
                else:
                    print("🧩 잊혀진 기억 하나가 돌아왔다.\n")
                print("=" * 50)
                memory_collected += 1
                room.has_memory = False
                room.map[ny][nx] = '.'
                input("\n>> (엔터를 누르세요)")

    # 문 통과
    for dir_name, (door_x, door_y) in DOOR_POS.items():
        if player_px == door_x and player_py == door_y:
            if dir_name == "up" and room_y > 0:
                room_y -= 1
                player_px, player_py = DOOR_POS["down"]
            elif dir_name == "down" and room_y < DUNGEON_HEIGHT - 1:
                room_y += 1
                player_px, player_py = DOOR_POS["up"]
            elif dir_name == "left" and room_x > 0:
                room_x -= 1
                player_px, player_py = DOOR_POS["right"]
            elif dir_name == "right" and room_x < DUNGEON_WIDTH - 1:
                room_x += 1
                player_px, player_py = DOOR_POS["left"]
            break

def all_souls_talked():
    count = 0
    for row in dungeon:
        for room in row:
            if room.has_soul and room.soul_talked:
                count += 1
    return count == 10

def handle_interaction():
    global guardian_talked, soul_talk_index

    room = dungeon[room_y][room_x]

    # 자아 대화 및 흡수 처리
    if room.has_self and not room.self_absorbed:
        sx, sy = room.self_pos
        if abs(player_px - sx) + abs(player_py - sy) == 1:
            draw_current_room()
            print("\nΩ 상처받은 자아: '오랜 시간 너를 기다렸어...'")
            time.sleep(2)
            print("Ω 자아: '너는 나를 받아줄 수 있니?'")
            time.sleep(2)
            print("Ω 자아가 당신의 내면에 스며듭니다...")
            time.sleep(2.5)
            room.remove_self()
            input(">> (엔터를 눌러 계속)")
            return

    # 가디언 대화
    if room.guardian and not guardian_talked:
        gx, gy = GUARDIAN_POS
        if abs(player_px - gx) + abs(player_py - gy) == 1:
            guardian_talked = True
            draw_current_room()
            print("\n👤 G: '때로는 진실을 모르는 것이 도움이 될수도 있습니다...'")
            print("G: '이곳에서 나가는 순간 소중한 기억을 잃을수도 있죠...")
            print("G: '그 너머에 무엇이 있는지... 후회하지 않을 자신이 있다면 여기를 떠나시지요...'")
            print("🚪 우하단에 자신의 세계로 돌아가는 문이 열렸습니다!")
            room.open_escape_door()
            input(">> (엔터를 눌러 계속)")
            # 자아 생성 조건 체크
            if memory_collected == 10 and all_souls_talked():
                dungeon[0][0].add_self()
            return

    # 혼 대화
    if room.has_soul and not room.soul_talked:
        sx, sy = room.soul_pos
        if abs(player_px - sx) + abs(player_py - sy) == 1:
            room.soul_talked = True
            draw_current_room()
            if soul_talk_index < len(soul_messages):
                print("\n👻 " + soul_messages[soul_talk_index])
                soul_talk_index += 1
            else:
                print("\n👻 혼의 침묵이 흐른다...")
            input(">> (엔터를 눌러 계속)")
            return

def show_ending(hidden=False):
    clear()
    if hidden:
        print("🌟 모든 기억과 혼, 그리고 자아를 되찾았다!")
        print("🚪 자아와 함께 이곳을 벗어나 새로운 시작을 맞이한다...")
        print("\n=== 히든 엔딩 ===\n")
        credits = [
            "점차 시야가 밝아지더니 무언가 형체가 보이기 시작한다...",
            "나: '다... 당신은!!!'",
            "자신이 그렇게도 그리워 하던 사람이 바로 앞에 보인다...",
            "그 사람이 기쁨과 슬픔이 혼재된 표정으로 말한다...",
            "'저를 기억하시나요?'",
            "나는 웃으며 대답한다...",
            "'다녀왔어'"
        ]
        for line in credits:
            print(line)
            time.sleep(3)
        print("\n Made by NS_20730... 'REMINISCENCE'")
    else:
        if memory_collected == 10:
            print("🌟 모든 기억을 되찾고, 그대는 진실을 마주했다.")
            print("💫 당신은 침대에 누워있으며 서서히 눈을 뜨고 있다.")
            print("✨ 당신이 그곳에서 되찾은 기억이 점차 사라진다...")
            print("🔑 하지만 당신은 생각한다.")
            print("🛎️ 기억을 잃는다 해도 자신은 절대로 멈추지 않을 것임을...")
        else:
            print("🌫️ 기억의 파편은 흩어진 채...")
            print("🌙 기억을 모두 찾지 못하여 자아가 점차 붕괴하기 시작한다...")
            print("🕳️ 그대는 무엇을 잃었는지조차 알지 못했다.")
    input("\n>> (엔터로 여정을 끝낸다.)")

def main():
    global room_x, room_y, player_px, player_py

    show_title()
    show_prologue()

    while True:
        draw_current_room()

        room = dungeon[room_y][room_x]
        # 탈출 조건 체크
        if guardian_talked and (room_x, room_y) == (9, 9) and (player_px, player_py) == ESCAPE_POS:
            zero_zero_room = dungeon[0][0]
            if zero_zero_room.self_absorbed and all_souls_talked() and memory_collected == 10:
                show_ending(hidden=True)
                break
            else:
                show_ending(hidden=False)
                break

        cmd = input("이동: W/A/S/D | 상호작용: E | 종료: Q >> ").lower()
        if cmd == 'q':
            print("게임 종료.")
            break
        elif cmd == 'e':
            handle_interaction()
        else:
            handle_movement(cmd)

if __name__ == "__main__":
    main()
