import bisect
import math
import csv
import sys

class Node:
    def __init__(self, isleaf, nxt, parent, degree, file):
        self.key = []
        self.value = []
        self.isleaf = isleaf
        self.next = nxt
        self.parent = parent
        self.child = []
        self.degree = int(degree)
        self.file = file

    def insert(self, key, value, skip):
        while self.parent != None and skip == 0:#skip==1일땐 아래 skip
            self = self.parent
        if self.isleaf == 1:
            #if key in self.key == False:
            index = bisect.bisect_left(self.key, key)
            self.key.insert(index, key)
            self.value.insert(index, value)
            if len(self.key) >= self.degree:
                mid = math.floor(self.degree/2)
                self.split(mid)
                self = self.parent
        else:
            index = bisect.bisect_left(self.key, key)
            self = self.child[index]
            self.insert(key, value, 1)

    def insertNode(self, key, child):
        index = bisect.bisect_left(self.key, key)
        self.key.insert(index, key)
        self.child.insert(index+1, child)
        if len(self.key) >= self.degree:
            mid = math.floor(self.degree/2)
            self.split(mid)
            
    def split(self, mid):
        if self.isleaf == 1:
            new = Node(1, self.next, self.parent, self.degree, file)
            new.key = self.key[mid:]
            new.value = self.value[mid:]
            self.key = self.key[:mid]
            self.value = self.value[:mid]
            self.next = new
            
            if self.parent == None:
                self.parent = Node(0, None, None, self.degree, file)
                self.parent.key.append(new.key[0])
                self.parent.child.append(self)
                self.parent.child.append(new)
                new.parent = self.parent
            else:
                self.parent.insertNode(new.key[0], new)
        else:
            new = Node(0, self.next, self.parent, self.degree, file)
            up = self.key[mid]
            new.key = self.key[mid+1:]
            new.child = self.child[mid+1:]
            i = 0
            while i < len(new.child):
                new.child[i].parent = new
                i = i + 1
            self.key = self.key[:mid]
            self.child = self.child[:mid+1]
            self.next = new
            
            if self.parent == None:
                self.parent = Node(0, None, None, self.degree, file)
                self.parent.key.append(up)
                self.parent.child.append(self)
                self.parent.child.append(new)
                new.parent = self.parent
            else:
                self.parent.insertNode(up, new)

    def read(self, line):
        with open(self.file, "r") as f:
            i = 1
            while i < line:
                skip = f.readline()
                i = i+1
            read_line = f.readline()#line 번째 줄 읽기
            if not read_line:
                return
            read_line = read_line.rstrip("\n")
            if "leaf:" in read_line:
                read_line = read_line.lstrip("leaf:")
                read_line = read_line.rstrip()
                node = read_line.split(" -> ")
                save = self
                for i in node:
                    key = i.split(" ")
                    for k in key:
                        self.key.append(int(k))
                    if self.next != None:
                        self = self.next
                self = save
                self.read(line+1)

            elif "value:" in read_line:
                read_line = read_line.lstrip("value:")
                read_line = read_line.rstrip()
                node = read_line.split(" | ")
                for i in node:
                    value = i.split(" ")
                    for v in value:
                        self.value.append(int(v))
                    if self.next != None:
                        self = self.next

            else:
                read_line = read_line.rstrip(" / ")
                node = read_line.split(" / ")
                pre = None
                for i in node:
                    key = i.split(" ")
                    for k in key:
                        self.key.append(int(k))
                        new = Node(1, None, self, self.degree, self.file)
                        self.child.append(new)
                        if pre != None:
                            pre.next = new
                        pre = new
                    new = Node(1, None, self, self.degree, self.file)
                    self.child.append(new)#key 개수 +1개만큼 child노드 만들기
                    pre.next = new
                    pre = new
                    
                    self.isleaf = 0
                    if self.next != None:
                        self = self.next
                i = 0
                while self.parent != None:
                    self = self.parent
                    i = i+1
                while i > 0:
                    self = self.child[0]
                    i = i-1
                    
                self = self.child[0]
                self.read(line+1)
                        

    def write(self):
        index = open(self.file, "w")
        sys.stdout = index
        print("degree : " + degree)
        while self.parent != None:#root까지 올라가기
            self = self.parent
            
        while self.isleaf != 1:
            down = self.child[0]#내려갈 시작점
            while self != None:
                for i in self.key:
                    print(str(i), end = " ")#한 노드에 속한 키 출력
                print("/", end = " " )#'/' 로 노드 구별
                self = self.next
            print("")#"\n"으로 level 구별
            self = down
            
        #leaf노드 출력
        start = self
        print("leaf:", end = "")
        while self != None:
            for k in self.key:
                print(str(k), end = " ")
            if self.next != None:
                print("->", end = " ")
            self = self.next
        print("")
        self = start
        print("value:", end = "")
        while self != None:
            for v in self.value:
                print(str(v), end = " ")
            if self.next != None:
                print("|", end = " ")
            self = self.next
        print("")


    def key_search(self, key, skip):
        while self.parent != None and skip == 0:#skip==1일때 아래줄 skip
            self = self.parent
        if self.isleaf == 1:
            if key in self.key:
                index = bisect.bisect_left(self.key, key)
                print(str(self.value[index]))
            else:
                print("NOT FOUND")

        else:
            for i in self.key:
                if i == self.key[len(self.key)-1]:
                    print(str(i), end = "")
                else:
                    print(str(i), end = ",")
            print("")
            index = bisect.bisect_left(self.key, key)
            if index <= (len(self.key)-1) and self.key[index] == key:
                index = index + 1
            self = self.child[index]
            self.key_search(key, 1)

    def range_search(self, start, end):
        while self.parent != None:
            self = self.parent
        while self.isleaf != 1:
            self = self.child[0]

        while self != None:
            v = 0
            for i in self.key:
                if int(i) >= start and int(i) <= end:
                   print(str(i) + "," + str(self.value[v]))
                v = v+1
            self = self.next
        
    def delete(self, key):
        need_del = None
        left_sibiling = None
        while self.parent != None:
            self = self.parent
        while self.isleaf != 1:
            index = bisect.bisect_left(self.key, key)
            if index <= (len(self.key)-1) and self.key[index] == key:
                index = index + 1
                need_del = self#leaf 아닌 곳에도 key가 있는지 확인
                del_index = index - 1
            if index > 0:
                left_sibiling = self.child[index-1]
            else:
                left_sibling = None
            self = self.child[index]
            p_index = index

        d_index = bisect.bisect_left(self.key, key)
        del(self.key[d_index])
        del(self.value[d_index])
        if need_del != None:
            need_del.key[del_index] = self.key[d_index]

        while True:
            if len(self.key) >= math.floor((self.degree-1)/2):#key개수 충분한 경우
                break
            else:
                #오른쪽에서 borrow
                if index < len(self.parent.key) and len(self.next.key) > math.floor((self.degree-1)/2):
                    b1 = self.parent.key[p_index]
                    self.key.append(b1)
                    if self.isleaf == 1:
                        self.value.append(self.next.value[0])
                        del(self.next.value[0])
                        del(self.next.key[0])
                        self.parent.key[p_index] = self.next.key[0]
                    else:
                        self.child.append(self.next.child[0])
                        self.next.child[0].parent = self
                        self.parent.key[p_index] = self.next.key[0]
                        del(self.next.key[0])
                        del(self.next.child[0])
                    break

                #왼쪽에서 borrow
                elif left_sibiling != None and len(left_sibiling.key) > math.floor((self.degree-1)/2):
                    s_index = len(left_sibiling.key)-1
                    if self.isleaf == 1:
                        self.key.insert(0, left_sibiling.key[s_index])
                        self.value.insert(0, left_sibiling.value[s_index])
                        del(left_sibiling.key[s_index])
                        del(left_sibiling.value[s_index])
                        self.parent.key[p_index-1] = self.key[0]
                    else:
                        b1 = self.parent.key[p_index-1]
                        self.key.insert(0, b1)
                        self.child.insert(0, left_sibiling.child[s_index+1])
                        self.child[0].parent = self
                        self.parent.key[p_index-1] = left_sibiling.key[s_index]
                        del(left_sibiling.key[s_index])
                        del(left_sibiling.child[s_index+1])
                    break

                #merge
                else:                      
                    #오른쪽 노드랑 merge
                    if index < len(self.parent.key):
                        self.key = self.key + self.next.key
                        self.value = self.value + self.next.value
                        self.next.key = None
                        self.next.value = None
                        self.next = self.next.next
                        del(self.parent.key[p_index])
                        del(self.parent.child[p_index+1])

                    #왼쪽 노드랑 merge
                    else:
                        left_sibiling.key = left_sibiling.key + self.key
                        left_sibiling.value = left_sibiling.value + self.value
                        self.key = None
                        self.value = None
                        left_sibiling.next = self.next
                        del(self.parent.key[p_index-1])
                        del(self.parent.child[p_index])
                        
                    self = self.parent
                    if self.parent == None:
                        break
                    p_index = bisect.bisect_left(self.parent.key, self.key[0])
                    index = p_index
                    if p_index > 0:
                        left_sibiling = self.parent.child[p_index-1]
                    else:
                        left_sibiling = None

#파일 만들기
if(sys.argv[1] == "-c"):
    f = open(sys.argv[2], "w")
    degree = sys.argv[3]
    sys.stdout = f
    print("degree : " + degree)
    f.close()

#삽입하기
elif(sys.argv[1] == "-i"):
    #기존 index 파일에서 degree 읽어오기
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    
    pair = {}
    with open(sys.argv[3], "r") as file:
        file_read = csv.reader(file)
        for line in file:
            pair_list = line.split(',')
            pair[int(pair_list[0])] = int(pair_list[1])

    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)#기존 노드 읽어오기
    for key in pair:
        root.insert(key, pair[key], 0)
    root.write()

#삭제하기
elif(sys.argv[1] == "-d"):
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)
    
    delete = []
    with open(sys.argv[3], "r") as file:
        file_read = csv.reader(file)
        for line in file:
            delete.append(int(line))
    for d in delete:
        root.delete(d)
    root.write()

#단일 검색하기
elif(sys.argv[1] == "-s"):
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    search_key = int(sys.argv[3])
    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)
    root.key_search(search_key, 0)#함수내부에서 출력
    
#범위 검색하기
elif sys.argv[1] == "-r":
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)
    root.range_search(start, end)#함수내부에서 출력
