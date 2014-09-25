#-*- coding:utf-8 -*-
import math

def fun(x):
	#return (x+5)*(x+5)-5;
	#return math.e**x-100+x
	#return 2*x+x**2-1000
	return x**3+2*x

def f1(startx, ratio):
	small=0.000001
	delta = 0.01;
	curx = startx;
	prey = 0;
	count = 0;
	while True:
		cury = fun(curx)
		if abs(cury-prey)<=small:
			break;
		g=(fun(curx+delta)-fun(curx-delta))/(2*delta)
		curx = curx-g*ratio
		prey = cury
		count += 1
		print "count:\t"+str(count)
		print "curx is\t"+str(curx)
		print "g is \t"+str(g)
		print "cury is \t" + str(cury)
		print "prey is \t" + str(prey)

	print "jizhidian at\t"+str(curx)

#x(n+1)=x(n)£­f(x(n))/f'(x(n))
def f2(startx, ratio):
	small=0.000001
	delta = 0.001;
	curx = startx;
	prey = 0;
	count = 0;
	while True:
		cury = fun(curx)
		if abs(cury)<=small:
			break;
		g=(fun(curx+delta)-fun(curx-delta))/(2*delta)
		#curx = curx-cury/g
		curx = curx-g/g2(curx)
		prey = cury
		count += 1
		print "count:\t"+str(count)
		print "curx is\t"+str(curx)
		#print "g is \t"+str(g)
		#print "cury is \t" + str(cury)
		#print "prey is \t" + str(prey)
	#print "root at\t"+str(curx)
	return curx



def g2(curx):
	delta = 0.01
	g1 = (fun(curx+delta+delta)-fun(curx))/(2*delta)
	g2 = (fun(curx)-fun(curx-2*delta))/(2*delta)
	rst = (g1-g2)/(2*delta)
	rst = 6*curx
	print "gpp="+str(rst)
	return rst

f2(0.5, 0.1)

import os
os.system("pause")
