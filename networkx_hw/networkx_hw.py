import networkx as nx
import sys
import gensim, logging
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
G = nx.Graph()
m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
model.init_sims(replace=True)
words = ['разговаривать_VERB', 'докладывать_VERB', 'беседовать_VERB', 'общаться_VERB', 'говорить_VERB',\
         'рассказывать_VERB', 'болтать_VERB', 'трепаться_VERB', 'сообщать_VERB']

for i, word in enumerate(words):
    G.add_node(word, label=word)
for i, word in enumerate(words):
    if word in model:
        if i + 1 < len(words):
            for j in range (i+1, len(words)):
                if words[j] in model:
                    if model.similarity(word, words[j])> 0.5:
                        G.add_edge(word, words[j])
    else:
        print(word + ' is not present in the model')

#центральные слова графа
deg = nx.degree_centrality(G)
print('центральность узлов (в порядке убывания):')
for nodeid in sorted(deg, key=deg.get, reverse=True):
    print(nodeid)

print('радиус графа: ', nx.radius(G))
print('коэффициент кластеризации: ', nx.average_clustering(G))

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='green', node_size=20)
nx.draw_networkx_edges(G, pos, edge_color='blue')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
plt.axis('off')
plt.show()