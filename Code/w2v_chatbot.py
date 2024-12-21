import numpy as np
import pandas as pd
import gensim
from underthesea import word_tokenize
import string
from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity
import json
import os 
os.chdir('../Dataset/') # data path

class W2VChatBot:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.dataset_vectors = []
        self.answers = None
        self.size = 0

    def load_model(self, model_path='baomoi.model.bin'):
        if not os.path.exists(model_path) or not os.path.isfile(model_path):
          print('Model not found')
          return False
        self.model  = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
        self.tokenizer = word_tokenize
        print('W2V: Load model successfully')
        return True

    def load_answer(self, data_path='normal_gf_excel.xlsx'):
        if not os.path.exists(data_path) or not os.path.isfile(data_path):
            print('Answer not found')
        if data_path.endswith('.json'):
            print('Json file Detected')
            data = self.read_json_file(data_path)
            self.answers = np.array([item['answer'] for item in data])
        else:
            data = pd.read_excel(data_path, dtype=str)
            self.answers = data['answer'].values   
        self.size = len(self.answers)
        print(self.answers[:5])

    def response(self, input):
        # input_embedding = self.doc_embedding(input)
        input_embedding = self.w2v_embedding(input)
        
        # Compute cosine similarity between input sentence and each sentence in the list
        similarities = [self.similarity_score(input_embedding, embedding) for embedding in self.dataset_vectors]
        most_similar_idx = np.argmax(similarities)
        max_score = similarities[most_similar_idx]

        if (max_score <= 0.5):
            return -1, 'Em không biết trả lời như thế nào', max_score
        
        return most_similar_idx, self.answers[most_similar_idx], max_score
        # return self.answers[most_similar_idx]
    
    #  ----------  Word2Vex ------------
    def tokenize(self, text, stop_w=['vậy', 'khi', 'có thể', 'nào', 'sẽ', 'gì', 'có', 'rồi']):
        punctuation = string.punctuation + '–' + '“' + '”' + '‘' + '’'
        text = " ".join(text.split())
        print()
        tokens = self.tokenizer(text)
        tokens = [w for w in tokens if w not in punctuation] #Remove punction
        tokens = [word.lower() for word in tokens] #Lower text
        tokens = [w for w in tokens if w not in stop_w] #Remove stop words
        # print(tokens)
        return tokens

    def w2v_embedding(self, doc):
        tokens = self.tokenize(doc)
        if tokens == []:
            return []
        word_vectors = []
        for w in tokens:
          if w not in self.model:
              continue
          else:
              word_vectors.append(self.model[w])
        doc_vector = np.mean(word_vectors, axis=0)
        return doc_vector

    # ----------- Support functions -----------
    def similarity_score(self, vetor1, vetor2):
        similarity = cosine_similarity([vetor1], [vetor2])
        return similarity[0][0]

    def read_json_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:  # Specify encoding for potential special characters
            data = json.load(f)
        return data

    # ----------- Load Data (2 way) -----------
    def load_dataset(self, data_path, n=None, file_name='dataset_vectors'):
        if not os.path.exists(data_path) or not os.path.isfile(data_path):
              print('Answer not found')
        if data_path.endswith('.json'):
              print('Json file Detected')
              data = self.read_json_file(data_path)
              questions = np.array([item['question'] for item in data])
              self.dataset_vectors = [self.w2v_embedding(q) for q in questions]
        elif data_path.endswith('.xlsx'):
              print('Excel file Detected')
              data = pd.read_excel(data_path, dtype=str)
              questions = data['question'].values
              self.dataset_vectors = [self.w2v_embedding(q) for q in questions]
        else:
              print('CSV file Detected')
              data = pd.read_csv(data_path, dtype=str)
              questions = data['question'].values
              self.dataset_vectors = [self.w2v_embedding(q) for q in questions]

        if n is None:
            n = len(questions)

        # for i in range(n):
        #     self.dataset_vectors.append(self.doc_embedding(questions[i]))

        self.dataset_vectors = np.array(self.dataset_vectors)
        self.size = n
        np.save(file_name+'.npy', self.dataset_vectors)
        print('Import Done')
        return True

    def load_data_from_npy(self, npy_path='dataset_vectors.npy'):
        if not os.path.exists(npy_path):
            print('File npy not found')
            return False
        self.dataset_vectors = np.load(npy_path)
        # df = pd.read_excel(data_path, header=None, skiprows=1)
        self.size = len(self.dataset_vectors)
        print('Import Done')
        return True
    
if __name__ == '__main__':
    bot = W2VChatBot()
    model_path = 'baomoi.model.bin'
    data_path = 'Tsundere_bot.json'
    bot.load_model()
    bot.load_answer(data_path)
    # bot.load_dataset(data_path, file_name='w2v_tsun_bot')
    bot.load_data_from_npy(npy_path='w2v_tsun_bot.npy')

    print(bot.response('Em là ai?'))
    # print(bot.response('Mày ngu quá'))
    print(bot.response('Em đang làm gì vậy'))
    print(bot.response('Em có thích anh không?'))
    print(bot.response('Anh cô đơn quá'))
    print(bot.response('Em có thích chơi game không'))
    print(bot.response('Em muốn tặng quà không'))
    print(bot.response('Đồ ngu ngốc'))
