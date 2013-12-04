# coding: utf8
import os
import datetime

#The table of posts of user's purchases submissions
db.define_table('purchase',
                Field('user_ref','reference auth_user'),
                Field('title','string'),
                Field('user_image','upload',uploadseparate=True),
				Field('store', requires=IS_IN_SET(['GameStop','Amazon','Best Buy','Target','Wal-Mart','Toys \'R Us', 'Ebay', 'Craigslist','FuncoLand','EB Games', 'GAME','other'])),
				Field('store_loc','string'),
				Field('price','float'),
                Field('description','text'),
				Field('time_submitted','datetime',default=request.now),
				Field('average_score','float'),
                Field('review_count','integer',default=0))


#Comments that people can leave on a post
db.define_table('rating',
                Field('user_ref','reference auth_user'),
                Field('purchase_ref','reference purchase'),
                Field('rating','integer',requires=IS_INT_IN_RANGE(1,10)))
