import requests
import random
import json
import time
from datetime import datetime

cache_limit = 900 # 15 min in seconds


class ChanError(Exception):
    message = "Chan Error"


class BoardError(ChanError):
    def __init__(self, board):
        self.message = f"Specified board {board} could not be reached"


class ThreadError(ChanError):
    def __init__(self, post):
        self.message = f"Specified post {post} is not the OP of a thread"


class Thread:
    def __init__(self, board, number, op, img="", text=""):
        self.time = 0
        self.board = board
        self.number = number
        self.op = op
        self.img = img
        self.text = text
        self.replies = list()

    def _api(self):
        try:
            return requests.get(f"https://api.4chan.org/{self.board}/thread/{self.number}.json").text
        finally:
            time.sleep(1)

    def get_replies(self):
        if self.op is not None:
            return []
        if datetime.now().timestamp() > self.time + cache_limit and self.replies:
            return self.replies
        try:
            replies = json.loads(self._api()).get("posts")
            for reply in replies:
                r = Thread(self.board, reply.get("no"), self,
                           img=str(reply.get("tim", ""))+reply.get("ext", ""),
                           text=reply.get("com", ""))
                self.replies.append(r)
            self.time = datetime.now().timestamp()
        except KeyError as e:
            raise ThreadError(self.number)
        self.img = self.replies[0].img
        self.text = self.replies[0].text
        return self.replies

    def get_text(self):
        return self.text if self.text else self.op.text

    def get_img(self):
        img = self.img if self.img else self.op.img
        return f"https://i.4cdn.org/{self.board}/{img}"

    def get_random_reply(self):
        return random.choice(self.get_replies())


class Board:

    def __init__(self, b, title, description):
        self.board = b
        self.title = title
        self.threads = list()
        self.time = 0
        self.description = description

    def _api(self, uri):
        try:
            return requests.get(f"https://api.4chan.org/{self.board}/{uri}").text
        finally:
            time.sleep(1)

    def _add_thread(self, no):
        self.threads.append(Thread(self.board, no, None))

    def get_threads(self):
        if datetime.now().timestamp() > self.time + cache_limit and self.threads:
            return self.threads
        threads = json.loads(self._api("1.json")).get("threads")
        self.time = datetime.now().timestamp()
        for thread in threads:
            thread = thread.get("posts")[0]
            if thread.get("sticky", False): continue
            self._add_thread(thread.get("no"))
        return self.threads

    def get_random_thread(self):
        return random.choice(self.get_threads())

    def get_description(self):
        return self.description

    def get_info(self):
        return f"Title : {self.title}<br/>Description : {self.description}"


class Chan:

    boards = {}

    @staticmethod
    def _api(uri):
        try:
            return requests.get("https://api.4chan.org/" + uri).text
        finally:
            time.sleep(1)

    def get_boards(self):
        if self.boards:
            return self.boards
        boards_json = self._api("boards.json")
        boards = json.loads(boards_json)["boards"]
        for board in boards:
            b = board.get("board")
            t = board.get("title")
            m = board.get("meta_description")
            obj = Board(b,t,m)
            self.boards[b] = obj
        return self.boards

    def get_board(self, b):
        try:
            return self.get_boards().get(b)
        except KeyError:
            raise BoardError(b)

    def get_random_post(self, board=""):
        board = random.choice(list(self.get_boards().values())) if not board else self.get_board(board)
        thread = board.get_random_thread()
        post = thread.get_random_reply()
        return post
