# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import os
import json
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    return dict()
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

#This is the page for a user to submit a purchase.
@auth.requires_login()
def submitPurchase():
	form = SQLFORM.factory(
			Field('Title','string'),
			Field('user_image','upload',uploadfolder=os.path.join(request.folder,'uploads'),uploadseparate=True),
			Field('Description','text'),
			Field('store', requires=IS_IN_SET(['GameStop','Amazon','Best Buy','Target','Wal-Mart','Toys \'R Us', 'Ebay', 'Craigslist','FuncoLand','EB Games', 'GAME','other'])),
			Field('located','string'),
			Field('price','float'),
			table_name='purchase')
	if form.accepts(request.vars,formname='form'):
		logger.info('form.vars.user_image is:'+form.vars.user_image)
		logger.info('request.vars.user_image is:'+str(request.vars.user_image))
		#myFile = db.purchase.user_image.store(request.vars.user_image,form.vars.user_image)
		db.purchase.insert(user_ref=auth.user, title = form.vars.Title,
							user_image=form.vars.user_image,
							description=form.vars.Description,
							store=form.vars.store,
							store_loc = form.vars.located,
							price = round(form.vars.price,2)+0.00,
							average_score = 0
							)
	return dict(form=form)

def viewPurchases():
	if request.vars['pgnum']:
		page = int(request.vars['pgnum'])
	else:
		page = 0
        if request.vars['store']:
            if request.vars['store'] != "All":
                rows = db(db.purchase.store == request.vars['store']).select(orderby=~db.purchase.time_submitted)
                return dict(rows=rows,page=page)
        rows = db(db.purchase.id > 0).select(orderby=~db.purchase.time_submitted, limitby=(0+(page*25),25+(page*25)))
        return dict(rows=rows,page=page)

def viewSingle():
	if request.args(0):
		myID=request.args(0)
		row = db(db.purchase.id == myID).select().first()
		return dict(row=row)
	else:
		return dict()

@request.restful()
def review():
	def POST(**vars):
		myRow = db((db.rating.user_ref == vars['user']) & (db.rating.purchase_ref == vars['purchase'])).select().first()
		if myRow == None:
			#Insert a new review into the table
			db.rating.insert(user_ref=vars['user'], purchase_ref=vars['purchase'], rating=vars['score'])
                        purchaseRow = db(db.purchase.id == vars['purchase']).select().first()
                        db(db.purchase.id == vars['purchase']).update(review_count = purchaseRow.review_count+1)
                        vScore = float(vars['score'])
                        newScore = purchaseRow.average_score + vScore
                        rCount = purchaseRow.review_count+1
                        fScore = newScore/float(rCount)
                        db(db.purchase.id == vars['purchase']).update(average_score = fScore)
                        return "Thank you for reviewing"
		else:
			#update the currently existing row in the review table
			rating = db((db.rating.user_ref == vars['user']) & (db.rating.purchase_ref == vars['purchase'])).select().first()
                        db((db.rating.user_ref == vars['user']) & (db.rating.purchase_ref == vars['purchase'])).update(rating=vars['score'])
                        purchaseRow = db(db.purchase.id == vars['purchase']).select().first()
                        vScore = float(vars['score'])
                        rCount = float(purchaseRow.review_count)
                        allRatings = purchaseRow.average_score*rCount
                        newTotal = allRatings - float(rating.rating)
                        fTotal = newTotal + vScore
                        newAvg = fTotal/rCount
                        db(db.purchase.id == vars['purchase']).update(average_score = newAvg)
			return "You have updated your review"
	return dict(POST=POST)

@request.restful()
def sortPurchase():
    def GET(**vars):
        print vars['store']
        selectedRows = db(db.purchase.store == vars['store']).select()
        jsonRows = json.dumps([[row.id] for row in selectedRows])
        print jsonRows
        return jsonRows
    return dict(GET=GET)
