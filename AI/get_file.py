import paramiko
import json
import time
from predict import *
from similarity.Similarity import *

hostname = '114.115.130.106'
port = 22
username = 'root'
password = 'Buaa2019'

curr_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

remote_path = "/data/topics.json"
remote_all_path = "/data/alltopics.json"

local_path = r"./%s.json" % curr_time
local_all_path = r"./%s_all.json" % curr_time

# local_path = "2019-06-02_all.json"
# local_all_path = "2019-06-01.json"

new_local_path = r"./%s_new.json" % curr_time
new_local_similar = r"./%s_all_new.json" % curr_time

new_remote_path = "/data/new.json"
new_remote_similar = "/data/_new.json"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password, compress=True)
sftp_client = client.open_sftp()

def get_remote_file():
    try:
        sftp_client.get(remote_path, local_path)
        # return 1
    except IOError:
        print("something wrong about the remote topics.json")
        return -1

    try:
        sftp_client.get(remote_all_path, local_all_path)
        return 1
    except IOError:
        print("something wrong about the remote alltopics.json")
        return -1


def dump_to_remote():
    # transfer to remote server
    sftp_client.put(new_local_path, new_remote_path)
    sftp_client.put(new_local_similar, new_remote_similar)

def classify_emotion():
    new_comment_file = open(local_path, 'r', encoding='utf-8')

    try:
        raw_data = json.load(new_comment_file)
        new_data = []
        new_question = []
        for new_entry in raw_data:
            new_comment = new_entry['title'] + new_entry['content']
            classified = get_classification([new_comment])
            # classify into question or comment
            new_entry['emotion'] = 0
            # get emotion label
            if classified[0] == 'comment':
                emotion = get_emotion([new_comment])
                new_entry['emotion'] = emotion[0]
                new_entry['classification'] = 0
            elif classified[0] == 'question':
                # create list of new question
                new_entry['classification'] = 1
                selected = {}
                selected["id"] = new_entry["id"]
                selected["title"] = new_entry["title"]
                new_question.append(selected)
                # print(new_question)
            # add to new json dict
            new_data.append(new_entry)
        # dump to a local json file
        new_local_file = open(new_local_path, 'w', encoding='utf-8')
        json.dump(new_data, new_local_file, ensure_ascii=False, indent=4)
        new_local_file.close()
        new_comment_file.close()
        # return 1
        return new_question
    except KeyError:
        print("key error occurred")
        new_comment_file.close()
        # return -1
        return None

def get_similarity(new_question):
    # print(new_question)
    all_question_file = open(local_all_path, 'r', encoding='utf-8')
    all_question = []

    try:
        for all_entry in new_question:
            all_question.append(all_entry)
        # print(all_question)
        raw_data = json.load(all_question_file)
        # print(raw_data)
        for all_entry in raw_data:
            new_entry = {}
            new_entry['id'] = all_entry["id"]
            new_entry["title"] = all_entry["title"]
            all_question.append(new_entry)

        # print(all_question)
        simi_model = Similarity_function('./similarity/hlp_stop_words.txt', all_question)
        # print(new_question)
        all_simi = []
        for all_entry in new_question:
            if all_entry["title"] == "":
                all_entry["similar"] = []
            else:
                all_entry["similar"] = simi_model.getmostsimilar(all_entry["id"], all_entry["title"])["similar"]
            all_simi.append(all_entry)

        # print(all_simi)

        new_local_file = open(new_local_similar, 'w', encoding='utf-8')
        json.dump(all_simi, new_local_file, ensure_ascii=False, indent=4)
        new_local_file.close()

    except KeyError:
        print("key error occurred")
    finally:
        all_question_file.close()

if __name__ == "__main__":
    '''
    ret_new_question = classify_emotion()
    dump_to_remote()
    # get_similarity(ret_new_question)
    '''
    if get_remote_file() > 0:
        # get_similarity([])
        ret_new_question = classify_emotion()
        if ret_new_question is not None:
            get_similarity(ret_new_question)
            dump_to_remote()
            print("yep!")
    # '''
