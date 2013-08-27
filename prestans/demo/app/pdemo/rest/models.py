#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Eternity Technologies nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ETERNITY TECHNOLOGIES BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from prestans import types

class Player(types.Model):
	player_id = types.Integer(required=False)
	first_name = types.String(required=True)
	last_name = types.String(required=True)
	#height = 
	weight = types.Integer(minimum=0, required=True)
	dob = types.Date(required=True)

class PlayerMatchStats(types.Model):

	match_id = types.Integer(required=True)
	player_id = types.Integer(required=True)

	minutes = types.Integer(minimum=0, default=0) #mintues played

	fgm = types.Integer(minimum=0, default=0) #field goals made
	fga = types.Integer(minimum=0, default=0) #field goals attempted

	tpm = types.Integer(minimum=0, default=0) #three pointers made
	tpa = types.Integer(minimum=0, default=0) #three pointers attempted

	ftm = types.Integer(minimum=0, default=0) #free throws made
	fta = types.Integer(minimum=0, default=0) #free throws attempted

	reb = types.Integer(minimum=0, default=0) #rebounds
	ast = types.Integer(minimum=0, default=0) #assists
	blk = types.Integer(minimum=0, default=0) #blocks
	stl = types.Integer(minimum=0, default=0) #steals
	pf = types.Integer(minimum=0, default=0) #personal fouls
	to = types.Integer(minimum=0, default=0) #turnovers
	pts = types.Integer(minimum=0, default=0) #points

class Match(types.Model):
	match_id = types.Integer(required=True)
	season_id = types.Integer(required=True)

	venue = types.String(required=True)

	player_stats = types.Array(element_template=PlayerMatchStats())

class Season(types.Model):
	season_id = types.Integer(required=True)

class Team(types.Model):
	team_id = types.String(required=True)
	city = types.String(required=True)
	name = types.String(required=True)




