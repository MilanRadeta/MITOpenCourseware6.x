# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import requests
import string
import time
import threading
from project_util import translate_html, is_sublist
from mtTkinter import *
from datetime import datetime
import pytz
import xml.etree.ElementTree as ET


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def build_item_dict(item):
    result = {}
    keys = ['guid', 'title', 'link', 'description', 'pubDate']
    for key in keys:
        elem = item.find(key)
        result[key] = elem.text if elem is not None else ''
    return result


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    response = requests.get(url)
    root = ET.fromstring(response.content)
    ret = []
    for entry in root.findall('channel/item'):
        dict = build_item_dict(entry)
        guid = dict['guid']
        title = translate_html(dict['title'])
        link = dict['link']
        description = translate_html(dict['description'])
        pubdate = translate_html(dict['pubDate'])

        try:
            pubdate = datetime.strptime(pubdate, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2


class PhaseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text = text.lower()
        for punctuation in string.punctuation:
            text = text.replace(punctuation, ' ')
            text = text.replace('  ', ' ')
        text_words = text.split()
        phrase_words = self.phrase.split()
        return is_sublist(text_words, phrase_words)

# Problem 3


class TitleTrigger(PhaseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.title)

# Problem 4


class DescriptionTrigger(PhaseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.description)

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.


class TimeTrigger(Trigger):

    time_format = "%d %b %Y %H:%M:%S"

    def __init__(self, time):
        time = datetime.strptime(time, TimeTrigger.time_format)
        self.time = time

# Problem 6


class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.pubdate
        pubdate = pubdate.replace(tzinfo=None)
        return pubdate < self.time


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.pubdate
        pubdate = pubdate.replace(tzinfo=None)
        return pubdate > self.time


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8


class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9


class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    result = []
    for story in stories:
        for trigger in triggerlist:
            if (trigger.evaluate(story)):
                result.append(story)
                break

    return result


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines)  # for now, print it so you see what it contains!


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        # triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
