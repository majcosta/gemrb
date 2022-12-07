#!/usr/bin/python3
# GemRB - Infinity Engine Emulator
# Copyright (C) 2009 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

# This generates a formatio.2da file for GemRB, because it was becoming
# far too tedious to do this by hand. The output files have pairs of
# coordinates in the order of the party members.

# Run it as 'make_formation.py bg2 > override/bg2/formatio.2da' or similar.

# written (badly, sorry!) by fuzzie, feb 2nd 2009

# TODO: older games have focus points in different positions and different
# spacing (ie, coordinates have different offsets)
# eg, pst seems to usually have the focus point always on the lead char

import math

num_coords = 20

def print_y(y, i):
	end = " "
	if i == (num_coords - 1):
		end = ""
	print(y, end=end)


def generate_header():
	print("2DA V1.0")
	print("-10")
	print("# generated by make_formation.py, do not edit")

	print("", end=' ')
	for i in range(num_coords):
		print("X" + str(i + 1), end=' ')
		print_y("Y" + str(i + 1), i)
	print()

# A simple spaced line formation.
def generate_line(name):
	print(name, end=' ')
	yloc = 0
	for i in range(num_coords):
		print(0, end=' ')
		print_y(yloc, i)
		yloc += 36
	print()

# A 'T' shape formation, with 3 actors at the front.
def generate_t():
	print("T", end=' ')
	for i in range(num_coords):
		if i == 0:
			# centre
			print("0 0", end=' ')
		elif i == 1:
			# right
			print("48 0", end=' ')
		elif i == 2:
			# left
			print("-48 0", end=' ')
		elif i == 3:
			# first line member (48 deeper)
			print("0 48", end=' ')
		else:
			# line member (36 deeper)
			print(0, end=' ')
			print_y(48 + ((i - 3) * 36), i)
	print()

# A 'gathered' formation around a centre point.
def generate_gather():
	print("GATHER", end=' ')
	for i in range(num_coords):
		if i == 0:
			xloc = 0 # centre
			yloc = -36 # front
		elif i == 1:
			xloc = 48 # right
			yloc = -24
		elif i == 2:
			xloc = -48 # left
			yloc = -24
		elif i % 3 == 0:
			xloc = 48 # right
			yloc = 24 * i // 3
		elif i % 3 == 1:
			xloc = -48 # left
			yloc = 24 * (i - 1) // 3
		else:
			xloc = 0 # centre
			yloc = 12 + 24 * (i - 2) // 3
		print(xloc, end=' ')
		print_y(yloc, i)
	print()

# A block formation which places 4 on a row - first two in the 
# middle (left then right), then two on the outside (left then right).
# With a party size of 6 this results in 4 on the first row and 2 on the
# second, hence the name.
def generate_4and2():
	print("4AND2", end=' ')
	for i in range(num_coords):
		if i % 4 == 0:
			xloc = 0
		elif i % 4 == 1:
			xloc = 64
		elif i % 4 == 2:
			xloc = -64
		else:
			xloc = 128
		yloc = (i // 4) * 48
		print(xloc, end=' ')
		print_y(yloc, i)
	print()

# A wavy-line formation.
def generate_s(bg2style):
	print("S", end=' ')
	for i in range(num_coords):
		# x coordinate: +/- 15 for bg2, 0/64 otherwise
		if i % 2 == 0:
			if bg2style: print(15, end=' ') # on right
			else: print(0, end=' ') # on left
		else:
			if bg2style: print(-15, end=' ') # on left
			else: print(64, end=' ') # on right
		
		# y coordinate: 24 each
		print_y(i * 24, i)
	print()

# Returns the position in a formation of party member 'actorno',
# if the lead character must be in position 'leadpos'.
def corrected_position_for_actor(actorno, leadpos):
	if actorno == 0: # lead
		return leadpos
	elif actorno < leadpos + 1: # in front of lead
		return actorno - 1
	else: # behind lead (normal position)
		return actorno

# A wavy-line formation, with the lead character in the 4th position and
# the other characters in order (even if this leaves spaces!).
def generate_wavyline():
	print("WAVYLINE", end=' ')
	for i in range(num_coords):
		pos = corrected_position_for_actor(i, 3)

		# x coordinate: +/- 15
		if pos % 2 == 0:
			print(15, end=' ') # on right
		else:
			print(-15, end=' ') # on left
		
		# y coordinate: 24 each
		print_y(pos * 24, i)
	print()

# A formation surrounding the main character. The next character goes
# at the front, then one left, then one right, then the next left/right
# at the back, then other characters trail behind the main one (it goes
# completely chaotic in real BG2, apparently).
def generate_protect():
	rad = 68 # radius
	degrees_step = 72 # 360 / 5
	# center point of the formation is not the center of the figure
	offset = int(rad * math.sin(math.radians(90 + degrees_step)))
	back_angle = 54 # 2 * degrees_step - 90
	print("PROTECT", end=' ')
	for i in range(num_coords):
		if i == 0:
			print("0 0", end=' ') # centre
			pass
		elif i == 1: # front
			x = 0
			y = offset - rad
			print("{} {}".format(x,y) , end=' ')
		elif i == 2: # front left
			angle = math.radians(270 - degrees_step)
			x = int(math.cos(angle) * rad)
			y = 0
			print("{} {}".format(x,y), end=' ')
		elif i == 3: # front right
			angle = math.radians(270 + degrees_step)
			x = int(math.cos(angle) * rad)
			y = 0
			print("{} {}".format(x,y) , end=' ')
		elif i == 4: # back left
			angle = math.radians(180 - back_angle)
			x = int(math.cos(angle) * rad)
			y = int(math.sin(angle) * rad) + offset
			print("{} {}".format(x,y) , end=' ')
		elif i == 5: # back right
			angle = math.radians(back_angle)
			x = int(math.cos(angle) * rad)
			y = int(math.sin(angle) * rad) + offset
			print("{} {}".format(x,y) , end=' ')
		else:
			print(0, end=' ')
			print_y(24 * (i - 5), i)
	print()

# A simple 3-across block formation.
def generate_3by2():
	print("3BY2", end=' ')
	for i in range(num_coords):
		# x coordinate
		if i % 3 == 0:
			print(0, end=' ')
		elif i % 3 == 1:
			print(64, end=' ')
		else:
			print(-64, end=' ')

		# y coordinate
		print_y((i // 3) * 48, i)
	print()

# A simple 2-across block formation.
def generate_2by3():
	print("2BY3", end=' ')
	# left first, then right
	left_side = True
	yloc = 0
	for i in range(num_coords):
		if left_side: # left
			print(-24, end=' ')
			print_y(yloc, i)
		else: # right
			print(24, end=' ')
			print_y(yloc, i)
			# first step back is 48, then 36
			if yloc == 0:
				yloc = 48
			else:
				yloc += 36
		left_side = not left_side
	print()

# A horizontal line formation, with each character being placed
# alternately on right and left of the previous characters.
def generate_rank():
	print("RANK", end=' ')
	for i in range(num_coords):
		# lead character placed at focal point -32, spacing is 64
		if i % 2 == 0:
			print(-32 - ((i // 2) * 64), end=' ')
		else:
			print(-32 + (((i + 1) // 2) * 64), end=' ')
		print_y(0, i)
	print()

def generate_v():
	print("V", end=' ')
	for i in range(num_coords):
		if i % 2 == 0:
			xpos = (i // 2) * -15
		else:
			xpos = 64 + (i // 2) * -15
		ypos = (i // 2) * 48
		print(xpos, end=' ')
		print_y(ypos, i)
	print()

# A triangle with the lead character at the back. Focal point is at the
# front. Other characters are placed row-by-row starting at the front row,
# middle then left then right, with the maximum width being 3.
def generate_triangle():
	print("TRIANGLE", end=' ')
	for i in range(num_coords):
		pos = corrected_position_for_actor(i, 3)
		if pos == 0:
			print("0 0", end=' ') # front
		elif pos == 1:
			print("-32 36", end=' ') # middle left
		elif pos == 2:
			print("32 36", end=' ') # middle right
		else:
			pos = pos - 3
			# start 72 back, then move back 36 per row
			ypos = 72 + ((pos // 3) * 36)

			if pos % 3 == 0: # middle
				xpos = 0
			elif pos % 3 == 1: # left
				xpos = -64
			else: # right
				xpos = 64
			
			print(xpos, end=' ')
			print_y(ypos, i)
	print()

# A wide triangle with the lead character at the front. Characters are placed
# row-by-row. Second row: right then left. Third row: left then right then
# middle. Other rows: Middle first, left, right.
# TODO: the older games seem to have the third row ordered the same as the other ones
def generate_wedge():
	print("WEDGE", end=' ')
	for i in range(num_coords):
		if i == 0:
			print("0 0", end=' ') # front
		elif i == 1:
			print("64 36", end=' ') # second row: right
		elif i == 2:
			print("-64 36", end=' ') # second row: left
		elif i == 3:
			print("-124 72", end=' ') # third row: left
		elif i == 4:
			print("124 72", end=' ') # third row: right
		elif i == 5:
			print("0 72", end=' ') # third row: middle
		else:
			pos = i - 6
			if pos % 3 == 0:
				print(0, end=' ') # middle
			elif pos % 3 == 1:
				print(-124, end=' ') # left
			else:
				print(124, end=' ') # right
			ypos = 72 + (i // 3) * 36
			print_y(ypos, i)
	print()

def generate_none():
	print("NONE "  + "0 0 " * (num_coords - 1) + "0 0")

from sys import argv,exit

if len(argv) != 2:
	print("pass a game name on the command line")
	exit(1)

generate_header()

if argv[1] == "bg1" or argv[1] == "iwd" or argv[1] == "iwd2" or argv[1] == "how":
	generate_line("FOLLOW") # TODO: should be hard-coded game logic
	generate_t()
	generate_gather()
	generate_4and2()
	generate_3by2()
	generate_protect() # TODO: wrong formation for bg1 or others?
	generate_2by3()
	generate_rank()
	generate_v()
	generate_wedge()
	generate_s(False)
	generate_line("LINE")

if argv[1] == "pst":
	generate_line("FOLLOW") # TODO: should be hard-coded game logic
	generate_t()
	generate_gather()
	generate_4and2()
	generate_3by2()
	generate_protect()
	generate_2by3()
	generate_rank()
	generate_v()
	generate_wedge()
	generate_s(False)
	generate_line("LINE")
	generate_none()

if argv[1] == "bg2":
	generate_line("FOLLOW") # TODO: should be hard-coded game logic
	generate_t()
	generate_gather()
	generate_wavyline()
	generate_3by2()
	generate_protect()
	generate_2by3()
	generate_rank()
	generate_triangle()
	generate_wedge()
	generate_s(True)
	generate_line("LINE")
