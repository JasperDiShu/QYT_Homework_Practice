# 2020.03.10-Homework-test for

# 方案一：不用函数解决
list1 = ['aaa', 111, (4, 5), 2.01]
list2 = ['bbb', 333, 111, 3.14, (4, 5)]

print('方案一：不用函数解决')
List_same = []
List1_only = []
for x in list1:
    if (x in list2):
        List_same.append(x)
    else:
        List1_only.append(x)
for z in List1_only:
    print('%s only in List1' % str(z))
    List1_only.remove(z)
for y in List_same:
    print('%s in List1 and List2' % str(y))
for z in List1_only:
    print('%s only in List1' % str(z))

print('\n')

# 方案二：修改为函数的更加通用的方案

def find_same_string(List1, List2):
    print('方案二：修改为函数的更加通用的方案')
    List_same = []
    List1_only = []
    for x in List1:
        if (x in List2):
            List_same.append(x)
        else:
            List1_only.append(x)
    for z in List1_only:
        print('%s only in List1' % str(z))
        List1_only.remove(z)
    for y in List_same:
        print('%s in List1 and List2' % str(y))
    for z in List1_only:
        print('%s only in List1' % str(z))

if __name__ == '__main__':
    list1 = ['aaa', 111, (4, 5), 2.01]
    list2 = ['bbb', 333, 111, 3.14, (4, 5)]
    find_same_string(list1, list2)