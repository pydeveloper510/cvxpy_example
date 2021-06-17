# import lib
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# set initial data
price_a = np.full(12, 325.)
price_b = np.array([300, 300, 290, 275, 275, 280, 260, 250, 230, 200, 210, 190.])
price_c = np.array([100, 110, 98, 115, 200, 220, 210, 500, 500, 490, 487, 550.])

total_profit = 0

a_month_cnt = []
b_month_cnt = []
c_month_cnt = []
per_profit = []
# get every month product cnt and profit from initial data 
for i in range(0, 12):
    # set variable
    a = cp.Variable()
    b = cp.Variable()
    c = cp.Variable()

    # get every month profif of each model
    p_a = price_a[i]
    p_b = price_b[i]
    p_c = price_c[i]
    print('_____ ' + str(i+1) + ' _____')
    # print(p_a)
    # print(p_b)
    # print(p_c)

    if i > 5:
        # set condition second half of year
        constraints = [
            a >= 2000,
            b >= 2000,
            c >= 2000,
            b <= 4500,
            c <= 5000,
            a + b + c <= 10000,
        ]
    else:
        # set condition first half of year
        constraints = [
            a >= 2000,
            b >= 2000,
            c >= 2000,
            a <= 4000,
            b <= 4500,
            a + b + c <= 10000,
        ]

    # set problem
    obj = cp.Maximize(p_a * a + p_b * b + p_c * c)
    prob = cp.Problem(obj, constraints)
    
    # solve
    prob.solve()

    # result (every month product cnt)
    a_cnt = round(float(a.value))
    b_cnt = round(float(b.value))
    c_cnt = round(float(c.value))

    # set per month cnt 
    a_month_cnt.append(a_cnt)
    b_month_cnt.append(b_cnt)
    c_month_cnt.append(c_cnt)

    print("Status:", prob.status)
    print("Result value:", a.value, b.value, c.value)
    print("Result round value:", a_cnt, b_cnt, c_cnt)

    # this month profit 
    profit = p_a * a_cnt + p_b * b_cnt + p_c * c_cnt
    per_profit.append(profit)
    print(str(i + 1) + " profit: " +  str(profit))
    total_profit += profit

print("Total Profit : " +  str(total_profit))

# for draw graph change list to tuple
a_data = tuple(a_month_cnt)
b_data = tuple(b_month_cnt)
c_data = tuple(c_month_cnt)
profit_data = tuple(per_profit)

list_a_b_data = []

# set a+b data for graph
for i in range(0, 12):
    _a =list(a_data)
    _b =list(b_data)
    _c = _a[i] + _b[i]
    list_a_b_data.append(_c)

# set a + b data set
a_b_data = tuple(list_a_b_data)

#set fig and ax1, ax2
fig, (ax1, ax2) = plt.subplots(2, 1)
N = 13
ind = np.arange(1, N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence
p1 = ax1.bar(ind, a_data, width, label="A")
p2 = ax1.bar(ind, b_data, width, bottom=a_data, label="B")
p3 = ax1.bar(ind, c_data, width, bottom=a_b_data, label="C")
#graph setting ax1
ax1.axhline(0, color='grey', linewidth=0.8)
ax1.set_ylabel('Product count')
ax1.set_title('Each product count per month')
ax1.set_xticks(ind)
ax1.set_yticks(np.arange(0, 13000, 2000))
ax1.legend((p1[0], p2[0], p3[0]), ('A', 'B', 'C'))
# Label with label_type 'center' instead of the default 'edge'
ax1.bar_label(p1, label_type='center')
ax1.bar_label(p2, label_type='center')
ax1.bar_label(p3, label_type='center')
ax1.bar_label(p3)
# profit graph setting ax2
ax2.set_title('Profit per month')
ax2.set_ylabel('Profit')
ax2.set_xticks(ind)
p_1 = ax2.bar(ind, profit_data, width, label="Per profit")
ax2.bar_label(p_1)
# draw graph
plt.show()