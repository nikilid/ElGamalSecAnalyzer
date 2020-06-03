import random
import math
import base64
import time

	
def nod(a, b):
	if (b == 0):
		return (a, 1, 0)
	(d, kb, kc) = nod(b, a%b)
	return (d, kc, kb - (a // b)*kc)


def factor(q, f, time_end):
	res = []
	d = 2
	qsqrt = int(math.sqrt(q)) + 1
	while (d <= qsqrt):
		count = 0
		while (q % d == 0):
			count += 1
			q /= d
		if (count != 0):
			res.append((d, count))
		d += 1
		if (time.time() > time_end):
			f.write('    Не удалось найти факторизацию '+ str(q)+ '\n')
			return -1
	if (q > 1):
		res.append((int(q), 1))
	return res


def polig_hellman(y, g, p, tim, f):
	f.write('Метод Полига-Хеллмана\n')
	time_start = time.time()
	time_end = time_start + tim
	q = p - 1
	list_div = factor(q, f, time_end)
	if (list_div  == -1):
		return -1
	f.write('    Удалось найти факторизацию '+ str(q)+ '\n')
	size = len(list_div)
	res = [0 for i in range(size)]
	d, kc, kb = nod(g, p)
	a_inverse = kc % p
	it = 0
	for pair in list_div:
		if (pair[0] == 2):
			h = y
			b = 1
			for i in range(pair[1]):
				if (i != 0):
					st = (1 << (i - 1)) * b
					h = h*pow(a_inverse, st, p)
				if (pow(h, int(p/(1<<(i+1))), p) == 1):
					b = 0
				else:
					b = 1
				res[0] = res[0] + (1 << i)*b
				res[0] = res[0] % (1 << pair[1])
				if (time.time() > time_end):
					return -1
		else:
			h = y
			#print(it)
			table = [-1 for i in range(pair[0])]
			for j in range(pair[0]):
				table[j] = pow(g, p//pair[0]*j, p)
				if (time.time() > time_end):
					return -1
			for i in range(pair[1]):
				if (i != 0):
					st = pow(pair[0], i-1, p) * c
					h = h*pow(a_inverse, st, p)
				h_in = pow(h, p//pow(pair[0], i+1), p)
				c = 0
				for j in range(pair[0]):
					if (table[j] == h_in):
						c = j
						break
					if (time.time() > time_end):
						return -1
				res[it] = res[it] + pow(pair[0], i)*c
				res[it] = res[it] % (pow(pair[0], pair[1]))
				if (time.time() > time_end):
					return -1
		it += 1
	result = 0
	for i in range(size):
		l_m_i = pow(list_div[i][0], list_div[i][1])
		m_i = p // l_m_i
		d, kc, kd = nod(m_i, l_m_i)
		n_i = kc % l_m_i
		#print(l_m_i, m_i, n_i)
		result += res[i]*m_i*n_i
		if (time.time() > time_end):
			return -1
	f.write('    Найден ключ: ' + str(int(result % (p-1))) + '\n')
	f.write('    Время работы: ' + str(time.time() - time_start) + ' секунд\n')
	return 0





def make_s(s, time_end, f):
	#s = 2^ts
	lis = []
	log_s = int(math.log(s, 2))
	for j in range(log_s + 1):
		for r in range(s - 1, -1, -1):
			k = r + 1
			t = 0
			while ((k & 1) != 1):
				k >>= 1
				t += 1
			if (t == j):
				lis.append(r)
				break
			if (time.time() > time_end):
				return -1
	return lis

	

def pollard(y, g, p, tim, f):
	f.write('ро-метод Полларда\n')
	time_start = time.time()
	time_end = time_start + tim
	col = []
	col.append((y, 0, 1))
	h = y
	f.write('    G1: h < ' + str(p//3) + '\n' + '    G2: ' + str(p//3) + ' <= h < ' + str(p*2//3) + '\n' + '    G3: ' + str(p*2//3) + ' <= h < ' + str(p) + '\n')
	for i in range(1, p, 1):
		x = 0
		z = 1
		if (h < p//3):
			h = y*h % p
			x = col[i-1][1] % (p-1)
			z = (col[i-1][2]+1)%(p-1)
		else:
			if (h >= p//3 and h < p*2//3):
				h = h*h % p
				x = col[i-1][1]*2%(p-1)
				z = (col[i-1][2]*2)%(p-1)
			else:
				if (h >= p*2//3 and h < p):
					h = g*h % p
					x = (col[i-1][1]+1)%(p-1)
					z = col[i-1][2]%(p-1)
		col.append((h, x, z))
		s = make_s(i, time_end, f)
		if (s == -1):
			return -1
		for j in s:
			if (col[j][0] == h):
				d, kc, kb = nod(col[j][2] - z, p - 1)
				if (d == 1):
					res = (x-col[j][1])*(kc % (p-1))%(p-1)
					f.write('    Найден ключ: ' + str(int(res)) + '\n')
					f.write('    Время работы: ' + str(time.time() - time_start) + ' секунд\n')
					return 0
				else:
					d1, kc1, kb1 = nod(col[j][2] - z, (p-1)/d)
					res = (x-col[j][1])*(kc1 % ((p-1)/d))%p
					for k in range(1, d, 1):
						h = res + k*(p-1)//d
						if (pow(g, int(h%(p-1)), p) == y):
							f.write('    Найден ключ: ' + str(int(h%(p-1))) + '\n')
							f.write('    Время работы: ' + str(time.time() - time_start) + ' секунд\n')
							return 0
			if (time.time() > time_end):
				return -1
		if (time.time() > time_end):
			return -1
	return -1



def babystepgiantstep(y, g, p, tim, f):
	f.write('Большой шаг - малый шаг\n')
	time_start = time.time()
	time_end = time_start + tim
	for t in range (int(math.sqrt(p))+1, p, 1):
		f.write('    t = ' + str(t) + '\n')
		q_r = p//t + 2
		L = []
		L.append(0)
		g_in_t = pow(g, t, p)
		for q in range(1, q_r, 1):
			L.append(pow(g_in_t, q, p))
			if (time.time() > time_end):
				return -1
		#print(L)
		for r in range(1, t + 1, 1):
			g_in_r = pow(g, r, p)
			left = y*g_in_r % p
			if (time.time() > time_end):
				return -1
			for i in range(1, q_r, 1):
				if (L[i] == left):
					q_res = i
					res = (q_res*t-r)%(p-1)
					f.write('    Найден ключ: ' + str(res) + '\n')
					f.write('    Время работы: ' + str(time.time() - time_start) + ' секунд\n')
					return 0
				if (time.time() > time_end):
					return -1			
	return -1

def test_millera_rabina(n, count_round):
	if n == 2 or n == 3 :
		return True
	if (n & 1 == 0) or (n == 1):
		return False

	#представить число n - 1 = 2^{s}t
	s = 0
	t = n - 1
	while ((t & 1) != 1):
		t >>= 1
		s += 1
	for i in range(count_round):
		a = random.randint(2, n-2)
		x = pow(a, t, n)
		if (x == 1 or x == n - 1):
			continue
		for j in range(s-1):
			pow(x, 2, n)
			if (x == 1):
				return False
			if (x == n - 1):
				break
		else:
			return False
	return True

def gcd(a,b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

def gen_key(nbit, tim, f):
	time_start = time.time()
	time_end = time_start + tim
	q = 1 
	while (q < (1<<nbit) or test_millera_rabina(q+1, int(math.sqrt(q+1))) == False ):
		if (q > (1<<(nbit+1))):
			q = 1
		q *= random.choice((3,2,5,7))
		if (time.time() > time_end):
			return -1
	p = q + 1
	a = 0
	i = 2
	fact_q = factor(q, f, time.time()+30)
	#print(fact_q)
	#print(q)
	while (i < p):
		flag = 1
		for j in fact_q:
			if (pow(i, int((p-1)/j[0]), p) == 1):
				flag = 0
		if (flag):
			a = i
			break
		i += 1
		if (time.time() > time_end):
				return -1
	x = random.getrandbits(nbit)
	y = pow(a, x, p)
	f.write('Закрытый ключ: ' + str(x) + ', открытый ключ: ' + str(y) + ', образующий элемент: ' + str(a) + ', порядок группы: ' + str(p) + '\n')
	#print(x, ' ', y, ' ', p, a)
	#print(polig_hellman(y, 2, p, 20, f))
	return 0


flag1 = int(input("Выберете режим:\n1 - генерация слабого ключа (могут быть взломаны методом Полига-Хеллмана)\n2 - проверка ключа\n"))
f = open("result.txt", 'w')
if (flag1 == 1):
	nbit = int(input("Укажите размер секретного ключа в битах:\n"))
	t = int(input("Укажите максимальное время работы:\n"))
	if (gen_key(nbit, t, f) == -1):
		print("Сгенерировать ключ не удалось\n")
		f.write('Сгенерировать ключ не удалось\n')
if (flag1 == 2):
	y = int(input("Укажите открытый ключ: \n"))
	g = int(input("Укажите образующий элемент: \n"))
	p = int(input("Укажите порядок группы: \n"))
	f.write('Открытый ключ: ' + str(y) + ', образующий элемент: ' + str(g) + ', порядок группы: ' + str(p) + '\n')
	t = int(input("Укажите максимальное время работы:\n"))
	flag = int(input("Выберете алгоритм: \n1 - Большой шаг - малый шаг\n2 - ро-метод Полларда\n3 - метод Полига-Хеллмана\n4 - Все вышеперечисленные\n"))
	if (flag == 1):
		if (babystepgiantstep(y, g, p, t, f) == -1):
			f.write('    Ключ не найден \n')
	if (flag == 2):
		if (pollard(y, g, p, t, f) == -1):
			f.write('    Ключ не найден \n')
	if (flag == 3):
		if (polig_hellman(y, g, p, t, f) == -1):
			f.write('    Ключ не найден \n')
	if (flag == 4):
		t = t/3
		if (babystepgiantstep(y, g, p, t, f) == -1):
			f.write('    Ключ не найден \n')
		if (pollard(y, g, p, t, f) == -1):
			f.write('    Ключ не найден \n')
		if (polig_hellman(y, g, p, t, f) == -1):
			f.write('    Ключ не найден \n')
f.close()





