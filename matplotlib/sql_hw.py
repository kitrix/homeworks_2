import sqlite3
import matplotlib.pyplot as plt

def words_table():
    conn = sqlite3.connect('hittite.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wordforms")
    results = cursor.fetchall()
    conn.close()
    conn = sqlite3.connect('hittite_new.db')
    c = conn.cursor()
    c.execute("CREATE TABLE words(id integer, Lemma text, Wordform text, Glosses text)")
    i = 0
    for res in results:
        i += 1
        c.execute("INSERT INTO words VALUES (?,?,?,?)",(i, res[0], res[1], res[2]))
    conn.commit()
    conn.close()
    return()


def glosses_table():
    conn = sqlite3.connect('hittite_new.db')
    c = conn.cursor()
    f = open('glosses.txt', 'r', encoding = 'utf-8')
    lines = f.readlines()
    gl = []
    gl_mean = []
    for l in lines:
        l2 = l.replace('\n', '')
        a = l2.split(' — ')
        gl.append(a[0])
        gl_mean.append(a[1])
    c.execute("CREATE TABLE glosses(id integer, Glosses text, Meaning text)")
    i = 0
    for g in gl:
        c.execute("INSERT INTO glosses VALUES (?,?,?)", (i+1,g,gl_mean[i]))
        i += 1
    conn.commit()
    conn.close()
    return()


def id_table():
    conn = sqlite3.connect('hittite_new.db')
    c = conn.cursor()
    c.execute("CREATE TABLE w_g_id (word_id, gloss_id integer)")
    c.execute("SELECT id, Glosses FROM words")
    wg = c.fetchall()
    for w in wg:
        gl = w[1].split('.')
        for g in gl:
            g2 = []
            g2.append(g)
            c.execute("SELECT id FROM glosses WHERE Glosses=?",(g2))
            a = c.fetchall()
            if a:
                c.execute("INSERT INTO w_g_id VALUES (?,?)", (w[0], a[0][0]))
    conn.commit()
    conn.close()
    return()

def draw_glosses():
    conn = sqlite3.connect('hittite_new.db')
    c = conn.cursor()
    c.execute("SELECT gloss_id FROM w_g_id")
    num = c.fetchall()
    id_num = {}
    for n in num:
        if n[0] in id_num:
            id_num[n[0]] += 1
        else:
            id_num[n[0]] = 1
    c.execute("SELECT id, Glosses FROM glosses")
    glosses = c.fetchall()
    gl = [] #записываются все глоссы
    n = [] #количество глосс
    
    for g in glosses:
        for i in id_num:
            if g[0] == i:
                gl.append(g[1])
                n.append(id_num[i])
    plt.bar(gl,n)
    plt.title("Все глоссы")
    plt.xlabel("Глоссы")
    plt.ylabel("Количество")
    plt.show()

    case = ['ACC','DAT','INSTR','LOC','NOM']
    case_gl = []
    case_num = []
    pos = ['ADJ','ADV','COMP','CONJ','DEM','INDEF','N','NEG','P','PART',\
           'POSS','PRON','PRV','PTCP','REL','V']
    pos_gl = []
    pos_num = []
    person = ['1PL','1SG','2PL','2SG','3PL','3SG']
    person_gl = []
    person_num = []
    v_form = ['AUX','IMP','PST','PRS']
    v_gl = []
    v_num = []
    other = ['NEG','NUM','Q','QUOT','SG','PL']
    other_gl = []
    other_num = []

    for k, gloss in enumerate(gl):
        for c in case:
            if c == gloss:
                case_gl.append(c)
                case_num.append(n[k])
        for p in pos:
            if p == gloss:
                pos_gl.append(p)
                pos_num.append(n[k])
        for per in person:
            if per == gloss:
                person_gl.append(per)
                person_num.append(n[k])
        for v in v_form:
            if v == gloss:
                v_gl.append(v)
                v_num.append(n[k])
        for o in other:
            if o == gloss:
                other_gl.append(o)
                other_num.append(n[k])

    plt.bar(case_gl, case_num)
    plt.title("Падежи")
    plt.xlabel("Глоссы")
    plt.ylabel("Количество")
    plt.show()

    plt.bar(pos_gl, pos_num)
    plt.title("Части речи")
    plt.xlabel("Глоссы")
    plt.ylabel("Количество")
    plt.show()

    plt.bar(person_gl, person_num)
    plt.title("Лицо, число")
    plt.xlabel("Глоссы")
    plt.ylabel("Количество")
    plt.show()
    conn.close()

    plt.bar(v_gl, v_num)
    plt.title("Глаголы")
    plt.xlabel("Глоссы")
    plt.ylabel("Количество")
    plt.show()
    conn.close()

    plt.bar(other_gl, other_num)
    plt.title("Другие глоссы")
    plt.xlabel("Глоссы")
    plt.ylabel("Количество")
    plt.show()
    conn.close()
    return()

def main():
    words_table()
    glosses_table()
    id_table()
    draw_glosses()
    return()


main()


                   
