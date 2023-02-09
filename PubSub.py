from typing import NamedTuple, DefaultDict , Optional,  List
from collections import defaultdict,deque,set
import time
from sys import intern
from itertools import islice
from heapq import merge


User = str
Timestamp = float
Post = NamedTuple('Post',[('timestamp',float),('user',str),('message',str)])
posts= deque()                                                # type: deque  #Posts from newest to oldest
user_posts = defaultdict(deque)                               # type: Defaultdict[User,deque]
following  = defaultdict(set)                                 # type: Defaultdict[User,Set[User]]
followers  = defaultdict(set)                                 # type: Defaultdict[User,Set[User]]


def post_message(user:User,message:str
                    ,timestamp:Timestamp=None) ->None:
    # vietoj kekviena karta inicializavimo user, dabar reikia tik viena karta su intern, kad nebutu atskiruose dictinory ivedinejama daug kartu user
    user = intern(user)
    timestamp = timestamp or time.time()
    post = Post(timestamp,user,message)
    posts.appendleft(post)
    user_posts[user].appendleft(post)


def follow(user:User, followed_user:User)-> None: 
    user,followed_user = intern(user),intern(followed_user)
    following[user].add(followed_user)
    followers[followed_user].add(user)
    
def post_by_user(user:User,limit:Optional[int]=None)-> List[Post]: 
    return list(islice(user_posts[user],limit))

    

def post_for_user(user:User,limit:Optional[int]=None)-> List[Post]:
    #mums reikiama informacija, reikia reverse  lista kad butu pasiekiama naujausi postai
    relevent_data = merge(*[user_posts[following_users]  for following_users in following[user]],reverse=True)
    return list(islice(relevent_data,limit))


def search(phrase:str,limit:Optional[int]=None)-> List[Post]:
    #Adiing pre-indexing to speed up
    return list(islice(post for post in posts if phrase in post.text),limit)
    