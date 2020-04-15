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

class PostError(ChanError):
    def __init__(self, post, thread):
        self.message = f"Specified post {post} is not a post of thread {thread}"


class Thread:
    def __init__(self, board, number, op, img="", text=""):
        self.time = 0
        self.board = board
        self.number = number
        self.op = op
        self.img = img
        self.text = text
        self.replies = dict()

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
                self.replies[reply.get("no")] = r
            self.time = datetime.now().timestamp()
        except KeyError as e:
            raise ThreadError(self.number)
        self.img = self.replies[self.number].img
        self.text = self.replies[self.number].text
        return self.replies

    def get_text(self):
        return self.text if self.text else self.op.text

    def get_img(self):
        img = self.img if self.img else self.op.img
        return f"https://i.4cdn.org/{self.board}/{img}"

    def get_random_reply(self):
        return random.choice(list(self.get_replies().values()))

    def get_reply(self, no):
        try:
            return self.get_replies()[no]
        except KeyError as e:
            raise PostError(no, self.number)

    def get_uri(self):
        op_n = self.number if not self.op else self.op.number
        return f"{self.board} {op_n} {self.number}"


class Board:

    def __init__(self, b, title, description):
        self.board = b
        self.title = title
        self.threads = dict()
        self.time = 0
        self.description = description

    def _api(self, uri):
        try:
            return requests.get(f"https://api.4chan.org/{self.board}/{uri}").text
        finally:
            time.sleep(1)

    def _add_thread(self, no):
        self.threads[no] = (Thread(self.board, no, None))

    def get_threads(self):
        if datetime.now().timestamp() > self.time + cache_limit and self.threads:
            return self.threads
        threads = []
        for page in json.loads(self._api("threads.json")):
            threads += page.get("threads")
        self.time = datetime.now().timestamp()
        for thread in threads:
            if thread.get("sticky", False): continue
            self._add_thread(thread.get("no"))
        return self.threads

    def get_random_thread(self):
        return random.choice(list(self.get_threads().values()))

    def get_thread(self, no):
        try:
            return self.get_threads()[no]
        except KeyError as e:
            raise ThreadError(no)

    def get_description(self):
        return self.description

    def get_info(self):
        return f"Title : {self.title}<br/>Description : {self.description}"

    def get_summary(self):
        return f"/{self.board}/ {self.title}"


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
            return self.get_boards()[b]
        except KeyError:
            raise BoardError(b)

    def get_post(self, board="", thread="", post=""):
        if not board:
            board = random.choice(list(self.get_boards().values()))
        else:
            board = self.get_board(board)
        if not thread:
            thread = board.get_random_thread()
        else:
            thread = board.get_thread(int(thread))
        if not post:
            return thread.get_random_reply()
        elif post == "op":
            return thread.get_reply(thread.number)
        else:
            return thread.get_reply(int(post))

    def get_info(self, board=""):
        if board:
            return self.get_board(board).get_info()
        else:
            return "<br/>".join(map(lambda b: b.get_summary(), self.get_boards().values()))
