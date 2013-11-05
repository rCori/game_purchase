# coding: utf8

#The table of posts of user's purchases submissions
db.define_table('purchase',
                Field('user_ref','reference auth_user'),
                Field('title','string'),
                Field('user_image','upload'),
                Field('description','string'))


#Comments that people can leave on a post
db.define_table('rating',
                Field('user_ref','reference auth_user'),
                Field('purchase_ref','reference purchase'),
                Field('rating','integer',requires=IS_INT_IN_RANGE(1,10)))
